import json
import itertools
from rptodoProject import rptodo, database


class toDo():
    """Simple class to model todo object."""

    def __init__(self, name, description, priority):
        database_size = len(rptodo.DatabaseHandler(db_path=database.fetch_database_directory()).read_todos())

        self.name = name
        self.description = description
        self.priority = priority #TODO add logic to validate priority in this class!
        self.done = False
        self.id = id(self)
        self.db_index = database_size # account for 0 indexing done by lists
        self.dict = {self.name:
                    {'description':self.description,
                     'priority':self.priority,
                     'done_status':self.done,
                     'index':self.db_index,
                     'id':self.id}}

    def __str__(self):
        return json.dumps(self.dict)

    # def _validate_priority(priority):
    # """Return a priority value between 1 and 3."""
    
    # while True:
    #     try:
    #         priority = int(priority)
    #         _check_range(priority)
    #     except (ValueError, exceptions.RangeError):
    #         print('Please enter a priority between 1 and 3')
    #         priority = input('enter a new priority:\t')
    #     else:
    #         return priority

    # def _check_range(priority):
    # """Validate that the priority value provided is between 1 and 3."""

    # if priority not in range(1,4):
    #     raise exceptions.RangeError