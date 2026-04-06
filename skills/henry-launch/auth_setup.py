#!/usr/bin/env python3
"""HENRY AI Auth Setup.

Generates JWT secrets and creates .env files for secure deployment.

Usage:
  python auth_setup.py --path ./my-project
  python auth_setup.py --test
"""
import argparse
import os
import secrets
import sys


def setup_auth(path):
    print(f"═══ HENRY AI AUTH SETUP ═══\nProject: {path}\n")

    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a directory")
        return {"status": "error", "message": "Directory not found"}

    env_example = os.path.join(path, ".env.example")
    env_file = os.path.join(path, ".env")

    # Generate secure JWT secret
    jwt_secret = secrets.token_urlsafe(48)

    # Read .env.example if it exists, otherwise create default
    if os.path.isfile(env_example):
        with open(env_example) as f:
            template = f.read()
    else:
        template = "JWT_SECRET=\nDATABASE_URL=sqlite:///./app.db\n"

    # Replace placeholder values
    env_content = template.replace("generate-with-auth_setup.py", jwt_secret)
    env_content = env_content.replace("JWT_SECRET=\n", f"JWT_SECRET={jwt_secret}\n")

    # Write .env
    with open(env_file, "w") as f:
        f.write(env_content)

    # Verify .gitignore includes .env
    gitignore_path = os.path.join(path, ".gitignore")
    gitignore_ok = False
    if os.path.isfile(gitignore_path):
        with open(gitignore_path) as f:
            if ".env" in f.read():
                gitignore_ok = True

    if not gitignore_ok:
        # Add .env to gitignore
        with open(gitignore_path, "a") as f:
            f.write("\n.env\n")
        print("  [FIXED] Added .env to .gitignore")

    # Verify no secrets in tracked files
    auth_py = os.path.join(path, "backend", "auth.py")
    if os.path.isfile(auth_py):
        with open(auth_py) as f:
            content = f.read()
        if "CHANGE-ME-IN-PRODUCTION" in content:
            print("  [OK] auth.py uses env var with safe default marker")
        elif jwt_secret in content:
            print("  [WARN] JWT secret found in auth.py — this should use os.environ")

    print(f"\n  [OK] JWT secret generated ({len(jwt_secret)} chars)")
    print(f"  [OK] .env file created at {env_file}")
    print(f"  [OK] .gitignore includes .env: {gitignore_ok or 'fixed'}")
    print(f"\n  NEXT: Review .env and adjust values as needed")

    return {"status": "success", "env_file": env_file, "secret_length": len(jwt_secret)}


def run_tests():
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .env.example
        with open(os.path.join(tmpdir, ".env.example"), "w") as f:
            f.write("JWT_SECRET=generate-with-auth_setup.py\nDATABASE_URL=sqlite:///./app.db\n")
        with open(os.path.join(tmpdir, ".gitignore"), "w") as f:
            f.write(".env\n__pycache__/\n")

        result = setup_auth(tmpdir)
        assert result["status"] == "success"
        assert result["secret_length"] >= 48

        # Verify .env was created
        env_path = os.path.join(tmpdir, ".env")
        assert os.path.isfile(env_path)

        # Verify secret was injected
        with open(env_path) as f:
            content = f.read()
        assert "generate-with-auth_setup.py" not in content
        assert "JWT_SECRET=" in content
        assert len(content.split("JWT_SECRET=")[1].split("\n")[0]) >= 48

    # Test with nonexistent path
    result = setup_auth("/nonexistent")
    assert result["status"] == "error"

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HENRY AI Auth Setup")
    parser.add_argument("--path", help="Path to project directory")
    parser.add_argument("--test", action="store_true", help="Run self-tests")

    args = parser.parse_args()

    if args.test:
        run_tests()
    elif args.path:
        setup_auth(args.path)
    else:
        parser.print_help()
