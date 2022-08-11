"""This module will be used as the view component of the to-do app's MVC architecture."""
from typing import Dict


class Renderer:

    @staticmethod
    def render_database_contents(database_contents: Dict[str, str]) -> None:
        """Print formatted database contents to stdout.

        Args:
            database_contents (Dict[str, str]): Database contents as Python Dict
        """
        if not database_contents:
            print("Database is empty! Try using --add to add a to-do.")
            return

        sorted_db_contents = _get_sorted_db_contents(database_contents)
        print(f"{'TO-DO ID':<20}\t{'PRIORITY':<20}\t{'DESCRIPTION':<50}")
        for to_do_id, to_do_dict in sorted_db_contents.items():
            print(f"{to_do_id:<20}\t{to_do_dict['_priority']:<20}\t{to_do_dict['_description']:<50}")

    @staticmethod
    def print_to_user(msg_to_render: str) -> None:
        """Print msg_to_render to stdout.

        Args:
            msg_to_render (str): Message that requires printing.
        """
        print(msg_to_render)


def _get_sorted_db_contents(database_contents: Dict[str, str]) -> Dict[str, str]:
    """Sort the database contents in from lowest to higest priority.

    Returns:
        Dict[str, str]: Sorted database contents based on priority.
    """
    return dict(sorted(database_contents.items(), key=lambda data: data[1]['_priority']))  # data[1] -> represents each to-do's dict
