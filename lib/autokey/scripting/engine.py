# Copyright (C) 2011 Chris Dekter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections.abc import Iterable

from typing import Tuple, Optional, List, Union

from autokey import model


class Engine:
    """
    Provides access to the internals of AutoKey.

    Note that any configuration changes made using this API while the configuration window
    is open will not appear until it is closed and re-opened.
    """
    SendMode = model.SendMode
    Key = model.Key

    def __init__(self, config_manager, runner):
        self.configManager = config_manager
        self.runner = runner
        self.monitor = config_manager.app.monitor
        self._macro_args = []
        self._return_value = ''
        self._triggered_abbreviation = None  # type: Optional[str]

    def get_folder(self, title: str):
        """
        Retrieve a folder by its title

        Usage: C{engine.get_folder(title)}

        Note that if more than one folder has the same title, only the first match will be
        returned.
        """
        for folder in self.configManager.allFolders:
            if folder.title == title:
                return folder
        return None

    def create_folder(self, title: str, parent_folder=None, temporary=False):
        """
        Create and return a new folder.

        Usage: C{engine.create_folder("new folder"), parent_folder=folder, temporary=True}

        Descriptions for the optional arguments:

        @param parentFolder: Folder to make this folder a subfolder of.
        @param temporary: Folders created with temporary=True are
                                    not persisted.
                                    Used for single-source rc-style scripts.

        If a folder of that name already exists, this will return it unchanged.
        The 'temporary' property is not touched to avoid deleting an existing
        folder.
        Note that if more than one folder has the same title, only the first match will be
        returned.
        """
        self.validateType(title, "title", str, "str")
        self.validateType(parent_folder, "parent_folder", model.Folder, "folder")
        self.validateType(temporary, "temporary", bool, "bool")
        if parent_folder is None:
            parent_folders = self.configManager.allFolders
        else:
            parent_folders = parent_folder.folders

        for folder in parent_folders:
            if folder.title == title:
                return folder
        else:
            new_folder = model.Folder(title)
            if parent_folder is None:
                self.configManager.allFolders.append(new_folder)
            else:
                parent_folder.add_folder(new_folder)
                if not temporary and parent_folder.temporary:
                    raise ValueError("Parameter 'temporary' is False, but parent folder is a temporary one. \
Folders created within temporary folders must themselves be set temporary")

            if not temporary:
                new_folder.persist()
            else:
                new_folder.temporary = True
            return new_folder


    def create_phrase(self, folder, name: str, contents: str,
                      abbreviations: Union[str, List[str]]=None,
                      hotkey: Tuple[List[Union[model.Key, str]], Union[model.Key, str]]=None,
                      send_mode: model.SendMode=model.SendMode.KEYBOARD, window_filter: str=None,
                      show_in_system_tray: bool=False, always_prompt: bool=False,
                      temporary=False):
        """
        Create a new text phrase inside the given folder. Use C{engine.get_folder(folder_name)} to retrieve the folder
        you wish to create the Phrase in. If the folder is a temporary
        one, the phrase will be created as temporary.

        The first three arguments (folder, name and contents) are required. All further arguments are optional and
        considered to be keyword-argument only. Do not rely on the order of the optional arguments.
        The optional parameters can be used to configure the newly created Phrase.

        Usage (minimal example): C{engine.create_phrase(folder, name, contents)}

        Further concrete examples:
        C{
        engine.create_phrase(folder, "My new Phrase", "This is the Phrase content", abbreviations=["abc", "def"],
        hotkey=([engine.Key.SHIFT], engine.Key.NP_DIVIDE), send_mode=engine.SendMode.CB_CTRL_SHIFT_V,
        window_filter="konsole\.Konsole", show_in_system_tray=True)
        }

        Descriptions for the optional arguments:

        abbreviations may be a single string or a list of strings. Each given string is assigned as an abbreviation
        to the newly created phrase.

        hotkey parameter: The hotkey parameter accepts a 2-tuple, consisting of a list of modifier keys in the first
        element and an unshifted (lowercase) key as the second element.
        Modifier keys must be given as a list of strings (or Key enum instances), with the following
        values permitted:
            <ctrl>
            <alt>
            <super>
            <hyper>
            <meta>
            <shift>
        The key must be an unshifted character (i.e. lowercase) or a Key enum instance. Modifier keys from the list
        above are NOT allowed here. Example: (["<ctrl>", "<alt>"], "9") to assign "<Ctrl>+<Alt>+9" as a hotkey.
        The Key enum contains objects representing various special keys and is available as an attribute of the "engine"
        object, named "Key". So to access a function key, you can use the string "<f12>" or engine.Key.F12
        See the AutoKey Wiki for an overview of all available keys in the enumeration.

        send_mode: This parameter configures how AutoKey sends the phrase content, for example by typing or by pasting
        using the clipboard. It accepts items from the SendMode enumeration, which is also available from the engine
        object as engine.SendMode. The parameter defaults to
        engine.SendMode.KEYBOARD. Available send modes are:
            KEYBOARD
            CB_CTRL_V
            CB_CTRL_SHIFT_V
            CB_SHIFT_INSERT
            SELECTION
        To paste the Phrase using "<shift>+<insert>, set send_mode=engine.SendMode.CB_SHIFT_INSERT

        window_filter: Accepts a string which will be used as a regular expression to match window titles or
        applications using the WM_CLASS attribute.

        @param folder: folder to place the abbreviation in, retrieved using C{engine.get_folder()}
        @param name: Name/description for the phrase.
        @param contents: the expansion text
        @param abbreviations: Can be a single string or a list (or other iterable) of strings. Assigned to the Phrase
        @param hotkey: A tuple containing a keyboard combination that will be assigned as a hotkey.
                       First element is a list of modifiers, second element is the key.
        @param send_mode: The pasting mode that will be used to expand the Phrase.
                          Used to configure, how the Phrase is expanded. Defaults to typing using the "Keyboard" method.
        @param window_filter: A string containing a regular expression that will be used as the window filter.
        @param show_in_system_tray: A boolean defaulting to False.
                                    If set to True, the new Phrase will be shown in the tray icon context menu.
        @param always_prompt: A boolean defaulting to False. If set to True,
                              the Phrase expansion has to be manually confirmed, each time it is triggered.
        @param temporary: Hotkeys created with temporary=True are
                                    not persisted as .jsons, and are replaced if the description is not
                                    unique within the folder.
                                     Used for single-source rc-style scripts.
        @raise ValueError: If a given abbreviation or hotkey is already in use or parameters are otherwise invalid
        @return The created Phrase object. This object is NOT considered part of the public API and exposes the raw
          internals of AutoKey. Ignore it, if you don’t need it or don’t know what to do with it.
          It can be used for _really_ advanced use cases, where further customizations are desired. Use at your own
          risk. No guarantees are made about the object’s structure. Read the AutoKey source code for details.
        """
        # Start with input type-checking.
        self.validateType(folder, "folder", model.Folder, "folder")
        self.validateType(name, "name", str, "str")
        self.validateType(contents, "contents", str, "str")
        self.validateAbbreviations(abbreviations)
        self.validateHotkey(hotkey)
        self.validateType(send_mode, "send_mode", model.SendMode, "model.SendMode")
        self.validateType(window_filter, "window_filter", str, "str")
        self.validateType(show_in_system_tray, "show_in_system_tray", bool, "bool")
        self.validateType(always_prompt, "always_prompt", bool, "bool")
        self.validateType(temporary, "temporary", bool, "bool")
        # TODO: The validation should be done by some controller functions in the model base classes.
        if abbreviations:
            if isinstance(abbreviations, str):
                abbreviations = [abbreviations]
            elif not isinstance(abbreviations, Iterable):
                raise ValueError("Expected a single string or a list/iterable of strings, not {}".format(
                    type(abbreviations))
                )
            for abbr in abbreviations:
                if not self.configManager.check_abbreviation_unique(abbr, None, None)[0]:
                    raise ValueError("The specified abbreviation '{}' is already in use.".format(abbr))
        if hotkey:
            modifiers = sorted(hotkey[0])
            if not self.configManager.check_hotkey_unique(modifiers, hotkey[1], None, None)[0]:
                raise ValueError("The specified hotkey and modifier combination is already in use.")

        if folder.temporary and not temporary:
            raise ValueError("Parameter 'temporary' is False, but parent folder is a temporary one. \
Phrases created within temporary folders must themselves be explicitly set temporary")

        self.monitor.suspend()
        try:
            p = model.Phrase(name, contents)
            if send_mode in model.SendMode:
                p.sendMode = send_mode
            if abbreviations:
                p.add_abbreviations(abbreviations)
            if hotkey:
                p.set_hotkey(*hotkey)
            if window_filter:
                p.set_window_titles(window_filter)
            p.show_in_tray_menu = show_in_system_tray
            p.prompt = always_prompt
            p.temporary = temporary

            folder.add_item(p)
            # Don't save a json if it is a temporary hotkey. Won't persist across
            # reloads.
            if not temporary:
                p.persist()
            return p
        finally:
            self.monitor.unsuspend()
            self.configManager.config_altered(False)


    def validateType(self, item, name, type_, type_description):
        if item is not None and not isinstance(item, type_):
            raise ValueError("Expected {} to be {}, not {}".format(
                name,
                type_description,
                type(item)))

    def validateAbbreviations(self, abbreviations):
        if abbreviations is not None:
            fail=False
            if not isinstance(abbreviations, str):
                fail=True
                if isinstance(abbreviations, list):
                    fail=False
                    for item in abbreviations:
                        if not isinstance(item, str):
                            fail=True
            if fail:
                raise ValueError("Expected abbreviations to be str or list of str, not {}".format(
                    type(abbreviations))
                    )


    def isValidHotkeyType(self, item):
        return isinstance(item, str) or \
                            isinstance(item, model.Key)

    def validateHotkey(self, hotkey):
        if hotkey is not None:
            fail=False
            if not isinstance(hotkey, tuple):
                fail=True
            else:
                if len(hotkey) != 2:
                    fail=True
                else:
                    # First check modifiers is list of str or keys
                    if isinstance(hotkey[0], list):
                        for item in hotkey[0]:
                            if not self.isValidHotkeyType(item):
                                fail=True
                    elif not self.isValidHotkeyType(hotkey[0]):
                        fail=True
                    else:
                        fail=True
                    # Then check second element is a key or str
                    if not self.isValidHotkeyType(hotkey[1]):
                        fail=True
            if fail:
                raise ValueError("Expected hotkey to be a tuple of modifiers then keys, as lists of model.Key or str, not {}".format(
                    type(hotkey))
                )


    def create_abbreviation(self, folder, description, abbr, contents):
        """
        DEPRECATED. Use engine.create_phrase() with appropriate keyword arguments instead.
        Create a new text phrase inside the given folder and assign the abbreviation given.

        Usage: C{engine.create_abbreviation(folder, description, abbr, contents)}

        When the given abbreviation is typed, it will be replaced with the given
        text.

        @param folder: folder to place the abbreviation in, retrieved using C{engine.get_folder()}
        @param description: description for the phrase
        @param abbr: the abbreviation that will trigger the expansion
        @param contents: the expansion text
        @raise Exception: if the specified abbreviation is not unique
        """
        if not self.configManager.check_abbreviation_unique(abbr, None, None)[0]:
            raise Exception("The specified abbreviation is already in use")

        self.monitor.suspend()
        p = model.Phrase(description, contents)
        p.modes.append(model.TriggerMode.ABBREVIATION)
        p.abbreviations = [abbr]
        folder.add_item(p)
        p.persist()
        self.monitor.unsuspend()
        self.configManager.config_altered(False)

    def create_hotkey(self, folder, description, modifiers, key, contents):
        """
        DEPRECATED. Use engine.create_phrase() with appropriate keyword arguments instead.

        Create a text hotkey

        Usage: C{engine.create_hotkey(folder, description, modifiers, key, contents)}

        When the given hotkey is pressed, it will be replaced with the given
        text. Modifiers must be given as a list of strings, with the following
        values permitted:

        <ctrl>
        <alt>
        <super>
        <hyper>
        <meta>
        <shift>

        The key must be an unshifted character (i.e. lowercase)

        @param folder: folder to place the abbreviation in, retrieved using C{engine.get_folder()}
        @param description: description for the phrase
        @param modifiers: modifiers to use with the hotkey (as a list)
        @param key: the hotkey
        @param contents: the expansion text
        @raise Exception: if the specified hotkey is not unique
        """
        modifiers.sort()
        if not self.configManager.check_hotkey_unique(modifiers, key, None, None)[0]:
            raise Exception("The specified hotkey and modifier combination is already in use")

        self.monitor.suspend()
        p = model.Phrase(description, contents)
        p.modes.append(model.TriggerMode.HOTKEY)
        p.set_hotkey(modifiers, key)
        folder.add_item(p)
        p.persist()
        self.monitor.unsuspend()
        self.configManager.config_altered(False)

    def run_script(self, description):
        """
        Run an existing script using its description to look it up

        Usage: C{engine.run_script(description)}

        @param description: description of the script to run
        @raise Exception: if the specified script does not exist
        """
        target_script = None
        for item in self.configManager.allItems:
            if item.description == description and isinstance(item, model.Script):
                target_script = item

        if target_script is not None:
            self.runner.run_subscript(target_script)
        else:
            raise Exception("No script with description '%s' found" % description)

    def run_script_from_macro(self, args):
        """
        Used internally by AutoKey for phrase macros
        """
        self._macro_args = args["args"].split(',')

        try:
            self.run_script(args["name"])
        except Exception as e:
            self.set_return_value("{ERROR: %s}" % str(e))

    def get_macro_arguments(self):
        """
        Get the arguments supplied to the current script via its macro

        Usage: C{engine.get_macro_arguments()}

        @return: the arguments
        @rtype: C{list(str())}
        """
        return self._macro_args

    def set_return_value(self, val):
        """
        Store a return value to be used by a phrase macro

        Usage: C{engine.set_return_value(val)}

        @param val: value to be stored
        """
        self._return_value = val

    def _get_return_value(self):
        """
        Used internally by AutoKey for phrase macros
        """
        ret = self._return_value
        self._return_value = ''
        return ret

    def _set_triggered_abbreviation(self, abbreviation: str, trigger_character: str):
        """
        Used internally by AutoKey to provide the abbreviation and trigger that caused the script to execute.
        @param abbreviation: Abbreviation that caused the script to execute
        @param trigger_character: Possibly empty "trigger character". As defined in the abbreviation configuration.
        """
        self._triggered_abbreviation = abbreviation
        self._triggered_character = trigger_character

    def get_triggered_abbreviation(self) -> Tuple[Optional[str], Optional[str]]:
        """
        This function can be queried by a script to get the abbreviation text that triggered it’s execution.

        If a script is triggered by an abbreviation, this function returns a tuple containing two strings. First element
        is the abbreviation text. The second element is the trigger character that finally caused the execution. It is
        typically some whitespace character, like ' ', '\t' or a newline character. It is empty, if the abbreviation was
        configured to "trigger immediately".

        If the script execution was triggered by a hotkey, a call to the DBus interface, the tray icon, the "Run"
        button in the main window or any other means, this function returns a tuple containing two None values.

        Usage: C{abbreviation, trigger_character = engine.get_triggered_abbreviation()}
        You can determine if the script was triggered by an abbreviation by simply testing the truth value of the first
        returned value.

        @return: Abbreviation that triggered the script execution, if any.
        @rtype: C{Tuple[Optional[str], Optional[str]]}
        """
        return self._triggered_abbreviation, self._triggered_character