# Copyright (C) 2019 BlueDrink9

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

from unittest.mock import MagicMock, patch
import pytest
from hamcrest import *

import autokey as ak
from autokey import baseUIActions

def test_save():
    expected_is_recursive=True
    expected_regex="Chrome*"
    dialog=MagicMock()
    item=MagicMock()
    def mock_get_dialog_regex():
        return expected_regex
    dialog.get_filter_text = mock_get_dialog_regex
    def mock_get_is_recursive():
        return expected_is_recursive
    dialog.get_is_recursive = mock_get_is_recursive

    def mock_set_item_recursive(result_):
        item.is_recursive=result_
    item.set_filter_recursive = mock_set_item_recursive
    def mock_set_item_title(regex):
        item.titleregex=regex
    item.set_window_titles = mock_set_item_title

    baseUIActions.save(dialog, item)

    assert_that(item.is_recursive, is_(expected_is_recursive))
    assert_that(item.titleregex, is_(expected_regex))

