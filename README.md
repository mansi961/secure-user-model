
# Secure User Model

A FastAPI application demonstrating secure user authentication and a calculation
engine, built with SQLAlchemy, Pydantic, and a factory-pattern design for
extensible arithmetic operations. Includes a full CI/CD pipeline via GitHub
Actions that runs the test suite and pushes a Docker image to Docker Hub on
every successful build.

## Features

- User model: secure registration with bcrypt password hashing (never stores plain-text passwords).
- Calculation model: stores two operands (a, b), an operation type (Add, Sub, Multiply, Divide), and the computed result, linked to a user via foreign key.
- Factory pattern: CalculationFactory selects and runs the correct operation class based on the requested type.
- Pydantic schemas: CalculationCreate validates incoming data (rejects invalid operation types and division by zero); CalculationRead serializes output data.
- 100% test coverage: unit tests for the factory and schema validation, plus integration tests against a real PostgreSQL database.

## Running Tests Locally

1. Install dependencies (inside a virtual environment):

        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt

2. Start a PostgreSQL test database on localhost:5433:

        docker run -d --name secure-user-test-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=secure_user_test_db -p 5433:5432 postgres:16

3. Run the test suite with coverage:

        pytest tests/ -v --cov=app --cov-report=term-missing --cov-fail-under=90

All 36 tests should pass with 100% coverage of application code (app/main.py is excluded via .coveragerc since it's an entrypoint, not testable logic).

To run only the new Calculation-related tests:

        pytest tests/test_calculation_factory.py tests/test_calculation_integration.py -v

## CI/CD Pipeline

Every push to main triggers a GitHub Actions workflow (.github/workflows/ci-cd.yml) that:

1. Spins up a PostgreSQL 16 service container.
2. Installs dependencies and runs the full test suite with a 90% coverage gate.
3. On success, builds a Docker image and pushes it to Docker Hub, tagged with both latest and the commit SHA.

## Docker Hub

The application image is published here:

https://hub.docker.com/r/is218/secure-user-model

Pull and run it locally:

        docker pull is218/secure-user-model:latest
        docker run -p 8000:8000 -e DATABASE_URL="postgresql://postgres:postgres@host.docker.internal:5432/secure_user_db" is218/secure-user-model:latest

Note (Apple Silicon): the image is built for linux/amd64. On M-series Macs, add --platform linux/amd64 to both docker pull and docker run to run it via emulation.

Once running, visit http://localhost:8000/docs for the interactive API documentation.

## Learning Outcomes Addressed

- CLO3: Automated testing with pytest (unit + integration).
- CLO4: GitHub Actions CI, automating tests and Docker builds.
- CLO9: Containerization with Docker.
- CLO11: SQLAlchemy integration with PostgreSQL.
- CLO12: JSON validation/serialization with Pydantic.
- CLO13: Secure password hashing with bcrypt; no plain-text credentials ever stored or logged.
