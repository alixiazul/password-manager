# Password Manager CLI

## Overview

This project is a simple command-line application to store and retrieve passwords using AWS Secrets Manager. Accessing your AWS account with your Access Key ID and Secret Key will be considered sufficient authorization to retrieve the passwords.

## Features

The application allows you to:

- Store a user ID and password as a secret in Secrets Manager.
- List all the stored secrets.
- Retrieve a secret - the resulting user ID and password will be stored in a file instead of being printed out.
- Delete a secret.

## Skills

- Interact with AWS services programmatically in a Python script using Boto3.
- Use mocks to test Python code that uses Boto3.
- Test for exceptions in Boto3.
- Explore testing with the Moto library.
- Use TDD to develop functionality.

## Usage

Create Python interpreter environment: 
```sh
make create-environment
```

Build the environment requirements:
```sh
make requirements
```

Set up development requirements (bandit, safety, black):
```sh
make dev-setup
```

Run the black code check, unit tests, coverage check:
```sh
make run-checks
```