import pytest
from rptodoProject import cli


@pytest.fixture
def db_controller(mocker):
    db_controller_mock = mocker.Mock()
    mocker.patch("rptodoProject.rptodo.DBController.__new__", return_value=db_controller_mock)
    return db_controller_mock


@pytest.mark.parametrize(
    "command_line_option",
    ["--add", "--list", "--clear"]
)
def test_get_parsed_args(monkeypatch, command_line_option):
    """Validate that Namespace object is created as expected for each possible command line argument."""
    monkeypatch.setattr("sys.argv", ["todo", command_line_option])
    cmd_line_args = cli.get_parsed_args()
    assert getattr(cmd_line_args, command_line_option.strip("-")) 


def test_error_is_raised_for_invalid_argument(monkeypatch):
    monkeypatch.setattr("sys.argv", ["todo", "--dummy_option"])
    with pytest.raises(SystemExit):
        cli.get_parsed_args()


def test_add_to_do_is_called(db_controller, monkeypatch):
    monkeypatch.setattr("sys.argv", ["todo", "--add"])
    cli.main()
    db_controller.add_to_do.assert_called_once()


def test_complete_to_do_is_called(db_controller, monkeypatch):
    monkeypatch.setattr("sys.argv", ["todo", "--complete"])
    cli.main()
    db_controller.complete_to_do.assert_called_once()


def test_remove_to_do_is_called(db_controller, monkeypatch):
    monkeypatch.setattr("sys.argv", ["todo", "--remove"])
    cli.main()
    db_controller.remove_to_do.assert_called_once()