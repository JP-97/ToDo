"""This module will handle rptodo's cli."""

import sys
import argparse
from rptodoProject import rptodo
import logging
import traceback

def initialize_logger() -> None:
    """Initialize ToDo app's logger."""
    logging.basicConfig(handlers=[
                            logging.FileHandler("rptodo.log"),
                            logging.StreamHandler()
                        ],
                        level=logging.INFO
                        )

def get_parsed_args() -> argparse.Namespace:
    """Parse the command-line arguments provided to the script"""
    cmd_line_parser = initialize_parser()
    return cmd_line_parser.parse_args()

def initialize_parser() -> argparse.ArgumentParser:
    """Initialize parser with the following options:

    add DESCRIPTION	--> Adds a new to-do to the database with a description
    list --> Lists all the to-dos in the database
    complete TODO_ID --> Completes a to-do by setting it as done using its ID
    remove TODO_ID --> Removes a to-do from the database using its ID
    clear --> Removes all the to-dos by clearing the database
    """
    cmd_line_parser = argparse.ArgumentParser(description="Application for managing ToDo tasks")
    cmd_line_parser.add_argument('--clear', help="Clear all ToDos from the database.", action="store_true")
    return cmd_line_parser

def main() -> None:
    initialize_logger()
    parsed_args = get_parsed_args()
    db_controller = rptodo.DBController()

    try:
        db_controller.discover_existing_database()
        
        if parsed_args.clear:
           db_controller.clear_database()

    except Exception as e:
        logging.error(f"The following exception occured -> {e}")
        logging.error(traceback.format_exc())
        sys.exit(99)











    # if arguments['add']:
    #     priority = _validate_priority(arguments['<priority>'])
    #     db_controller.add(arguments['<name>'],arguments['<description>'],priority)

    # if arguments['list']:
    #     print('Your database contains the following toDos: \n')
    #     print(pprint.pformat(db_controller.list()),'\n')

    # if arguments['complete']:
    #     try:
    #         id = _validate_id(['<id>'])
    #     except ValueError:
    #         print("Could not convert id to int. Please provide valid integer.")
    #     else:
    #         db_controller.complete(id)

    # if arguments['remove']:
    #     try:
    #         id = _validate_id(int,arguments['<id>'])
    #     except (TypeError,ValueError):
    #         print("Could not convert id to int. Please provide valid integer.")
    #     else:
    #         db_controller.remove(id)

    # if arguments['clear']:
    #     confirmed = input("Are you sure you want to clear the database? (y/n)")
    #     if confirmed != "y":
    #         print("Aborting clear operation")
    #         sys.exit(126)
    #     db_controller.clear()

if __name__ == "__main__":
    main()