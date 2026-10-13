# exteraGram plugin SDK stubs

This folder contains the official type stubs for exteraGram Python Plugins SDK
1.4.5.8-beta. They provide IDE autocomplete and static type information for
modules such as `base_plugin`, `client_utils`, `ui.settings`, and `hook_utils`.
They are not a desktop runtime: the modules run inside exteraGram.

## Use in this project

Run `make sdk` from the project root to download the latest official stubs.

In VS Code, add `sdk/stubs` to `python.analysis.extraPaths` in
`.vscode/settings.json`:

```json
{
  "python.analysis.extraPaths": ["./sdk/stubs"]
}
```

For Pyright, this can also be set in `pyrightconfig.json`:

```json
{
  "extraPaths": ["sdk/stubs"]
}
```

## Source and integrity

- Official release: <https://github.com/exteraSquad/plugins-pysdk-builds/releases/tag/sdk-v1.4.5.8-beta-37843526009-1>
- Downloaded asset: `stubs.zip` (contains `pyi-files.zip`)
- SHA-256 of `stubs.zip`: `a41abef8c16fc72d808b8511fbbf44bbc1e3c0e1bf6b24cb6406e68219f4b8b2`
- SDK version: `1.4.5.8-beta`; use exteraGram `12.5.1+` per the current plugin docs.

For SDK documentation and plugin examples, see <https://plugins.exteragram.app/docs>.
