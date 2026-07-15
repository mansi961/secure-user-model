
# Secure User Model

A FastAPI application demonstrating secure user authentication and a calculation

engine, built with SQLAlchemy, Pydantic, and a factory-pattern design for

extensible arithmetic operations. Includes a full CI/CD pipeline via GitHub

Actions that runs the test suite and pushes a Docker image to Docker Hub on

every successful build.

## Features

- **User model** — secure registration with bcrypt password hashing (never

  stores plain-text passwords).

- **Calculation model** — stores two operands (`a`, `b`), an operation type

  (`Add`, `Sub`, `Multiply`, `Divide`), and the computed result, linked to a

  user via foreign key.

- **Factory pattern** — `CalculationFactory` selects and runs the correct

  operation class based on the requested type, decoupling operation logic

  from the model.

- **Pydantic schemas** — `CalculationCreate` validates incoming data

  (rejects invalid operation types and division by zero); `CalculationRead`

  serializes output data.

- **100% test coverage** — unit tests for the factory and schema validation,

  plus integration tests against a real PostgreSQL database.

## Project Structure

cat README.md

eof
