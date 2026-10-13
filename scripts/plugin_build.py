import ast
import importlib.util
import io
import json
import re
import sys
import tokenize
from pathlib import Path


JSON_REFERENCE = re.compile(r"\$json(?:\.[A-Za-z_][A-Za-z0-9_]*)+")
STRING_PREFIX = re.compile(r"(?i)^([rubf]*)(\"\"\"|'''|\"|')")


def resolve_reference(config, reference):
    value = config
    for part in reference.removeprefix("$json.").split("."):
        if not isinstance(value, dict) or part not in value:
            raise ValueError("Unknown config reference: {}".format(reference))
        value = value[part]
    if isinstance(value, (dict, list)):
        raise ValueError(
            "Config reference must resolve to a scalar value: {}".format(reference)
        )
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)


def replace_references(text, config):
    return JSON_REFERENCE.sub(
        lambda match: resolve_reference(config, match.group(0)),
        text,
    )


def token_offset(source_lines, position):
    row, column = position
    return sum(len(line) for line in source_lines[:row - 1]) + column


def replace_backtick_literals(source):
    result = []
    index = 0
    quote = None
    triple = False
    escaped = False
    in_comment = False

    while index < len(source):
        char = source[index]
        if in_comment:
            result.append(char)
            if char == "\n":
                in_comment = False
            index += 1
            continue
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif triple and source.startswith(quote * 3, index):
                result.extend((quote, quote, quote))
                index += 3
                quote = None
                triple = False
                continue
            elif not triple and char == quote:
                quote = None
            result.append(char)
            index += 1
            continue
        if char == "#":
            in_comment = True
            result.append(char)
            index += 1
            continue
        if char in ("'", '"'):
            quote = char
            triple = source.startswith(char * 3, index)
            width = 3 if triple else 1
            result.extend(char * width)
            index += width
            continue
        if char == "`":
            end = index + 1
            escaped_backtick = False
            while end < len(source):
                if source[end] == "\\":
                    escaped_backtick = not escaped_backtick
                    end += 1
                    continue
                if source[end] == "`" and not escaped_backtick:
                    break
                escaped_backtick = False
                end += 1
            if end < len(source):
                value = source[index + 1:end].replace(r"\`", "`")
                result.append(repr(value))
                index = end + 1
                continue
        result.append(char)
        index += 1

    return "".join(result)


def substitute_json_literals(source, config):
    source = replace_backtick_literals(source)
    lines = source.splitlines(keepends=True)
    replacements = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.STRING:
            continue
        prefix = STRING_PREFIX.match(token.string)
        if prefix is None or "f" in prefix.group(1).lower():
            continue
        try:
            value = ast.literal_eval(token.string)
        except (SyntaxError, ValueError):
            continue
        if not isinstance(value, str) or "$json." not in value:
            continue
        replacement = replace_references(value, config)
        if replacement != value:
            start = token_offset(lines, token.start)
            end = token_offset(lines, token.end)
            replacements.append((start, end, repr(replacement)))

    for start, end, replacement in reversed(replacements):
        source = source[:start] + replacement + source[end:]
    return source


def source_offset(lines, position):
    row, byte_column = position
    prefix = lines[row - 1].encode("utf-8")[:byte_column].decode("utf-8")
    return sum(len(line) for line in lines[:row - 1]) + len(prefix)


def local_import_target(node, module_name, package_name, module_names):
    if node.level:
        current_package = (
            module_name
            if module_name.endswith(".__init__")
            else module_name.rpartition(".")[0]
        )
        if module_name == package_name:
            current_package = package_name
        relative_name = "." * node.level + (node.module or "")
        try:
            target = importlib.util.resolve_name(relative_name, current_package)
        except ImportError:
            return None
        return target if target in module_names else None

    target = node.module or ""
    return target if target in module_names else None


