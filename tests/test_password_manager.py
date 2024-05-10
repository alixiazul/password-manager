from src.password_manager import *
from unittest.mock import patch
from moto import mock_aws
import boto3
import pytest
import io
import os


@pytest.fixture(scope="function")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def sm_client():
    with mock_aws():
        yield boto3.client("secretsmanager")


class TestDisplayMenu:
    def test_invalid_input(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("builtins.input", side_effect=["q", "x"]):
                display_menu()
        assert "Invalid input." in fake_out.getvalue()

    # remake this test with mock moto
    def test_display_number_or_secrets(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("builtins.input", side_effect=["l", "x"]):
                display_menu()
        assert "0 secret(s) available" in fake_out.getvalue()

    def test_store_secret_message(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["e", "Missile_Launch_Codes", "bidenj", "Pa55word", "x"],
            ):
                display_menu()

        assert "Secret saved." in fake_out.getvalue()

    def test_list_correct_number_of_secrets_when_one_secret_exists(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=[
                    "e",
                    "Missile_Launch_Codes",
                    "bidenj",
                    "Pa55word",
                    "l",
                    "x",
                ],
            ):
                display_menu()

        assert "1 secret(s) available" in fake_out.getvalue()

    def test_retreaval_password(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=[
                    "e",
                    "Missile_Launch_Codes",
                    "bidenj",
                    "Pa55word",
                    "r",
                    "Missile_Launch_Codes",
                    "x",
                ],
            ):
                display_menu()

        assert "Secrets stored in local file secrets.txt" in fake_out.getvalue()
        with open("output/secrets.txt") as f:
            line = f.readline()
            assert line == "UserId: bidenj\n"
            line = f.readline()
            assert line == "Password: Pa55word"

    def test_delete_password(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=[
                    "e",
                    "Missile_Launch_Codes",
                    "bidenj",
                    "Pa55word",
                    "d",
                    "Missile_Launch_Codes",
                    "x",
                ],
            ):
                display_menu()

        assert "Specify secret to delete:" in fake_out.getvalue()
        assert "Deleted" in fake_out.getvalue()
        secrets_list = [
            secret["Name"] for secret in sm_client.list_secrets()["SecretList"]
        ]
        assert "Missile_Launch_Codes" not in secrets_list

    def test_goodbye_message(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["x"],
            ):
                display_menu()

        assert "Your secrets are saved with me! Bye!" in fake_out.getvalue()


class TestStoreSecret:
    def test_asks_for_secret_information(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["Missile_Launch_Codes", "bidenj", "Pa55word"],
            ):
                store_secret(sm_client)

        res_list = fake_out.getvalue().split("\n")

        # is this stops working it might be -1
        assert "Secret saved." in res_list

    def test_saves_the_secret(self, sm_client):
        with patch(
            "builtins.input",
            side_effect=["Missile_Launch_Codes", "bidenj", "Pa55word"],
        ):
            store_secret(sm_client)
        with patch(
            "builtins.input",
            side_effect=["Missile_Launch_Codes2", "xi", "Pa55wordxi"],
        ):
            store_secret(sm_client)

        secret_list = [
            secret["Name"] for secret in sm_client.list_secrets()["SecretList"]
        ]
        assert "Missile_Launch_Codes" in secret_list
        assert "Missile_Launch_Codes2" in secret_list

    def test_secret_is_saved_correctly(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["Missile_Launch_Codes", "bidenj", "Pa55word"],
            ):
                store_secret(sm_client)

        secret_string = sm_client.get_secret_value(SecretId="Missile_Launch_Codes")

        assert (
            '{"username":bidenj,"password":Pa55word}' in secret_string["SecretString"]
        )

    def test_secret_name_invalid_returns_warning_message(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["Missile_L aunch_Codes", "bidenj", "Pa55word"],
            ):
                store_secret(sm_client)

        res_list = fake_out.getvalue().split("\n")

        assert "Invalid Secret identifier." in res_list

    def test_secret_name_already_exists(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["Missile_Launch_Codes", "bidenj", "Pa55word"],
            ):
                store_secret(sm_client)
            with patch(
                "builtins.input",
                side_effect=["Missile_Launch_Codes", "bidenj", "Pa55word"],
            ):
                store_secret(sm_client)

        assert "Secret identifier already exists." in fake_out.getvalue()


class TestListSecrets:
    def test_no_secrets(self, sm_client):
        assert list_secrets(sm_client) == 0

    def test_one_secrets_saved(self, sm_client):
        with patch(
            "builtins.input",
            side_effect=["Missile_Launch_Codes", "bidenj", "Pa55word"],
        ):
            store_secret(sm_client)
        assert list_secrets(sm_client) == 1


class TestRetrieveSecrets:
    def test_retrieve_secrets(self, sm_client):
        with patch(
            "builtins.input",
            side_effect=["Missile_Launch_Codes", "bidenj", "Pa55word"],
        ):
            store_secret(sm_client)

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["Missile_Launch_Codes"],
            ):
                retrieve_secrets(sm_client)

        assert "Specify secret to retrieve:" in fake_out.getvalue()
        assert "Secrets stored in local file secrets.txt" in fake_out.getvalue()
        with open("output/secrets.txt") as f:
            line = f.readline()
            assert line == "UserId: bidenj\n"
            line = f.readline()
            assert line == "Password: Pa55word"

    def test_secrets_do_not_exist(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["Missile"],
            ):
                retrieve_secrets(sm_client)

        assert "Specify secret to retrieve:" in fake_out.getvalue()
        assert "Invalid secret" in fake_out.getvalue()


class TestDeleteSecret:
    def test_deletes_secret(self, sm_client):
        with patch(
            "builtins.input",
            side_effect=["Missile_Launch_Codes", "bidenj", "Pa55word"],
        ):
            store_secret(sm_client)

        secrets_list = [
            secret["Name"] for secret in sm_client.list_secrets()["SecretList"]
        ]

        assert "Missile_Launch_Codes" in secrets_list

        with patch(
            "builtins.input",
            side_effect=["Missile_Launch_Codes"],
        ):

            delete_secret(sm_client)

        secrets_list = [
            secret["Name"] for secret in sm_client.list_secrets()["SecretList"]
        ]
        assert "Missile_Launch_Codes" not in secrets_list

    def test_delete_non_existing_secret(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["Missile_Launch_Codes"],
            ):
                delete_secret(sm_client)

        assert "There are no secrets with that name." in fake_out.getvalue()
