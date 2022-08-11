class toDo(): #TODO convert this to a dataclass! (maybe?)
    """Simple class to model todo object."""

    def __init__(self, description, priority):

        self.description = description
        self.priority = priority  #TODO understand priority checking logic provided from @Property decorator
        # self.done = False
        # self.id = id(self)
        # self.db_index = database_size # account for 0 indexing done by lists

    # Enforce description and priority requirements

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, d):
        if len(d) > 100:
            raise ValueError("To-Do description exceeds allowable length (100 chars)!")
        self._description = d

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, p):
        try:
            p_int = int(p)            
        except ValueError:
            raise ValueError("To-Do priority was not a valid integer!")
        else:
            if p_int < 1 or p_int > 5:
                raise ValueError("To-Do priority is not in the correct range!")
            self._priority = p
