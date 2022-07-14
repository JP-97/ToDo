"""This module deals with interacting with the rptodo database."""

import configparser
import os
import json
from rptodoProject import config
from rptodoProject import exceptions
import logging


class Database():

    APP_DIR = os.path.dirname(__file__)
    DATABASE_NAME = '_database.json'
    DATABASE_ABS_PATH = os.path.join(APP_DIR,
                                     "Database",
                                      DATABASE_NAME)

    def __init__(self, config_path):
        self.config_path = config_path
        self._initialize_database()
        
    def _initialize_database(self) -> None :
        """Ensure that a database exists at DEFAULT_DATABASE_NAME.
        
        If no database exists, a blank database will be created."""
        if not self._db_exists():
            self._create_database()
            self._update_config_file() 
            logging.info(f"Initialized database at {Database.DATABASE_ABS_PATH}")
        else:
            # If the database already exists, don't want to overwrite the contents with empty list
            self._log_database_location()

    def _update_config_file(self) -> None:
        """Update the config file to contain the absolute path to the database."""
        db_config = configparser.ConfigParser()
        db_config["DEFAULT"] = {"database": Database.DATABASE_ABS_PATH}
        try:
            with open(self.config_path, 'w') as config_file:
                db_config.write(config_file)
            logging.info("Updated config file with db path.")
        except Exception:
            logging.error("Could not update config file with DB path!")
            raise exceptions.DirError()

    def _log_database_location(self) -> None:
        """Log the database location saved in the database variable under DEFAULT."""
        parser = configparser.ConfigParser()
        parser.read(self.config_path)
        logging.info(f"Database is stored at: {parser['DEFAULT']['database']}")

    def _db_exists(self) -> bool:
        """Return True if database exists at DATABASE_ABS_PATH"""
        if os.path.isfile(Database.DATABASE_ABS_PATH):
            return True
        return False

    def _create_database(self) -> None:
        """Create the rptodo database at DATABASE_ABS_PATH"""
        if not self._db_directory_exists():
            self._create_db_directory()
        try:
            with open(Database.DATABASE_ABS_PATH, 'w') as db:
                db.write('[]')
        except OSError:
            logging.error("Something went wrong creating the database!")
            raise

    def _db_directory_exists(self) -> bool:
        """Return True if APP_DIR\\Database exists"""
        db_dir = os.path.join(Database.APP_DIR, "Database")
        if os.path.exists(db_dir):
            return True
        return False

    def _create_db_directory(self) -> bool:
        """Create a directory to hold rptodo database at APP_DIR\\Database"""
        db_dir = os.path.join(Database.APP_DIR, "Database")
        try:
            os.mkdir(db_dir)
        except OSError:
            logging.error("Something went wrong trying to create the database directory!")
            raise

    def clear(self) -> None:
        """Clear all contents in the Database."""
        try:
            with open(Database.DATABASE_ABS_PATH, 'w') as db:
                db.write('[]')
        except OSError:
            logging.error("Something went wrong clearing the database!")
            raise

    def write_to_database(self, contents_to_write: str) -> bool:
        """Write the contents to the database.

        Args:
            contents_to_write (str): Serializable JSON to be written to the database.

        Returns:
            bool: True if contents were successfully written.
        """
        pass