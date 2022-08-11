import pytest
import json
import pathlib

from typing import Dict, Any

from rptodoProject import config, database, toDo
from rptodoProject.exceptions import DBReadError, FileError


@pytest.fixture
def db(tmp_path: pathlib.WindowsPath, monkeypatch) -> database.Database:
    """Return a Database with location mocked to use tmp_path fixture."""
    d = tmp_path / "Database"
    d.mkdir()
    t = d / "_database.json"
    monkeypatch.setattr(config.Config, "get_database_location", lambda _: t)
    db = database.Database()
    return db


def write_dummy_contents_to_db(db: database.Database, contents_to_write: Dict[str, Dict[str, str]]) -> None:
    """Write provided contents to provided database."""
    with open(db._database_abs_path, "w") as db_contents:
        db_contents.write(json.dumps(contents_to_write, indent=4))


def get_contents_from_db(db: database.Database) -> Dict[str, Any]:
    """Return a dict containing db's contents."""
    with open(db._database_abs_path, "r") as db_contents:
        return json.load(db_contents)


def test_add_to_do(db: database.Database) -> None:
    """Given a blank database, ensure that:
    - we can add multiple todos
    - each todo gets a unique ID.
    """
    test_todos = [toDo.toDo("This is test todo 1", "5"), toDo.toDo("This is test todo 2", "1")]

    for todo in test_todos:
        db.add_to_do(todo)

    db_contents = get_contents_from_db(db)

    assert len(db_contents) == 2  # validate that both todos were added
    assert list(db_contents.keys())[0] != list(db_contents.keys())[1]  # validate that both todos have unique ids


def test_clear(db: database.Database) -> None:
    dummy_db_contents = {"1": {"dummy_key": "dummy_val"}, "2": {"dummy_key": "dummy_val"}}
    write_dummy_contents_to_db(db, dummy_db_contents)

    db.clear()

    db_contents = get_contents_from_db(db)
    assert len(db_contents) == 0


@pytest.mark.parametrize(
    "db, dummy_db_contents",
    [("db", {"1": {"dummy_key": "dummy_val"}, "2": {"dummy_key": "dummy_val"}}), ("db", {})],
    indirect=["db"],
)
def test_get_database_contents(db: database.Database, dummy_db_contents: Any) -> None:
    write_dummy_contents_to_db(db, dummy_db_contents)

    assert db.get_database_contents() == dummy_db_contents


def test_get_database_contents_invalid_db_contents(db) -> None:
    dummy_db_contents = "Invalid JSON"
    with open(db._database_abs_path, "w") as db_contents:
        db_contents.write(dummy_db_contents)

    with pytest.raises(DBReadError):
        db.get_database_contents()


def test_get_database_contents_no_database_found(db) -> None:
    db._database_abs_path = "fake_path"
    with pytest.raises(FileError):
        db.get_database_contents()
