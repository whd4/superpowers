#!/usr/bin/env python3
"""HENRY AI Project Deployer.

Validates, builds, and deploys Docker-based HENRY projects.

Usage:
  python deployer.py --path ./my-project
  python deployer.py --path ./my-project --dry-run
  python deployer.py --test
"""
import argparse
import os
import subprocess
import sys
import json


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    msg = f"  [{status}] {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return condition


def deploy(path, dry_run=False):
    print(f"═══ HENRY AI DEPLOYER ═══\nProject: {path}\n")

    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a directory")
        return {"status": "error", "message": "Directory not found"}

    results = {"checks": [], "status": "pending"}

    # 1. Validate structure
    print("VALIDATION:")
    has_dockerfile = check("Dockerfile exists", os.path.isfile(os.path.join(path, "Dockerfile")))
    has_claude = check("CLAUDE.md exists", os.path.isfile(os.path.join(path, "CLAUDE.md")))
    has_gitignore = check(".gitignore exists", os.path.isfile(os.path.join(path, ".gitignore")))

    # Check no secrets committed
    env_file = os.path.join(path, ".env")
    gitignore_path = os.path.join(path, ".gitignore")
    env_in_gitignore = False
    if os.path.isfile(gitignore_path):
        with open(gitignore_path) as f:
            env_in_gitignore = ".env" in f.read()
    check(".env in .gitignore", env_in_gitignore or not os.path.isfile(env_file),
          "SECURITY: .env must be gitignored")

    no_secrets = True
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__", ".venv")]
        for f in files:
            if f == ".env":
                continue  # .env is expected locally, just not committed
            fpath = os.path.join(root, f)
            try:
                with open(fpath, "r", errors="ignore") as fh:
                    content = fh.read()
                    if "CHANGE-ME-IN-PRODUCTION" not in content and any(
                        marker in content.lower() for marker in
                        ["sk-", "api_key=sk", "password=", "secret_key="]
                    ):
                        check("No hardcoded secrets", False, f"Found in {fpath}")
                        no_secrets = False
            except (UnicodeDecodeError, IsADirectoryError):
                pass
    if no_secrets:
        check("No hardcoded secrets", True)

    if not has_dockerfile:
        print("\nCANNOT DEPLOY — no Dockerfile found")
        return {"status": "failed", "reason": "No Dockerfile"}

    if dry_run:
        print("\nDRY RUN — skipping build and deploy steps")
        return {"status": "dry_run", "validation": "passed" if has_dockerfile else "failed"}

    # 2. Build Docker image
    print("\nBUILD:")
    project_name = os.path.basename(os.path.abspath(path))
    tag = f"henry-{project_name}:latest"

    try:
        result = subprocess.run(
            ["docker", "build", "-t", tag, "."],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=300,
        )
        build_ok = result.returncode == 0
        check("Docker build", build_ok,
              "Success" if build_ok else result.stderr[-200:] if result.stderr else "Unknown error")
    except FileNotFoundError:
        check("Docker build", False, "Docker not installed or not in PATH")
        build_ok = False
    except subprocess.TimeoutExpired:
        check("Docker build", False, "Build timed out (300s)")
        build_ok = False

    if not build_ok:
        print("\nCANNOT DEPLOY — Docker build failed")
        return {"status": "failed", "reason": "Docker build failed"}

    # 3. Report
    print(f"\nDEPLOY STATUS:")
    print(f"  Image: {tag}")
    print(f"  Run: docker run -p 8000:8000 --env-file .env {tag}")
    print(f"  Health: curl http://localhost:8000/health")

    return {"status": "ready", "image": tag}


def run_tests():
    import tempfile

    # Test with valid project
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create minimal project
        with open(os.path.join(tmpdir, "Dockerfile"), "w") as f:
            f.write("FROM python:3.11-slim\n")
        with open(os.path.join(tmpdir, "CLAUDE.md"), "w") as f:
            f.write("# Test\n")
        with open(os.path.join(tmpdir, ".gitignore"), "w") as f:
            f.write(".env\n")

        result = deploy(tmpdir, dry_run=True)
        assert result["status"] == "dry_run"
        assert result["validation"] == "passed"

    # Test with missing directory
    result = deploy("/nonexistent/path")
    assert result["status"] == "error"

    # Test with empty directory (no Dockerfile)
    with tempfile.TemporaryDirectory() as tmpdir:
        result = deploy(tmpdir, dry_run=True)
        assert result["status"] == "failed"

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HENRY AI Project Deployer")
    parser.add_argument("--path", help="Path to project directory")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, don't build")
    parser.add_argument("--test", action="store_true", help="Run self-tests")

    args = parser.parse_args()

    if args.test:
        run_tests()
    elif args.path:
        deploy(args.path, dry_run=args.dry_run)
    else:
        parser.print_help()
