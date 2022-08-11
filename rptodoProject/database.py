"""This module deals with interacting with the rptodo database."""

import os
import json
import random
from rptodoProject import toDo, exceptions, config
import logging
from typing import Dict


class Database():
    def __init__(self):
        self._config = config.Config()
        self._database_abs_path = ""
        self._database_parent_dir = ""
        self._discover_existing_database()

    def _discover_existing_database(self) -> None:
        """Get the database absolute path from self._config
            - If no error is raised from self._config.get_database_location(), there is either
                an existing database at the location specified or there isn't. If there is, nothing 
                needs to be done. If there isn't an existing database, it is assumed either the database
                has not yet been created or was deleted, in which case it needs to be initialized.
        """
        logging.info("Searching for existing database...")
        self._database_abs_path = self._config.get_database_location()
        self._database_parent_dir = os.path.dirname(self._database_abs_path)
        if not self._db_exists():
            self._create_database()

    def clear(self) -> None:
        """Clear all contents in the Database.

        Note: Even if there is no database at the default location (ie. discover_existing_database fails)
        this method will create a blank database at _DATABASE_ABS_PATH

        Raises:
            DBWriteError: Unable to clear the database.
        """
        try:
            self._write_to_database({})

        except exceptions.DBWriteError as e:
            raise exceptions.DBClearError(f"Something went wrong clearing the database --> {e}")

    def add_to_do(self, todo: toDo.toDo) -> bool:
        """Write the to-do to the database.

        Args:
            contents_to_write (toDo.toDo): Object containing the to-do details.

        Returns:
            bool: True if contents were successfully written.

        Raises:
            DBWriteError: Unable to update the database with the provided to-do.
        """ 
        db_contents = self._get_db_contents()
        todo_id = self._get_unique_todo_id()
        db_contents[todo_id] = vars(todo)  # update existing contents with todo
        self._write_to_database(db_contents)
        logging.info("Successfully added to-do to database!")
        return True

    def get_database_contents(self) -> Dict[str, str]:
        """Present contents of database to the user.

        Returns:
            bool: True if contents were successfully read and displayed.
        """
        return self._get_db_contents()

    def _db_exists(self) -> bool:
        """Return True if database exists at _DATABASE_ABS_PATH"""
        if os.path.isfile(self._database_abs_path):
            return True
        return False

    def _create_database(self) -> None:
        """Ensure that a Database directory exists and create a blank _database.json file at self._database_abs_path."""
        if not self._db_directory_exists():
            self._create_db_directory()
        try:
            self._write_to_database({})
        except exceptions.DBWriteError:
            logging.error("Something went wrong creating the database!")
            raise

    def _write_to_database(self, contents_to_write: Dict[str, str]) -> None: 
        """Write contents_to_write to database.

        Raises:
            DBWriteError: Unable to write to the database.
        """
        try:
            with open(self._database_abs_path, 'w') as db:
                db.write(json.dumps(contents_to_write, indent=4))
        except Exception as e:
            raise exceptions.DBWriteError(f"The following occured writing <{contents_to_write}> to database --> {e}")

    def _db_directory_exists(self) -> bool:
        """Return True if self._database_parent_dir exists"""
        if os.path.exists(self._database_parent_dir):
            return True
        return False

    def _create_db_directory(self) -> None:
        """Create a directory to hold rptodo database at _APP_DIR\\Database"""
        try:
            os.mkdir(self._database_parent_dir)
        except OSError:
            logging.error("Something went wrong trying to create the database directory!")
            raise

    def _get_unique_todo_id(self) -> str:
        """Return a random 6 digit string to represent the to-do's id in the database."""
        return str(random.randint(1, 999999)).zfill(6)

    def _get_db_contents(self) -> Dict[str, str]:
        """Return Dict containing contents in the database.

        Raises:
            exceptions.DBReadError: Could not deserialize json objects.
            exceptions.FileError: Could not find database file."""
        try:
            with open(self._database_abs_path, "r") as db:
                return json.load(db)
        except json.JSONDecodeError:
            raise exceptions.DBReadError("Could not read database - suspect database is corrupt")
        except FileNotFoundError:
            raise exceptions.FileError(f"Could not locate database at {self._database_abs_path}")
