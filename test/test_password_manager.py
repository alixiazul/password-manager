from src.password_manager import display_menu
from unittest.mock import patch
from moto import mock_aws
import boto3
import pytest
import io
import os


@pytest.fixture(scope="class")
def aws_creds():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def sm_client():
    with mock_aws():
        yield boto3.client("secretsmanager")


class TestDisplayMenu:
    def test_invalid_input(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch("builtins.input", side_effect=["q", "x"]):
                display_menu()
        assert "Invalid input." in fake_out.getvalue()

    # remake this test with mock moto
    def test_display_number_or_secrets(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            # with patch("builtins.input", return_value="q"):
            with patch("builtins.input", side_effect=["l", "x"]):
                display_menu()
        assert "0 secret(s) available" in fake_out.getvalue()


class TestStoreSecret:
    def test_asks_for_secret_information(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["e", "Missile_Launch_Codes", "bidenj", "Pa55word", "x"],
            ):
                display_menu()

        res_list = fake_out.getvalue().split("\n")

        # is this stops working it might be -1
        assert "Secret saved." in res_list

    def test_saves_the_secret(self, sm_client):
        with patch(
            "builtins.input",
            side_effect=["e", "Missile_Launch_Codes", "bidenj", "Pa55word", "x"],
        ):
            display_menu()
        with patch(
            "builtins.input",
            side_effect=["e", "Missile_Launch_Codes2", "xi", "Pa55wordxi", "x"],
        ):
            display_menu()

        secret_list = [
            secret["Name"] for secret in sm_client.list_secrets()["SecretList"]
        ]
        assert "Missile_Launch_Codes" in secret_list
        assert "Missile_Launch_Codes2" in secret_list

    def test_secret_is_saved_correctly(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["e", "Missile_Launch_Codes", "bidenj", "Pa55word", "x"],
            ):
                display_menu()

        secret_string = sm_client.get_secret_value(SecretId="Missile_Launch_Codes")

        assert (
            '{"username":bidenj,"password":Pa55word}' in secret_string["SecretString"]
        )

    def test_secret_name_invalid_returns_warning_message(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["e", "Missile_L aunch_Codes", "bidenj", "Pa55word", "x"],
            ):
                display_menu()

        res_list = fake_out.getvalue().split("\n")

        assert "Invalid Secret identifier." in res_list

    def test_secret_name_already_exists(self, sm_client):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            with patch(
                "builtins.input",
                side_effect=["e", "Missile_Launch_Codes", "bidenj", "Pa55word", "x"],
            ):
                display_menu()
            with patch(
                "builtins.input",
                side_effect=["e", "Missile_Launch_Codes", "bidenj", "Pa55word", "x"],
            ):
                display_menu()

        assert "Secret identifier already exists." in fake_out.getvalue()

    # def test_(self, sm_client):
    #     res = sm_client.create_secret(
    #         Name="MyT_estSecret",
    #         SecretString='{"username":"test1","password":"this is just a test"}',
    #     )
    #     print(res)
    #     res = sm_client.list_secrets()
    #     print(res)
    #     # sm_client.put_secret_value("this is just a test")
    #     assert False
