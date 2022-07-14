"""This module will be used as the controller provided to the view."""
import json
from typing import List,Dict
from rptodoProject import config, database
from rptodoProject.toDo import toDo
import logging

class DatabaseHandler:
    def __init__(self, db_path=None):
        self.db_path = db_path
    
    def read_todos(self):
        """Read all of the existing todos from the database.
        
        Returns:
            A list of dicts (toDo) as shown below:
        [
            {
            "To_do_name":{"description":"some description"},
                         {"priority":some number},
                         {"done":done_status},
                         {"id":todo_id}
            },
            ...
        ]
        """
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
                
        except OSError:
            print('Something went wrong trying to access the database!')
        except json.JSONDecodeError:
            print('Something went wrong when trying to read the database!')

    def write_todos(self, todos):
        """Writes a list of todos to the database.
        
        Note: Since opening in 'w' mode, this will overwrite contents of the database.
        """
        try:
            with open(self.db_path, 'w') as f:
                json.dump(todos, f, indent=4)
        except OSError:
            print('Something went wrong trying to access the database!')
        except TypeError:
            print('Something went wrong trying to encode the todos to json!')

class DBController:
    """Database controller class for MVC architecture."""
    def __init__(self): 
        # should never be a controller instantiate for a database that isn't in Config.ini[General]['database]
        # added db_path kwarg to give unit test a way of leveraging mock db
        self.db = None
        self.configurer = config.Config()
        # self._db_handler = DatabaseHandler(self.db_path)
        # self.todo_list = []

    # def list(self) -> List[Dict]:
    #     """List the todos in the database."""
    #     return self._db_handler.read_todos()    

    # def add(self,name, description, priority) -> toDo:
    #     """Add a toDo to the database."""
    #     todo = toDo(name,description,priority)
    #     self.todo_list.append(todo)
    #     todos = self.list()
    #     todos.append(todo.dict)
    #     self._db_handler.write_todos(todos)
    #     return todo

    # def complete(self,id):
    #     """Update the done status for the specified todo to True"""
    #     todos = self.list()
    #     #TODO very inneficient way of doing this... consider optimizing such that don't need to loop entire db
    #     try:
    #         todo, todo_name = self._fetch_todo(todos,id)
    #         if not todo[todo_name]['done_status']:
    #             todo[todo_name]['done_status'] = True
    #             print(f'Changed done_status for {id} to True')
    #         else:
    #             print('This todo has already been completed!')
    #     except ValueError:
    #         print('The specified todo could not be found!')

    #     self._db_handler.write_todos(todos)

    # def remove(self,id):
    #     """"Remove the specified todo from the database."""
    #     todos = self.list()
    #     try:
    #         todo, todo_name = self._fetch_todo(todos,id)
    #     except ValueError as e:
    #         print(str(e))
    #         return
    #     todos.pop(todo[todo_name]['index'])
    #     self._db_handler.write_todos(todos)

    def discover_existing_database(self) -> None:
        logging.info("Searching for existing database...")
        try:
            config_file_path = self.configurer.get_config_file_path()
            self.db = database.Database(config_file_path)
            # TODO: For now it is assumed that if the if a config file, there is also a DB at the default path.
            # This is obviously not always necessarily true... Need to improve robustness. Probably move
            # _initialize_database to a seperate function. 

        except FileNotFoundError:
            logging.info("Could not find an existing database!")
            self._initialize_database()

    def clear_database(self) -> None:
        """Remove all entries in the database and reset it with and empty list.
        
        This function will prompt the user before executing clear option. If user
        enters anything besides "yes", the program will quit.
        """
        clear_confirmation = input("Type 'yes' to clear database: \n")
        if clear_confirmation == "yes" and self.db is not None:
            self.db.clear()
        else:
            logging.info("Aborting clear database operation...")
    

    def _initialize_database(self) -> None:
        """Initialize the ToDo database with an empty list.
        
        This function is called if discover_existing_database can't find an existing on user's system.

        Initializing a database consists of:
            - Create a Configs directory along with a config.ini file.
            - Create a blank database.json file using the information from the config file.
        """
        logging.info("Initializing database...")
        config_file_path = self.configurer.create_db_config()
        self.db = database.Database(config_file_path)

    # def _fetch_todo(self,todo_list,id):
    #     """Return the corresponding todo from the database for the provided id."""
    #     for todo in todo_list:
    #         todo_name = next(iter(todo)) #access the id element of the first (and only) element
    #         # import pdb; pdb.set_trace()
    #         if todo[todo_name]['id'] == id:
    #             return todo, todo_name
    #     raise ValueError("This id does not exist!")

    
