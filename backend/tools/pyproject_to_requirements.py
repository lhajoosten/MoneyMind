"""Simple converter: pyproject.toml -> requirements.txt (+ optional dev file)

Limitaties:
- Schrijft enkel de dependency specifiers zoals in pyproject.toml (geen transitive pinning).
- Use this for quick Docker installs. For reproducible pinned installs, create a venv and pip freeze.
"""
from __future__ import annotations
import sys
from pathlib import Path
import argparse
import tomllib

def read_pyproject(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)

def format_deps(deps: list[str]) -> list[str]:
    # Keep lines as-is, strip comments/empty
    out = []
    for d in deps:
        line = d.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out

def write_file(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + ("\n" if lines else ""))

def main() -> int:
    p = argparse.ArgumentParser(description="Generate requirements.txt from pyproject.toml")
    p.add_argument("--pyproject", "-p", default="pyproject.toml", help="pyproject.toml path (relative to current dir)")
    p.add_argument("--out", "-o", default="requirements.txt", help="output requirements file")
    p.add_argument("--dev-out", "-d", default="requirements-dev.txt", help="optional dev requirements output")
    p.add_argument("--include-dev", action="store_true", help="also write optional-dependencies.dev to dev-out")
    args = p.parse_args()

    pyproject_path = Path(args.pyproject)
    if not pyproject_path.exists():
        print(f"ERROR: {pyproject_path} not found", file=sys.stderr)
        return 2

    data = read_pyproject(pyproject_path)
    project = data.get("project", {})
    deps = project.get("dependencies", []) or []
    deps = format_deps(deps)

    write_file(Path(args.out), deps)
    print(f"Wrote {len(deps)} dependencies to {args.out}")

    if args.include_dev:
        opt = data.get("project", {}).get("optional-dependencies", {}) or {}
        dev_deps = opt.get("dev", []) or []
        dev_deps = format_deps(dev_deps)
        write_file(Path(args.dev_out), dev_deps)
        print(f"Wrote {len(dev_deps)} dev-deps to {args.dev_out}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())