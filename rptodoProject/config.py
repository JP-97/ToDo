from rptodoProject import exceptions
import os
import logging

class Config:
    """This module provides configuration for ToDo database"""

    def __init__(self) -> None:
        self._app_dir = os.path.dirname(__file__)
        self._config_dir = os.path.join(self._app_dir,"Configs")
        self._config_path_default = os.path.join(self._config_dir, "Config.ini")

    def create_db_config(self) -> str:
        """Return Path-like string holding the absolute path to the app's config file.
        
        If Config.ini doesn't already exist in <parent_dir>/Configs, it is created. 
        """
        self._create_db_config_file()
        logging.info(f"Config file location: {self._config_path_default}")
        return self._config_path_default

    def get_config_file_path(self) -> str:
        """Return Path-like string containing the path to the database's config file.
        
        Raises:
            FileNotFoundError: Database's config file can't be found. 
        """
        if self._config_directory_exists():
            logging.info(f"Found Database config file at {self._config_path_default}")
            return self._config_path_default
        else:
            raise FileNotFoundError(f"Database config file could not be found at {self._config_path_default}")

    def _create_db_config_file(self) -> None:
        """If Config.ini does not exist, it is created."""
        try:
            if not self._config_directory_exists():
                self._create_config_directory()
            
            if not self._config_file_exists():
                self._create_config_file()

        except exceptions.DirError:
            print('Error: Config directory could not be created!')

        except exceptions.FileError:
            print('Error: Could not create Config.ini in Config directory')

    def _create_config_directory(self) -> None:
        """Create the configuration file directory for the database.
        
        Raises:
            DirError: An error occurred creating the directory."""
        try:
            os.mkdir(self._config_dir)
        except OSError:
            raise exceptions.DirError

    def _create_config_file(self) -> None:
        try:
            with open(self._config_path_default, "x"):
                pass
        except OSError:
            raise exceptions.FileError

    def _config_directory_exists(self) -> bool:
        """Return True if <parent_dir>/Configs directory exists."""
        if os.path.isdir(self._config_dir):
            logging.info(f'config directory ({self._config_dir}) already exists!')
            return True
        return False

    def _config_file_exists(self) -> bool:
        """Return True if <parent_dir>/Configs/Config.ini file exists."""
        if os.path.isfile(self._config_path_default):
            return True
        return False