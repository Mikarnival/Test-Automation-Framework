# Python API Test Automation Framework

A learning project for building a Python API automation test framework from scratch.

## Current features

- FastAPI mock server
- Requests-based HTTP client
- Pytest fixtures
- Pytest parameterization
- YAML-driven test data
- GET API tests
- Positive and negative test scenarios

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

## Run tests

```bash
python -m pytest -v
```

## Requirements

```bash
python -m pip freeze > requirements.txt
```