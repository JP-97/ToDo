from unittest import mock
import pytest
import json
import sys

from rptodoProject import cli
from rptodoProject.database import Database

@pytest.fixture
def db(): 
    return Database("C:\\Users\\Joshua\\Desktop\\Python\\ToDoApp\\rptodoProject\\Configs")

def test_initialize_db(db):
    
    assert DBController.initialize_database() == 0


# test_data1 = {
#     'name': 'test1',
#     'description': 'this is a test',
#     'priority': 1,
#     'todo':{'test1':{'description':'this is a test',
#                         'priority':1,
#                         'done_status':False,
#                         'id':1001}}
# }

# test_data2 = {
#     'name': 'test2',
#     'description': 'this is a test',
#     'priority': 2,
#     'todo':{'test2':{'description':'this is a test',
#                         'priority':2,
#                         'done_status':False,
#                         'id':1001}}
# }

# #create a mock json database with existing todo
# @pytest.fixture
# def mock_json_file(tmp_path):
#     todo = [toDo.toDo('test','test description',1).dict]
#     db_file = f'{tmp_path}\\test_db.json'
#     with open(db_file, 'w') as db:
#         json.dump(todo,db,indent=4)
#     return db_file

# @pytest.mark.parametrize(
# "name,description,priority,expected",
# [
#     pytest.param(test_data1['name'],test_data1['description'],
#             test_data1['priority'],test_data1['todo']),
    
#     pytest.param(test_data2['name'],test_data2['description'],
#             test_data2['priority'],test_data2['todo'])
    
# ]
# )
# def test_add(mock_json_file, name, description, priority, expected):

#     """
#     1.Get a to-do description and priority
#     2.Create a dictionary to hold the to-do information
#     3.Read the to-do list from the database
#     4.Append the new to-do to the current to-do list
#     5.Write the updated to-do list back to the database
#     6.Return the newly added to-do along with a return code back to the caller
#     """

    db_controller = rptodo.DBController(db_path=mock_json_file)
    #ensure that the returned todo has the same description. Difficult to track what the ID will be...
    assert db_controller.add(name,description,priority).dict[name]['description'] == expected[name]['description']
    db_contents_updated = db_controller._db_handler.read_todos()
    assert len(db_contents_updated) == 2

def test_list(mock_json_file):
    """Test to see if rptodo's list command works.

    Args:
        mock_json_file (str): path to mock database
    """
    db_controller = rptodo.DBController(db_path=mock_json_file)
    todos = db_controller.list()
    assert len(todos) == 1

# def test_complete(mock_json_file):
#     """Test to see if rptodo's complete command works."""
#     db_controller = rptodo.DBController(db_path=mock_json_file)
#     db_controller.complete(1000)
#     todos = db_controller._db_handler.read_todos()
#     for todo in todos:
        


