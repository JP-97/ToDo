from typing import Dict
from rptodoProject import database
from rptodoProject.toDo import toDo


class DBController:
    """Database controller class for MVC architecture."""
    def __init__(self):
        self.db = database.Database()

    def add_to_do(self, to_do_description: str, to_do_priority: str) -> str:
        """Create a ToDo and add it to the database.

        Args:
            to_do_description (str): A string describing what needs to be done.
            to_do_priority (str): A string describing the priority of the ToDo.
        """
        todo = toDo(to_do_description, to_do_priority)
        self.db.add_to_do(todo)
        return "Successfully added to-do to the database!"

    def get_database_contents(self) -> Dict[str, str]:
        """Return a Dict containing the database contents."""
        return self.db.get_database_contents()

    def clear_database(self) -> str:
        """Remove all entries in the database and reset it with and empty Dict.

        This function will prompt the user before executing clear option. If user
        enters anything besides "yes", the program will exit.

        Raises:
            ValueError: Anything other that "yes" was entered at prompt.
        """
        clear_confirmation = input("Type 'yes' to clear database: \n")
        if clear_confirmation == "yes":
            self.db.clear()
            return "Successfully cleared the database!"
        else:
            raise ValueError("User aborted the clear operation")
