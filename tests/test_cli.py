import pytest
import sys
import os
from rptodoProject import cli, config, database

def test_init_db(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """
    - Ensure chosing <init> results in creation of db and config file in appropriate location
    """
    monkeypatch.setattr("sys.argv", ["pytest", "init"])
    monkeypatch.setattr("rptodoProject.config.Config.APP_DIR", tmp_path)
    monkeypatch.setattr("rptodoProject.database.Database.APP_DIR", tmp_path)
    print(sys.argv)
    result = cli.main()
    print(list(tmp_path.iterdir()))
    # assert 0