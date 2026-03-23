"""
Run import-linter (layers + application vs infrastructure) then enforce domain isolation.

Domain rule (automatic for every `src/<bounded_context>/domain/` tree): code there may only
pull in `src.<same>.domain` or `src.shared.domain` (shared kernel). No new rules when you add a BC.
"""

from __future__ import annotations

import ast
import os
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _package_for_file(py_file: Path, src_root: Path) -> str:
    rel = py_file.relative_to(src_root).parent
    if rel == Path("."):
        return "src"
    return "src." + ".".join(rel.parts)


def _bounded_context_for_domain_file(py_file: Path, src_root: Path) -> str | None:
    rel = py_file.relative_to(src_root)
    parts = rel.parts
    if len(parts) < 2 or parts[1] != "domain":
        return None
    return parts[0]


def _imports_from_import_from(node: ast.ImportFrom, package: str) -> list[tuple[str, int]]:
    if node.level == 0:
        if node.module is None:
            return []
        return [(node.module, node.lineno)]

    parts = package.split(".")
    up = node.level - 1
    if up > len(parts) - 1:
        return []
    base = ".".join(parts[:-up]) if up else package

    if node.module:
        return [(f"{base}.{node.module}", node.lineno)]

    out: list[tuple[str, int]] = []
    for alias in node.names:
        if alias.name != "*":
            out.append((f"{base}.{alias.name}", node.lineno))
    return out


def _collect_src_modules(tree: ast.AST, package: str) -> list[tuple[str, int]]:
    found: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append((alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            found.extend(_imports_from_import_from(node, package))

    return found


def _allowed_prefixes(bc: str) -> tuple[str, ...]:
    own = f"src.{bc}.domain"
    if bc == "shared":
        return (own,)
    return (own, "src.shared.domain")


def _is_allowed_src_import(module: str, bc: str) -> bool:
    if not module.startswith("src."):
        return True
    for prefix in _allowed_prefixes(bc):
        if module == prefix or module.startswith(prefix + "."):
            return True
    return False


def check_domain_imports() -> list[str]:
    root = _repo_root()
    src_root = root / "src"
    errors: list[str] = []

    for py_file in sorted(src_root.glob("*/domain/**/*.py")):
        bc = _bounded_context_for_domain_file(py_file, src_root)
        if bc is None:
            continue

        package = _package_for_file(py_file, src_root)
        try:
            source = py_file.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(py_file))
        except SyntaxError as exc:
            errors.append(f"{py_file}: syntax error: {exc}")
            continue

        for mod, lineno in _collect_src_modules(tree, package):
            if not mod.startswith("src."):
                continue
            if not _is_allowed_src_import(mod, bc):
                errors.append(
                    f"{py_file}:{lineno}: domain in {bc!r} must not depend on {mod!r} "
                    f"(allowed: {', '.join(_allowed_prefixes(bc))})"
                )

    return errors


def run_import_linter() -> int:
    sys.path.insert(0, os.getcwd())
    from importlinter.cli import lint_imports as import_linter_main

    return import_linter_main()


def main() -> int:
    os.chdir(_repo_root())
    il_code = run_import_linter()
    if il_code != 0:
        return il_code

    violations = check_domain_imports()
    if violations:
        print("Domain import violations:", file=sys.stderr)
        for line in violations:
            print(line, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
