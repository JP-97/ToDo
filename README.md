
Run with poetry run todo <cmd> from ToDo directory


TODO - May 1st

Refactor initialize DB methodology... CLI uses controller to call init -> init uses config to create config file and database to create the database -> will need to refactor database as well since all the checks for the db_path and config file are going fdf be done with config class.

May 4th:

Complete redesign needs to be done.. Reduce number of classes. Starting from cli. CLI should exclusively use DBController to talk to DB. re-writing initialize_db function. DBController creates an instance of config, makes sure file exists. then creates an instance of db and makes sure DB gets created.

July 4th:

Optimized init function so that the db is automatically created as part of the __init__ method. No need to run an additional "initialize()" function. 

July 11th:
Added DBController.clear() api... Realized that program quits after single operation, meanining DBController is re-initialized each run... Need persistence somehow... Loop inputs? or have a
function in main() that checks if a DB already exists and initiliazes a DBController accordingly.

July 12th:
Added function to find existing database using config file. If a config file is found, it is assumed that there is also a database (need to fix this - not a correct assumption). A dbcontroller will be created with this database information.

    - Need to add looping mechanism in cli so that multiple commands can be provided for a single session. 

July 13th:
Removed init mechanism... felt awkward for user to have to manually initialize db. discover_existing_database will now look for an existing DB in the default path and if it can't find one, will initialize one. 

Created git repo named "ToDo" and made initial commit. Now all new features can be properly developped on local branch and regular commits can be made.

July 14th:
Started cli --add logic - created add_to_do() in rptodo, created a helper in cli.py that prompts user for description and priority of the todo, updated toDo.py such that its description and priority adhere to certain constraints!

July 19th:
Continued working on --add logic - created methods in database.py to get unique id, write to database, retrieve database contents.

Aug 4th
Finishes add_to_do in database.py/rptodo.py, created render.py to act as the project's "view" and started working on --list functionality, updated lynting settings for project.
- Need to figure out a way to sort the database contents based on priority!

August 5th:
Figured out how to sort dict of dicts using sorted(), refactored rendering logic to make sure blank DB wasn't printed
- Need to figure out a way to make logging.info look like standard print, but logging.error look like actual ERROR - don't want to use print to display info
- Need to write unit test for --list and --add so that I can push to github

August 6th:
Improved general robustness of all controller methods. Improved logging not to print to stdout. All controller and renderer exceptions to be caught by main.
** Came up with design choice that all controller public methods should return a str containing a 'success msg' which can then be passed to renderer. All printing to stdout
is to be done by renderer.
- Need to consider moving discover_existing_database to DBController's init method... Doesn't make much sense calling it from CLI, since CLI should have no knowledge of DB.

Aug 11th:
Removed discover_existing_database from controller. Now, Database has an instance of Config. When self._config is created, the database config file is created and DatabasePath
is populated. Database can then use this config along with get_database_location api to get the abs path for reads, writes and initialization. Now there is a stronger dependency
between them, but also less likelyhood one exists when the other doesnt. 
- TLDR: Database does not modify the config file now, it just reads from it. 

