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

import re

logger = __import__("autokey.logger").logger.get_logger(__name__)

def save(windowFilterDialog, item):
    regex = windowFilterDialog.get_filter_text()
    try:
        item.set_window_titles(regex)
    except re.error:
        logger.error(
                "Invalid window filter regex: '{}'. \
                        Discarding without saving.".format(regex)
                        )
    item.set_filter_recursive(windowFilterDialog.get_is_recursive())

