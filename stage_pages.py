import argparse
from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit

from build import EXPS


VERSION_FOLDERS = {
    "A": "版本A-清透玻璃版",
    "B": "版本B-模拟器版",
}


class LocalReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        if tag not in {"a", "link", "script", "img", "iframe"}:
            return
        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append(value)


def validate_local_links(site_dir):
    site_dir = Path(site_dir).resolve()
    failures = []

    for html_file in site_dir.rglob("*.html"):
        parser = LocalReferenceParser()
        parser.feed(html_file.read_text(encoding="utf-8"))
        for reference in parser.references:
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue

            relative_path = unquote(parsed.path)
            if relative_path.startswith("/"):
                target = site_dir / relative_path.lstrip("/")
            else:
                target = html_file.parent / relative_path

            try:
                target.resolve().relative_to(site_dir)
            except ValueError:
                failures.append(f"{html_file}: link escapes site: {reference}")
                continue

            if not target.exists():
                failures.append(f"{html_file}: missing target for {reference}")

    if failures:
        raise ValueError("Broken local link(s):\n" + "\n".join(failures))


def stage_site(build_dir, destination):
    build_dir = Path(build_dir)
    destination = Path(destination)
    required_files = [build_dir / "index.html"]

    for version in VERSION_FOLDERS:
        version_dir = build_dir / version
        required_files.extend(
            version_dir / name
            for name in (
                ["index.html", "all-in-one.html"]
                + [experiment["file"] + ".html" for experiment in EXPS]
            )
        )

    missing = [path for path in required_files if not path.is_file()]
    if missing:
        formatted = "\n".join(str(path) for path in missing)
        raise FileNotFoundError("Missing generated files:\n" + formatted)

    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(build_dir / "index.html", destination / "index.html")
    for version, folder in VERSION_FOLDERS.items():
        shutil.copytree(
            build_dir / version,
            destination / folder,
            dirs_exist_ok=True,
        )

    validate_local_links(destination)


def main():
    parser = argparse.ArgumentParser(
        description="Stage and validate the generated chemistry site for Pages."
    )
    parser.add_argument("--build-dir", type=Path, default=Path("build"))
    parser.add_argument("--output-dir", type=Path, default=Path("_site"))
    args = parser.parse_args()

    stage_site(args.build_dir, args.output_dir)
    print(f"Staged and validated site at {args.output_dir}")


if __name__ == "__main__":
    main()