def flatten_sources(source_path, config):
    package_name = source_path.name
    sources = {}
    paths = {}
    for python_file in source_path.rglob("*.py"):
        relative = python_file.relative_to(source_path)
        parts = relative.with_suffix("").parts
        if relative.name == "__init__.py":
            module_name = package_name + (
                "." + ".".join(relative.parent.parts) if relative.parent.parts else ""
            )
        else:
            module_name = package_name + "." + ".".join(parts)
        source = substitute_json_literals(
            python_file.read_text(encoding="utf-8"), config
        )
        sources[module_name] = source
        paths[module_name] = relative

    entry_module = package_name + ".plugin"
    if entry_module not in sources:
        raise ValueError(
            "Plugin entry module does not exist: {}".format(source_path / "plugin.py")
        )

    module_names = set(sources)
    dependencies = {name: set() for name in sources}
    removals = {name: [] for name in sources}
    future_features = []

    for module_name, source in sources.items():
        tree = ast.parse(source, filename=str(paths[module_name]))
        parent_map = {
            child: parent
            for parent in ast.walk(tree)
            for child in ast.iter_child_nodes(parent)
        }
        lines = source.splitlines(keepends=True)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if node.module == "__future__" and node.level == 0:
                future_features.extend(alias.name for alias in node.names)
                removals[module_name].append(
                    (
                        source_offset(lines, (node.lineno, node.col_offset)),
                        source_offset(lines, (node.end_lineno, node.end_col_offset)),
                    )
                )
                continue
            target = local_import_target(
                node, module_name, package_name, module_names
            )
            if target is None:
                continue
            if parent_map[node] is not tree:
                raise ValueError(
                    "Local module imports must be at module scope: {}".format(
                        paths[module_name]
                    )
                )
            if any(
                alias.asname is not None and alias.asname != alias.name
                for alias in node.names
            ):
                raise ValueError(
                    "Aliased local imports cannot be flattened: {}".format(
                        paths[module_name]
                    )
                )
            if node.module is None:
                imported_modules = [
                    target + "." + alias.name
                    for alias in node.names
                    if target + "." + alias.name in module_names
                ]
                if imported_modules:
                    raise ValueError(
                        "Importing a local module as a value cannot be flattened: "
                        "{}".format(paths[module_name])
                    )
            dependencies[module_name].add(target)
            removals[module_name].append(
                (
                    source_offset(lines, (node.lineno, node.col_offset)),
                    source_offset(lines, (node.end_lineno, node.end_col_offset)),
                )
            )

    ordered_modules = []
    visiting = set()
    visited = set()

    def visit(module_name):
        if module_name in visiting:
            raise ValueError(
                "Circular local imports cannot be flattened: {}".format(module_name)
            )
        if module_name in visited:
            return
        visiting.add(module_name)
        for dependency in sorted(dependencies[module_name]):
            visit(dependency)
        visiting.remove(module_name)
        visited.add(module_name)
        ordered_modules.append(module_name)

    for module_name in sorted(sources, key=lambda name: (name != package_name, name)):
        visit(module_name)

    output = []
    if future_features:
        features = ", ".join(sorted(set(future_features)))
        output.append("from __future__ import {}\n".format(features))
    for module_name in ordered_modules:
        source = sources[module_name]
        for start, end in sorted(removals[module_name], reverse=True):
            source = source[:start] + source[end:]
        source = source.strip()
        if source:
            output.append(source)
    return "\n\n".join(output) + "\n"


def build_plugin(config_path, source_path, output_path):
    with config_path.open(encoding="utf-8") as config_file:
        config = json.load(config_file)
    if not isinstance(config, dict):
        raise ValueError("The config JSON root must be an object")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        flatten_sources(source_path, config),
        encoding="utf-8",
    )


def main():
    if len(sys.argv) != 4:
        raise SystemExit(
            "Usage: scripts/plugin_build.py CONFIG.json SOURCE_DIR OUTPUT_FILE"
        )
    config_path, source_path, output_path = (
        Path(argument) for argument in sys.argv[1:]
    )
    build_plugin(config_path, source_path, output_path)


if __name__ == "__main__":
    main()
