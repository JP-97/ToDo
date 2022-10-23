import sys
import argparse
from rptodoProject import rptodo, render
import logging
import traceback


def initialize_logger() -> None:
    """Initialize ToDo app's logger."""
    logging.basicConfig(
        handlers=[
            logging.FileHandler("rptodo.log"),
        ],
        level=logging.INFO,
    )


def get_parsed_args() -> argparse.Namespace:
    """Parse the command-line arguments provided to the script"""
    cmd_line_parser = initialize_parser()
    return cmd_line_parser.parse_args()


def initialize_parser() -> argparse.ArgumentParser:
    """Initialize parser with the following options:

    add	--> Adds a new to-do to the database
    list --> Lists all the to-dos in the database
    complete TODO_ID --> Completes a to-do by setting it as done using its ID
    remove TODO_ID --> Removes a to-do from the database using its ID
    clear --> Removes all the to-dos by clearing the database
    """
    cmd_line_parser = argparse.ArgumentParser(description="Application for managing ToDo tasks")
    cmd_line_parser.add_argument("--add", help="Clear all ToDos from the database.", action="store_true")
    cmd_line_parser.add_argument("--list", help="List all ToDos in the database.", action="store_true")
    cmd_line_parser.add_argument("--remove", help="Remove a ToDo by providing the ID.", action="store_true")
    cmd_line_parser.add_argument("--complete", help="Complete a ToDo by providing the ID.", action="store_true")
    cmd_line_parser.add_argument("--clear", help="Clear all ToDos from the database.", action="store_true")
    return cmd_line_parser


def main() -> None:
    initialize_logger()
    parsed_args = get_parsed_args()
    db_controller = rptodo.DBController()

    try:
        if parsed_args.add:
            db_controller.add_to_do()
            render.Renderer.print_to_user("Successfully added todo to the database!")

        elif parsed_args.list:
            db_contents = db_controller.get_database_contents()
            render.Renderer.render_database_contents(db_contents)

        elif parsed_args.remove:
            db_controller.remove_to_do()
            render.Renderer.print_to_user("Successfully removed specified todo from the database!")

        elif parsed_args.complete:
            db_controller.complete_to_do()
            render.Renderer.print_to_user("Successfully set Completed status for specified todo")

        elif parsed_args.clear:
            db_controller.clear_database()
            render.Renderer.print_to_user("Successfully cleared the database!")

    except Exception as e:
        # catch all errors produced by controller, view and database
        logging.error(traceback.format_exc())
        render.Renderer.print_to_user(f"[ ERROR ] {e}")
        sys.exit(99)


if __name__ == "__main__":
    main()
