import pytest
import pathlib
import os
import configparser

from typing import Generator, Dict

from rptodoProject.config import Config


@pytest.fixture(autouse=True)
def adjust_config_file_default_paths(tmp_path, monkeypatch) -> Generator:
    # Mock Config class variables to point to tmp_path
    config_dir_abs_path = os.path.join(tmp_path, "Configs")
    monkeypatch.setattr(Config, "_APP_DIR", tmp_path)
    monkeypatch.setattr(Config, "_CONFIG_DIR", config_dir_abs_path)
    monkeypatch.setattr(Config, "_CONFIG_PATH_DEFAULT", os.path.join(config_dir_abs_path, "Config.ini"))
    yield


@pytest.fixture
def mocked_config_file(tmp_path: pathlib.WindowsPath) -> pathlib.PureWindowsPath:
    config_file_directory = tmp_path / "Configs"
    config_file_directory.mkdir()
    config_file_abs_path = config_file_directory / "Config.ini"
    return config_file_abs_path


def update_config_file_DATABASE(config_file_location: str, data_to_add: Dict[str, str]) -> None:
    """Update the provided config file's DATABASE section with data_to_add"""
    configurer = configparser.ConfigParser()
    configurer["DATABASE"] = data_to_add

    with open(config_file_location, "w") as config_file:
        configurer.write(config_file)


def test_get_database_location(mocked_config_file) -> None:
    """Ensure that the correct value is returned from the Config.ini file"""
    # Create a config file and add DatabasePath entry (mock creation of database)
    database_file_abs_path = mocked_config_file.parent.parent / "Database" / "_database.json"
    update_config_file_DATABASE(mocked_config_file, {"DatabasePath": database_file_abs_path})

    # Ensure Config object returns the mocked database path in tmp_path
    config = Config()
    assert config.get_database_location() == str(database_file_abs_path)


def test_get_database_location_raises_error_for_corrupt_config_file(mocked_config_file) -> None:
    update_config_file_DATABASE(mocked_config_file, {"dummy_key": "dummy_path"})

    config = Config()

    with pytest.raises(RuntimeError):
        config.get_database_location()


def test_create_db_config_file_no_Configs_dir_or_Config_file(tmp_path: pathlib.WindowsPath) -> None:
    """Ensure that Config.ini is created inside Configs directory if _APP_DIR is empty."""
    config_dir_abs_path = os.path.join(tmp_path, "Configs")

    # Instantiate instance of Config such that _discover_existing_db_config runs
    _ = Config()

    # Assert that Configs dir and Config.ini files are created in correct location
    assert os.path.isdir(config_dir_abs_path)
    assert os.path.isfile(os.path.join(config_dir_abs_path, "Config.ini"))


def test_create_db_config_file_Config_dir_but_no_Config_file(tmp_path: pathlib.WindowsPath) -> None:
    config_file_directory = tmp_path / "Configs"
    config_file_directory.mkdir()
    assert os.path.isdir(config_file_directory)
    assert not os.path.isfile(os.path.join(config_file_directory, "Config.ini"))

    # Instantiate instance of Config such that _discover_existing_db_config runs
    _ = Config()

    # Assert that Config.ini is created in already present Configs dir
    assert os.path.isfile(os.path.join(config_file_directory, "Config.ini"))
