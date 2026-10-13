import hashlib
import io
import json
import re
import shutil
import stat
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath


RELEASE_API = (
    "https://api.github.com/repos/exteraSquad/plugins-pysdk-builds/releases/latest"
)
SDK_DIR = Path(__file__).resolve().parent.parent / "sdk"
VERSION_PATTERN = re.compile(r"\bSDK\s+v([0-9][A-Za-z0-9.+-]*)", re.IGNORECASE)


def download(url):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "plugins-sdk-updater",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def extract_stubs(archive_bytes, destination):
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as outer:
        try:
            inner_bytes = outer.read("pyi-files.zip")
        except KeyError as error:
            raise ValueError("SDK archive does not contain pyi-files.zip") from error

    with zipfile.ZipFile(io.BytesIO(inner_bytes)) as inner:
        entries = [entry for entry in inner.infolist() if not entry.is_dir()]
        if not entries:
            raise ValueError("SDK archive contains no stub files")
        for entry in entries:
            member = PurePosixPath(entry.filename)
            if member.is_absolute() or "\\" in entry.filename or ".." in member.parts:
                raise ValueError("Unsafe path in SDK archive: {}".format(entry.filename))
            if member.suffix != ".pyi":
                raise ValueError(
                    "Unexpected file in SDK stub archive: {}".format(entry.filename)
                )
            if stat.S_ISLNK(entry.external_attr >> 16):
                raise ValueError(
                    "Symlinks are not allowed in SDK archive: {}".format(entry.filename)
                )
            target = destination.joinpath(*member.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(inner.read(entry))
    return inner_bytes


def update_readme(release_url, version, checksum):
    readme_path = SDK_DIR / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme = re.sub(
        r"(?m)^- Official release: .*",
        "- Official release: <{}>".format(release_url),
        readme,
    )
    readme = re.sub(
        r"(?m)^- SHA-256 of `stubs\.zip`: .*",
        "- SHA-256 of `stubs.zip`: `{}`".format(checksum),
        readme,
    )
    readme = re.sub(
        r"(?m)^- SDK version: .*",
        "- SDK version: `{}`; use exteraGram `12.5.1+` per the current plugin docs.".format(
            version
        ),
        readme,
    )
    readme_path.write_text(readme, encoding="utf-8")


def main():
    release = json.loads(download(RELEASE_API).decode("utf-8"))
    release_name = release.get("name") or release.get("tag_name", "")
    version_match = VERSION_PATTERN.search(release_name)
    if not version_match:
        raise ValueError(
            "Could not determine SDK version from latest release: {}".format(
                release_name
            )
        )

    assets = release.get("assets", [])
    asset = next((item for item in assets if item.get("name") == "stubs.zip"), None)
    if asset is None or not asset.get("browser_download_url"):
        raise ValueError("Latest SDK release has no downloadable stubs.zip asset")
    archive_bytes = download(asset["browser_download_url"])

    with tempfile.TemporaryDirectory(prefix="sdk-update-") as temporary_dir:
        staged_stubs = Path(temporary_dir) / "stubs"
        staged_stubs.mkdir()
        inner_bytes = extract_stubs(archive_bytes, staged_stubs)

        SDK_DIR.mkdir(parents=True, exist_ok=True)
        target_stubs = SDK_DIR / "stubs"
        target_stubs.mkdir(parents=True, exist_ok=True)
        for old_stub in target_stubs.rglob("*.pyi"):
            old_stub.unlink()
        for staged_stub in staged_stubs.rglob("*.pyi"):
            target = target_stubs / staged_stub.relative_to(staged_stubs)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(staged_stub, target)

    (SDK_DIR / "stubs.zip").write_bytes(archive_bytes)
    (SDK_DIR / "pyi-files.zip").write_bytes(inner_bytes)
    checksum = hashlib.sha256(archive_bytes).hexdigest()
    update_readme(release["html_url"], version_match.group(1), checksum)
    print(
        "Updated SDK stubs to {} ({})".format(version_match.group(1), checksum)
    )


if __name__ == "__main__":
    main()
