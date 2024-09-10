# Contributing to ImmutableNewsAPI

We're excited that you're interested in contributing to ImmutableNewsAPI! This document provides guidelines for contributing to the project. By participating in this project, you agree to abide by its terms.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally: `git clone https://github.com/tobalo/immutable-news-api.git`
3. Create a new branch for your feature or bug fix: `git checkout -b your-feature-name`
4. Make your changes and commit them with a clear commit message.
5. Push your changes to your fork: `git push origin your-feature-name`
6. Submit a pull request to the main repository.

## Development Environment

1. Ensure you have Python 3.12 installed.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in the necessary environment variables.

## Running Tests

Before submitting a pull request, please ensure all tests pass:

1. Run Python tests: `python -m pytest tests/`
2. Run the API test script: `./tests/test-news-endpoint.sh`

## Coding Standards

- Follow PEP 8 style guide for Python code.
- Write clear, readable, and well-documented code.
- Include docstrings for new functions and classes.
- Add type hints where appropriate.

## Pull Request Process

1. Ensure your code adheres to the project's coding standards.
2. Update the README.md with details of changes to the interface, if applicable.
3. Add or update tests as necessary.
4. Ensure the test suite passes before submitting your pull request.
5. Update the CHANGELOG.md with details of changes.
6. Your pull request will be reviewed by maintainers, who may request changes or ask questions.

## Reporting Bugs

- Use the GitHub Issues page to report bugs.
- Describe the bug in detail, including steps to reproduce.
- Include information about your environment (OS, Python version, etc.).

## Feature Requests

We welcome feature requests! Please submit them as GitHub Issues and include:

- A clear description of the feature.
- The motivation behind the feature.
- Possible implementation details (if you have ideas).

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

Thank you for contributing to ImmutableNewsAPI!
