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

# from autokey.gtkui import dialogs
# from autokey.gtkui.dialogs import WindowFilterSettingsDialog

@pytest.mark.skip(reason="unfinished test implementation")
def test_WindowFilterSettingsDialog_save():
    with \
            patch("autokey.gtkui.dialogs.WindowFilterSettingsDialog.get_is_recursive"), \
            patch("autokey.gtkui.dialogs.WindowFilterSettingsDialog.get_filter_text", return_value=".*"):
        WindowFilterSettingsDialog.save(item)

