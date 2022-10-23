from typing import Dict, Generator
from rptodoProject import database
from rptodoProject.toDo import toDo


class DBController:
    """Database controller class for MVC architecture."""

    def __init__(self):
        self.db = database.Database()

    def add_to_do(self) -> bool:
        """Create a ToDo and add it to the database.

        Args:
            to_do_description (str): A string describing what needs to be done.
            to_do_priority (str): A string describing the priority of the ToDo.

        Returns:
            True if todo was added to the database.
        """
        to_do_description, to_do_priority = self._get_to_do_information()
        todo = toDo(to_do_description, to_do_priority)
        self.db.add_to_do(todo)
        return True

    def get_database_contents(self) -> Dict[str, Dict[str, str]]:
        """Return a Dict containing the database contents."""
        return self.db.get_database_contents()

    def remove_to_do(self) -> bool:
        """Return True if todo with corresponding to_do_id was removed from the database."""
        to_do_id = self._get_to_do_id()
        return self.db.remove_to_do(to_do_id)

    def complete_to_do(self) -> bool:
        """Return True if todo with corresponding to_do_id was updated to be complete in the database."""
        to_do_id = self._get_to_do_id()
        return self.db.complete_to_do(to_do_id)

    def clear_database(self) -> bool:
        """Remove all entries in the database and reset it with and empty Dict.

        This function will prompt the user before executing clear option. If user
        enters anything besides "yes", the program will exit.

        Raises:
            ValueError: Anything other that "yes" was entered at prompt.

        Returns:
            True if database was cleared successfully.
        """
        clear_confirmation = input("Type 'yes' to clear database: \n")
        if clear_confirmation == "yes":
            self.db.clear()
            return True
        else:
            raise ValueError("User aborted the clear operation")

    def _get_to_do_information(self) -> Generator:
        for to_do_attribute in ["description", "priority (1 - 5)"]:
            yield input(f"Please enter the to-do's {to_do_attribute}: ")

    def _get_to_do_id(self) -> str:
        """Retrieve ID from user corresponding to the to-do to be removed or completed."""
        return input("Please enter the to-do's ID: ")
