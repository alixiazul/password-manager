import boto3
from botocore.exceptions import ClientError
import os


def display_menu():
    valid_inputs = ["e", "r", "d", "l", "x"]
    user_input = "a"
    while user_input not in valid_inputs:
        print("Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:")
        user_input = input()
        sm_client = boto3.client("secretsmanager")
        if user_input not in valid_inputs:
            print("Invalid input.", end="")

        if user_input == "e":
            store_secret(sm_client)
        elif user_input == "r":
            print()
        elif user_input == "d":
            print()
        elif user_input == "l":
            number_of_secrets = 0
            print(f"{number_of_secrets} secret(s) available")


def store_secret(sm_client):
    print("Secret identifier:")
    secret_identifier = input()

    for i in secret_identifier:
        if i.lower() not in "abcdefghijklmnopgrstuvwxyz1234567890-_":
            print("Invalid Secret identifier.")
            return 0

    print("UserId:")
    user_id = input()

    print("Password:")
    user_password = input()
    #  can not have these chars /_+=.@-
    # dashes are fine and also unser scores
    try:
        sm_client = boto3.client("secretsmanager")
        res = sm_client.create_secret(
            Name=secret_identifier,
            SecretString='{"username":'
            + user_id
            + ',"password":'
            + user_password
            + "}",
        )
    except ClientError as e:
        print(e)

    # print(res)

    # is everyting ok
    print("Secret saved.")


def list_secrets(sm_client):
    res = sm_client.list_secrets()


def retrieve_secrets(sm_client):
    pass


def delete_secret(sm_client):
    pass


if __name__ == "__main__":
    display_menu()
