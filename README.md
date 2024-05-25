# Password Manager CLI

## Overview

This project is a simple command-line application to store and retrieve passwords using AWS Secrets Manager. Accessing your AWS account with your Access Key ID and Secret Key will be considered sufficient authorization to retrieve the passwords.

## Features

The application allows you to:

- Store a user ID and password as a secret in Secrets Manager.
- List all the stored secrets.
- Retrieve a secret - the resulting user ID and password will be stored in a file instead of being printed out.
- Delete a secret.

## Learning Objectives

- Know how to interact with AWS services programmatically in a Python script using Boto3.
- Be able to use mocks to test Python code that uses Boto3.
- Know how to test for exceptions in Boto3.
- Explore testing with the Moto library.
- Use TDD to develop functionality.

## Installation

To install this project, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/alixiazul/password-manager.git

2. Navigate to the project directory:
   cd password-manager-cli

3. Install the required dependencies:
   python password_manager.py

## Usage

To use this project, follow these steps:

1. Set up your AWS credentials. You can do this by configuring the AWS CLI or setting the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
2. Run the application:
    python password_manager.py
3. Follow the on-screen prompts to store, list, retrieve, or delete secrets.
