"""Container class to hold rptodo specific exceptions."""


class DirError(Exception):
    pass


class FileError(Exception):
    pass


class DBWriteError(Exception):
    pass


class DBReadError(Exception):
    pass


class DBClearError(Exception):
    pass


class JsonError(Exception):
    pass


class IDError(Exception):
    pass


class RangeError(Exception):
    pass
