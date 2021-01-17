# Copyright (C) 2020 BlueDrink9

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import typing
import sys
import os

from unittest.mock import MagicMock, patch

import pytest
from hamcrest import *
from tests.engine_helpers import *

import autokey.model.folder
from autokey.configmanager import configmanager
from autokey.configmanager.configmanager import ConfigManager
from autokey.service import PhraseRunner
import autokey.service
from autokey.scripting import Engine

confman_module_path = "autokey.configmanager.configmanager"
# These tests currently use the scripting API to create test phrases.
# If we can do it a better way, we probably should, to reduce dependencies for
# these tests.

def get_autokey_dir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def test_create_default_folder(tmp_path):
    default_folder = tmp_path / "autokey"
    assert not default_folder.exists()
    with patch(confman_module_path + ".CONFIG_DEFAULT_FOLDER",
               default_folder):
        configmanager.create_default_folder()
        assert_that(default_folder.exists(),
                    "creating default config folder fails")

def test_recover_backup_config(tmp_path):
    config = tmp_path / "autokey.json"
    backup = tmp_path / "autokey.json~"
    backup.touch()
    assert not config.exists() and backup.exists()
    with \
            patch(confman_module_path + ".CONFIG_FILE", config), \
            patch(confman_module_path + ".CONFIG_FILE_BACKUP", backup), \
            patch(confman_module_path + "._restore_backup_config") as mock:
        configmanager._recover_config_backup(False, Exception())
        mock.assert_called_once()
                    # "creating default config folder fails")

def test_recover_backup_config_without_backup_raises_error(tmp_path):
    config = tmp_path / "autokey.json"
    backup = tmp_path / "autokey.json~"
    assert not config.exists() and not backup.exists()
    with \
            patch(confman_module_path + ".CONFIG_FILE", config), \
            patch(confman_module_path + ".CONFIG_FILE_BACKUP", backup):
        with pytest.raises(OSError):
            configmanager._recover_config_backup(False, OSError())

def test_back_up_config(tmp_path):
    config = tmp_path / "autokey.json"
    config.touch()
    backup = tmp_path / "autokey.json~"
    assert config.exists() and not backup.exists()
    with \
            patch(confman_module_path + ".CONFIG_FILE", config), \
            patch(confman_module_path + ".CONFIG_FILE_BACKUP", backup):
        configmanager._back_up_config()
        assert_that(backup.exists(),
                    "Backing up config doesn't create a backup")

def test_restore_config(tmp_path):
    config = tmp_path / "autokey.json"
    backup = tmp_path / "autokey.json~"
    backup.touch()
    assert not config.exists() and backup.exists()
    with \
            patch(confman_module_path + ".CONFIG_FILE", config), \
            patch(confman_module_path + ".CONFIG_FILE_BACKUP", backup):
        configmanager._restore_backup_config()
        assert_that(config.exists(),
                    "restoring backup config doesn't create a new config")

def test_get_item_with_hotkey(create_engine):
    engine, folder = create_engine
    # --- Setup ---
    modifiers = ["<ctrl>", "<alt>", "<super>", "<shift>"]
    key = "a"
    hotkey=(modifiers, key)
    testHK = create_test_hotkey(engine, folder, hotkey)
    resultHK = engine.configManager.get_item_with_hotkey(modifiers,
                                                         key, None)
    assert_that(resultHK, is_(equal_to(testHK)))

# TODO: check multiple folders, and global/special hotkeys.
# Check for similar tests in test_engine.
def test_item_has_same_hotkey(create_engine):
    engine, folder = create_engine
    modifiers = ["<ctrl>", "<alt>", "<super>", "<shift>"]
    key = "a"
    hotkey=(modifiers, key)
    testHK = create_test_hotkey(engine, folder, hotkey)
    assert ConfigManager.item_has_same_hotkey(testHK, modifiers, key, None)
