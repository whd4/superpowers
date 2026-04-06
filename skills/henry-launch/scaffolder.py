#!/usr/bin/env python3
"""HENRY AI Project Scaffolder.

Creates complete project structures for agency, acquisition, and MCP server projects.

Usage:
  python scaffolder.py --type agency --name my-client-project
  python scaffolder.py --type acquisition --name target-TXS5345
  python scaffolder.py --type mcp-server --name inventory-mcp
  python scaffolder.py --type agency --name test --dry-run
  python scaffolder.py --test
"""
import argparse
import os
import sys
import json

# === FILE TEMPLATES ===

DOCKERFILE_PYTHON = '''FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

FASTAPI_MAIN = '''from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .auth import get_current_user

app = FastAPI(title="{name}", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {{"status": "healthy", "service": "{name}"}}


@app.get("/api/v1/status", dependencies=[Depends(get_current_user)])
async def status():
    return {{"status": "operational"}}
'''

FASTAPI_AUTH = '''import os
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

SECRET_KEY = os.environ.get("JWT_SECRET", "CHANGE-ME-IN-PRODUCTION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
'''

REQUIREMENTS_AGENCY = '''fastapi>=0.104.0
uvicorn[standard]>=0.24.0
PyJWT>=2.8.0
python-dotenv>=1.0.0
pytest>=7.4.0
httpx>=0.25.0
'''

DOCKER_COMPOSE = '''services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
'''

GITHUB_ACTIONS = '''name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: {name}:latest
'''

ENV_EXAMPLE = '''# Copy to .env and fill in values
JWT_SECRET=generate-with-auth_setup.py
DATABASE_URL=sqlite:///./app.db
'''

GITIGNORE = '''.env
__pycache__/
*.pyc
.pytest_cache/
node_modules/
dist/
.venv/
'''

CLAUDE_MD_AGENCY = '''# {name}

## Project Type
HENRY AI Agency Project — AI transformation for client.

## Stack
- Backend: Python 3.11 + FastAPI
- Auth: JWT (PyJWT)
- Deployment: Docker + GitHub Actions
- Testing: pytest + httpx

## Commands
- Run locally: `docker compose up`
- Run tests: `pytest`
- Health check: `curl localhost:8000/health`

## Rules
- Never commit .env files
- All endpoints require JWT auth except /health
- Write tests before implementation (TDD)
'''

TEST_MAIN = '''from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
'''

# MCP Server templates
MCP_SERVER = '''"""MCP Server: {name}"""
from mcp import Server, StdioTransport

server = Server("{name}")


@server.tool("health_check")
async def health_check() -> dict:
    """Check if the server is running."""
    return {{"status": "healthy", "server": "{name}"}}


@server.tool("example_tool")
async def example_tool(input_text: str) -> dict:
    """Example tool — replace with your implementation.

    Args:
        input_text: The input to process.
    """
    try:
        result = f"Processed: {{input_text}}"
        return {{"status": "success", "result": result}}
    except Exception as e:
        return {{"status": "error", "message": str(e)}}


if __name__ == "__main__":
    import asyncio
    transport = StdioTransport()
    asyncio.run(server.run(transport))
'''

MCP_REQUIREMENTS = '''mcp>=1.0.0
pytest>=7.4.0
'''

MCP_TEST = '''import pytest
from src.server import health_check, example_tool


@pytest.mark.asyncio
async def test_health_check():
    result = await health_check()
    assert result["status"] == "healthy"


@pytest.mark.asyncio
async def test_example_tool():
    result = await example_tool(input_text="hello")
    assert result["status"] == "success"
'''

DOCKERFILE_MCP = '''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "src.server"]
'''

CLAUDE_MD_MCP = '''# {name}

## Project Type
HENRY AI MCP Server.

## Stack
- Runtime: Python 3.11
- Framework: MCP SDK (stdio transport)
- Testing: pytest + pytest-asyncio

## Commands
- Run: `python -m src.server`
- Test: `pytest`
- Build: `docker build -t {name} .`

## Rules
- Every tool must have typed parameters and docstrings
- Every tool must return {{"status": "success/error", ...}}
- Error boundaries on all tool calls
- Write tests before implementation (TDD)
'''

# Acquisition templates
DD_CHECKLIST = '''{
  "target": "{name}",
  "date": "",
  "financial": {
    "revenue_verification": {"status": "pending", "source": "", "notes": ""},
    "client_concentration": {"status": "pending", "top_client_pct": null, "notes": ""},
    "ar_aging": {"status": "pending", "over_90_days_pct": null, "notes": ""},
    "revenue_trend": {"status": "pending", "3yr_trend": "", "notes": ""},
    "expense_analysis": {"status": "pending", "owner_comp": null, "notes": ""}
  },
  "operational": {
    "key_person_dependency": {"status": "pending", "risk_level": "", "notes": ""},
    "staff_assessment": {"status": "pending", "headcount": null, "avg_tenure": null, "notes": ""},
    "technology_stack": {"status": "pending", "systems": [], "notes": ""},
    "process_documentation": {"status": "pending", "sops_exist": false, "notes": ""},
    "client_contracts": {"status": "pending", "transferable": null, "notes": ""}
  },
  "legal": {
    "active_litigation": {"status": "pending", "cases": [], "notes": ""},
    "tax_liens": {"status": "pending", "found": false, "notes": ""},
    "regulatory_compliance": {"status": "pending", "licenses_current": null, "notes": ""},
    "employment_issues": {"status": "pending", "notes": ""},
    "ip_ownership": {"status": "pending", "notes": ""}
  },
  "market": {
    "industry_trends": {"status": "pending", "direction": "", "notes": ""},
    "competitive_landscape": {"status": "pending", "competitors": [], "notes": ""},
    "regulatory_changes": {"status": "pending", "notes": ""},
    "disruption_risk": {"status": "pending", "notes": ""}
  }
}
'''

FINANCIAL_MODEL = '''{
  "target": "{name}",
  "acquisition_math": {
    "trailing_revenue": null,
    "purchase_multiple": 0.4,
    "purchase_price": null,
    "down_payment_pct": 10,
    "sba_loan_pct": 90,
    "sba_rate_pct": null,
    "sba_term_years": 10
  },
  "transform": {
    "ai_implementation_cost": null,
    "timeline_days": 90,
    "staff_changes": "",
    "process_automation": ""
  },
  "steady_state": {
    "revenue_post_transform": null,
    "target_ebitda_margin_pct": 65,
    "monthly_debt_service": null,
    "monthly_operating_cost": null
  },
  "exit": {
    "target_multiple": 7,
    "exit_timeline_months": 36
  },
  "scenarios": {
    "best": {"revenue_growth_pct": null, "ebitda_margin_pct": null},
    "expected": {"revenue_growth_pct": null, "ebitda_margin_pct": null},
    "worst": {"revenue_growth_pct": null, "ebitda_margin_pct": null}
  }
}
'''

TRANSFORM_PLAN = '''# 90-Day AI Transformation Plan: {name}

## Phase 1: Assessment (Days 1-15)
- [ ] Complete technology audit
- [ ] Map all manual processes
- [ ] Identify automation candidates (score by impact × ease)
- [ ] Assess staff AI readiness
- [ ] Document current workflows

## Phase 2: Implementation (Days 16-60)
- [ ] Deploy core AI tools (document processing, client communication)
- [ ] Automate top 3 manual processes
- [ ] Train staff on AI workflows
- [ ] Set up monitoring and KPI dashboards
- [ ] Migrate critical data to new systems

## Phase 3: Optimization (Days 61-90)
- [ ] Measure efficiency gains vs. baseline
- [ ] Optimize underperforming automations
- [ ] Document all new SOPs
- [ ] Calculate realized EBITDA improvement
- [ ] Prepare steady-state operating model

## Success Metrics
- Process automation rate: target >70%
- Staff efficiency gain: target 2-3x
- EBITDA margin: target 60-70%
- Client satisfaction: maintain or improve NPS
'''

CLAUDE_MD_ACQUISITION = '''# {name}

## Project Type
HENRY AI CPA Acquisition — due diligence and transformation.

## Structure
- diligence/ — DD checklist (JSON), financial model (JSON), risk register
- legal/ — LOI and NDA templates
- transform/ — 90-day AI transformation plan

## Workflow
1. Fill diligence/dd_checklist.json as research progresses
2. Fill diligence/financial_model.json with verified numbers
3. Run risk assessment: `python risk_matrix.py`
4. Draft LOI after DD clears
5. Execute 90-day transform plan post-close

## Rules
- Every number must have a source
- Use 70% of optimistic as expected scenario
- Always recommend attorney review for binding documents
'''


# === SCAFFOLDER LOGIC ===

def get_agency_files(name):
    return {
        "Dockerfile": DOCKERFILE_PYTHON.format(name=name),
        "docker-compose.yml": DOCKER_COMPOSE.format(name=name),
        ".github/workflows/deploy.yml": GITHUB_ACTIONS.format(name=name),
        "requirements.txt": REQUIREMENTS_AGENCY,
        "backend/__init__.py": "",
        "backend/main.py": FASTAPI_MAIN.format(name=name),
        "backend/auth.py": FASTAPI_AUTH,
        "backend/tests/__init__.py": "",
        "backend/tests/test_main.py": TEST_MAIN,
        ".env.example": ENV_EXAMPLE,
        ".gitignore": GITIGNORE,
        "CLAUDE.md": CLAUDE_MD_AGENCY.format(name=name),
    }


def get_mcp_files(name):
    return {
        "Dockerfile": DOCKERFILE_MCP.format(name=name),
        ".github/workflows/deploy.yml": GITHUB_ACTIONS.format(name=name),
        "requirements.txt": MCP_REQUIREMENTS,
        "src/__init__.py": "",
        "src/server.py": MCP_SERVER.format(name=name),
        "tests/__init__.py": "",
        "tests/test_tools.py": MCP_TEST,
        ".gitignore": GITIGNORE,
        "CLAUDE.md": CLAUDE_MD_MCP.format(name=name),
    }


def get_acquisition_files(name):
    return {
        "diligence/dd_checklist.json": DD_CHECKLIST.replace("{name}", name),
        "diligence/financial_model.json": FINANCIAL_MODEL.replace("{name}", name),
        "diligence/risk_register.json": '{"risks": []}',
        "legal/loi_template.md": f"# Letter of Intent: {name}\n\n[Use /legal agent to draft full LOI]\n",
        "legal/nda_template.md": f"# Non-Disclosure Agreement: {name}\n\n[Use /legal agent to draft full NDA]\n",
        "transform/90_day_plan.md": TRANSFORM_PLAN.format(name=name),
        "transform/integration_checklist.md": f"# Integration Checklist: {name}\n\n- [ ] Technology migration\n- [ ] Staff onboarding\n- [ ] Client communication\n- [ ] Brand transition\n- [ ] Regulatory filings\n",
        "CLAUDE.md": CLAUDE_MD_ACQUISITION.format(name=name),
    }


PROJECT_TYPES = {
    "agency": get_agency_files,
    "acquisition": get_acquisition_files,
    "mcp-server": get_mcp_files,
}


def scaffold(project_type, name, dry_run=False):
    if project_type not in PROJECT_TYPES:
        print(f"Error: Unknown type '{project_type}'. Choose: {', '.join(PROJECT_TYPES.keys())}")
        sys.exit(1)

    files = PROJECT_TYPES[project_type](name)
    base_dir = name

    if dry_run:
        print(f"DRY RUN — Would create {len(files)} files in '{base_dir}/':\n")
        for path in sorted(files.keys()):
            print(f"  {base_dir}/{path}")
        return {"files_count": len(files), "base_dir": base_dir}

    os.makedirs(base_dir, exist_ok=True)
    created = []
    for path, content in files.items():
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        created.append(full_path)

    print(f"Created {len(created)} files in '{base_dir}/':")
    for f in sorted(created):
        print(f"  {f}")

    return {"files_count": len(created), "base_dir": base_dir}


def run_tests():
    import tempfile
    import shutil

    for ptype in ["agency", "acquisition", "mcp-server"]:
        # Dry run test
        result = scaffold(ptype, f"test-{ptype}", dry_run=True)
        assert result["files_count"] > 0, f"{ptype}: no files generated"

        # Actual scaffold in temp dir
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                result = scaffold(ptype, f"test-{ptype}")
                assert result["files_count"] > 0
                assert os.path.isdir(f"test-{ptype}")

                # Check CLAUDE.md always exists
                assert os.path.isfile(f"test-{ptype}/CLAUDE.md"), f"{ptype}: missing CLAUDE.md"

                # Type-specific checks
                if ptype == "agency":
                    assert os.path.isfile(f"test-{ptype}/backend/main.py")
                    assert os.path.isfile(f"test-{ptype}/backend/auth.py")
                    assert os.path.isfile(f"test-{ptype}/Dockerfile")
                elif ptype == "acquisition":
                    assert os.path.isfile(f"test-{ptype}/diligence/dd_checklist.json")
                    # Validate JSON
                    with open(f"test-{ptype}/diligence/dd_checklist.json") as jf:
                        json.load(jf)
                elif ptype == "mcp-server":
                    assert os.path.isfile(f"test-{ptype}/src/server.py")
            finally:
                os.chdir(old_cwd)

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HENRY AI Project Scaffolder")
    parser.add_argument("--type", choices=list(PROJECT_TYPES.keys()), help="Project type")
    parser.add_argument("--name", help="Project name (used as directory name)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating files")
    parser.add_argument("--test", action="store_true", help="Run self-tests")

    args = parser.parse_args()

    if args.test:
        run_tests()
    elif args.type and args.name:
        scaffold(args.type, args.name, dry_run=args.dry_run)
    else:
        parser.print_help()
