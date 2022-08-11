import sys
import argparse
from rptodoProject import rptodo, render
import logging
import traceback
from typing import Generator


def initialize_logger() -> None:
    """Initialize ToDo app's logger."""
    logging.basicConfig(handlers=[
                            logging.FileHandler("rptodo.log"),
                        ],
                        level=logging.INFO
                        )


def get_parsed_args() -> argparse.Namespace:
    """Parse the command-line arguments provided to the script"""
    cmd_line_parser = initialize_parser()
    return cmd_line_parser.parse_args()


def get_to_do_information() -> Generator:
    for to_do_attribute in ["description", "priority (1 - 5)"]:
        yield input(f"Please enter the to-do's {to_do_attribute}: ")


def initialize_parser() -> argparse.ArgumentParser:
    """Initialize parser with the following options:

    add	--> Adds a new to-do to the database
    list --> Lists all the to-dos in the database
    complete TODO_ID --> Completes a to-do by setting it as done using its ID
    remove TODO_ID --> Removes a to-do from the database using its ID
    clear --> Removes all the to-dos by clearing the database
    """
    cmd_line_parser = argparse.ArgumentParser(description="Application for managing ToDo tasks")
    cmd_line_parser.add_argument('--add', help="Clear all ToDos from the database.", action="store_true")
    cmd_line_parser.add_argument('--list', help="List all ToDos in the database.", action="store_true")
    cmd_line_parser.add_argument('--clear', help="Clear all ToDos from the database.", action="store_true")
    return cmd_line_parser


def main() -> None:
    initialize_logger()
    parsed_args = get_parsed_args()
    db_controller = rptodo.DBController()

    try:
        if parsed_args.add:
            to_do_description, to_do_priority = get_to_do_information()
            status_msg = db_controller.add_to_do(to_do_description, to_do_priority)
            render.Renderer.print_to_user(status_msg)
        elif parsed_args.list:
            db_contents = db_controller.get_database_contents()
            render.Renderer.render_database_contents(db_contents)
        elif parsed_args.clear:
            status_msg = db_controller.clear_database()
            render.Renderer.print_to_user(status_msg)

    except Exception as e:
        # This umbrella statement will catch all errors produced by controller, view and database
        logging.error(traceback.format_exc())
        render.Renderer.print_to_user(f"[ ERROR ] {e}")
        sys.exit(99)


if __name__ == "__main__":
    main()
