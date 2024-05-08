import logging
import boto3
from botocore.exceptions import ClientError
import os


def display_menu():
    valid_inputs = ["e", "r", "d", "x"]
    user_input = "a"
    while user_input not in valid_inputs:
        user_input = input(
            "Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:"
        )
        if user_input not in valid_inputs:
            print("Invalid input.", end="")


if __name__ == "__main__":
    display_menu()
