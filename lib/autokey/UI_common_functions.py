import dbus
import importlib
import os.path
from shutil import which
import re
import subprocess
import sys
import time

from . import common
import autokey.model.helpers
import autokey.configmanager.configmanager as cm
import autokey.configmanager.configmanager_constants as cm_constants

logger = __import__("autokey.logger").logger.get_logger(__name__)

common_modules = ['argparse', 'collections', 'enum', 'faulthandler', 
            'gettext', 'inspect', 'itertools', 'logging', 'os', 'select', 'shlex',
            'shutil', 'subprocess', 'sys', 'threading', 'time', 'traceback', 'typing',
            'warnings', 'webbrowser', 'dbus', 'pyinotify']
gtk_modules = ['gi', 'gi.repository.Gtk', 'gi.repository.Gdk', 'gi.repository.Pango',
            'gi.repository.Gio', 'gi.repository.GtkSource']
qt_modules = ['PyQt5', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QtCore',
            'PyQt5.Qsci']

common_programs = ['wmctrl', 'ps']
# Checking some of these appears to be redundant as some are provided by the same packages on my system but 
# better safe than sorry.
optional_programs = ['visgrep', 'import', 'png2pat', 'xte', 'xmousepos']
gtk_programs = ['zenity']
qt_programs = ['kdialog']

def checkModuleImports(modules):
    missing_modules = []
    for module in modules:
        spec = importlib.util.find_spec(module)
        if spec is None: #module has not been imported/found correctly
            logger.error("Python module: \""+module+"\" was not found/able to be imported correctly on the system check that the module(s) are installed correctly")
            missing_modules.append(module)

    return missing_modules

def checkProgramImports(programs, optional=False):
    missing_programs = []
    for program in programs:
        if which(program) is None:
            # file not found by shell
            if optional:
                logger.info("Optional Commandline Program: \""+program+"\" was not found/able to be used correctly by AutoKey. Check that this program is correctly installed on your system.")
            else:
                logger.error("Commandline Program: \""+program+"\" was not found/able to be used correctly by AutoKey. Check that this program is correctly installed on your system.")
            missing_programs.append(program)
    return missing_programs

def checkOptionalPrograms():
    if common.USING_QT:
        checkProgramImports(optional_programs, optional=True)
    else:
        checkProgramImports(optional_programs, optional=True)

def getErrorMessage(item_type, missing_items):
    error_message = ""
    for item in missing_items:
         error_message+= item_type+": "+item+"\n"
    return error_message

def checkRequirements():
    errorMessage = ""
    if common.USING_QT:
        missing_programs = checkProgramImports(common_programs+qt_programs)
        missing_modules = checkModuleImports(common_modules+qt_modules)
    else:
        missing_programs = checkProgramImports(common_programs+gtk_programs)
        missing_modules = checkModuleImports(common_modules+gtk_modules)
    errorMessage += getErrorMessage("Python Modules",missing_modules)
    errorMessage += getErrorMessage("Programs",missing_programs)
    return errorMessage


# def init_global_hotkeys(app, configManager):
#     logger.info("Initialise global hotkeys")
#     configManager.toggleServiceHotkey.set_closure(app.toggle_service)
#     configManager.configHotkey.set_closure(app.show_configure_signal.emit)
#     This line replaces the above line in the gtk app. Need to find out
#     what the difference is before continuing.
#     configManager.configHotkey.set_closure(app.show_configure_async)


def path_created_or_modified(configManager, configWindow, path):
    time.sleep(0.5)
    changed = configManager.path_created_or_modified(path)
    if changed and configWindow is not None:
        configWindow.config_modified()

def path_removed(configManager, configWindow, path):
    time.sleep(0.5)
    changed = configManager.path_removed(path)
    if changed and configWindow is not None:
        configWindow.config_modified()


def save_item_filter(app, item):
    filter_regex = app.get_filter_text()
    try:
        item.set_window_titles(filter_regex)
    except re.error:
        logger.error(
            "Invalid window filter regex: '{}'. Discarding without saving.".format(filter_regex)
        )
    item.set_filter_recursive(app.get_is_recursive())


def get_hotkey_text(app, key):
    if key in app.KEY_MAP:
        keyText = app.KEY_MAP[key]
    else:
        keyText = key
    return keyText


def save_hotkey_settings_dialog(app, item):
    modifiers = app.get_active_modifiers()

    if app.key in app.REVERSE_KEY_MAP:
        key = app.REVERSE_KEY_MAP[app.key]
    else:
        key = app.key

    if key is None:
        raise RuntimeError("Attempt to set hotkey with no key")
    logger.info("Item {} updated with hotkey {} and modifiers {}".format(item, key, modifiers))
    item.set_hotkey(modifiers, key)

def load_hotkey_settings_dialog(app, item):
    app.targetItem = item
    if autokey.model.helpers.TriggerMode.HOTKEY in item.modes:
        app.populate_hotkey_details(item)
    else:
        app.reset()

def load_global_hotkey_dialog(app, item):
    if item.enabled:
        app.populate_hotkey_details(item)
    else:
        app.reset()

def show_config_window(app):
    if cm.ConfigManager.SETTINGS[cm_constants.IS_FIRST_RUN]:
        cm.ConfigManager.SETTINGS[cm_constants.IS_FIRST_RUN] = False
        app.args.show_config_window = True
    if app.args.show_config_window:
        app.show_configure()

