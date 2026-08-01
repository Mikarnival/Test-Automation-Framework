# Python API Test Automation Framework

A learning project for building a Python API automation test framework from scratch.

## Current features

- FastAPI mock server
- Requests-based reusable HTTP client
- GET, POST, PUT and DELETE user APIs
- Pytest fixtures and parameterization
- YAML-driven test data
- Positive, negative and validation scenarios
- Multi-step API workflow tests
- Automatic test-data reset before every test
- Git feature-branch and pull-request workflow

## Project structure

```text
common/        HTTP client and YAML loader
conf/          Framework configuration
data/          YAML test data
mock_server/   Local FastAPI mock service
testcase/      Pytest test cases
conftest.py    Shared pytest fixtures
```

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install pytest requests fastapi uvicorn pyyaml
```

## Start mock server

```bash
python -m uvicorn mock_server.main:app --reload --port 8000
```
Or
```bash
python -m mock_server.main
```

## Run tests

```bash
python -m pytest -v
```

## Requirements

```bash
python -m pip freeze > requirements.txt
```