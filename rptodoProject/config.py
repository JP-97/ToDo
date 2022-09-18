import configparser
import os
import logging

from rptodoProject import exceptions


class Config:
    """This establishes a config file for the to-do database."""

    _APP_DIR = os.path.dirname(__file__)
    _CONFIG_DIR = os.path.join(_APP_DIR, "Configs")
    _CONFIG_PATH_DEFAULT = os.path.join(_CONFIG_DIR, "Config.ini")
    _DATABASE_NAME = "_database.json"
    _DATABASE_ABS_PATH = os.path.join(_APP_DIR, "Database", _DATABASE_NAME)

    def __init__(self) -> None:
        self._config = configparser.ConfigParser()
        self._discover_existing_db_config()

    def get_database_location(self) -> str:
        """Return the database location specified in the config file."""
        try:
            self._config.read(Config._CONFIG_PATH_DEFAULT)
            return self._config["DATABASE"]["DatabasePath"]

        except KeyError:
            raise RuntimeError("Was not able to find DatabasePath key under DATABASE section in Config file")

    def _discover_existing_db_config(self) -> None:
        """Determine whether there is a database config file at the expected location (_CONFIG_PATH_DEFAULT)."""
        if self._config_file_exists():
            logging.info(f"Found Database config file at {Config._CONFIG_PATH_DEFAULT}")
        else:
            self._create_db_config_file()

    def _create_db_config_file(self) -> None:
        """If a database config file can't be found at the default location, create it.

        Note: As part of this creation, the DATABASE section in the config file will also
              be created with the DatabasePath key pointing to the _DATABASE_ABS_PATH.
        """
        if not self._config_directory_exists():
            self._create_config_directory()

        if not self._config_file_exists():
            self._create_config_file()

    def _create_config_directory(self) -> None:
        """Create the configuration file directory for the database.

        Raises:
            DirError: An error occurred creating the directory.
        """
        try:
            os.mkdir(Config._CONFIG_DIR)
        except OSError as e:
            raise exceptions.DirError(f"Config directory could not be created due to --> {e}")

    def _create_config_file(self) -> None:
        """Create a config file at the default location and insert DatabasePath information.

        Raises:
            FileError: An error occurs creating the database config file in the Configs directory.
        """
        try:
            self._config["DATABASE"] = {"DatabasePath": Config._DATABASE_ABS_PATH}
            with open(Config._CONFIG_PATH_DEFAULT, "w") as config:
                self._config.write(config)
            logging.info("Created database config file and added DatabasePath key")
        except OSError as e:
            raise exceptions.FileError(f"Database config file could not be created due to --> {e}")

    def _config_directory_exists(self) -> bool:
        """Return True if <parent_dir>/Configs directory exists."""
        if os.path.isdir(Config._CONFIG_DIR):
            logging.info(f"config directory ({Config._CONFIG_DIR}) already exists!")
            return True
        return False

    def _config_file_exists(self) -> bool:
        """Return True if <parent_dir>/Configs/Config.ini file exists."""
        if os.path.isfile(Config._CONFIG_PATH_DEFAULT):
            return True
        return False
