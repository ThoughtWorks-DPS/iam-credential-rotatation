from io import StringIO
from unittest.mock import patch, mock_open
import pytest
import click
from utils import output_results, validate_user_count


def test_user_count_is_in_valid_range():
    result = validate_user_count(5)
    assert result == 5

def test_user_count_is_zero():
    with pytest.raises(click.UsageError) as _:
          _ = validate_user_count(0)

def test_user_count_is_too_high():
    with pytest.raises(click.UsageError) as _:
          _ = validate_user_count(21)

def test_output_results():
    results = "testcredentials"
    with patch('sys.stdout', new = StringIO()) as results_out:
        output_results(results, '')
    assert results_out.getvalue().rstrip('\n') == results

def test_output_results_to_file():
    results = "testcredentials"
    open_mock = mock_open()
    with patch("builtins.open", open_mock, create=True):
        output_results(results, 'testfile')

    open_mock.assert_called_with("testfile", "w", encoding="utf8")
    open_mock.return_value.write.assert_called_once_with(results)

