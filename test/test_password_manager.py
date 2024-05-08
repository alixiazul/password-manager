from src.password_manager import display_menu
from unittest.mock import patch
import io


class TestDisplayMenu:
    def test_invalid_input(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            # with patch("builtins.input", return_value="q"):
            with patch("builtins.input", side_effect=["q", "x"]):
                display_menu()
        print(fake_out.getvalue())
        assert "Invalid input." == fake_out.getvalue()
