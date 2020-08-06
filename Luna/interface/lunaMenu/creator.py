import pymel.core as pm
from functools import partial
from Luna import Logger
from Luna import external
from Luna.core import optionVarFn
from Luna.static import Directories
from Luna.interface.lunaMenu import functions


def _null_command(*args):
    pass


class LunaMenu:
    MAIN_WINDOW = pm.melGlobals["gMainWindow"]
    MENU_OBJECT = "LunaMainMenu"
    MENU_LABEL = "Luna"
    ICON_PATH = Directories.ICONS_PATH

    @classmethod
    def _delete_old(cls):
        if pm.menu(cls.MENU_OBJECT, label=cls.MENU_LABEL, exists=1, parent=cls.MAIN_WINDOW):
            pm.deleteUI(pm.menu(cls.MENU_OBJECT, e=1, deleteAllItems=1))

    def __init__(self):
        self.menu = None  # type : pymel.core.uitypes.Menu
        self._delete_old()
        self.build()

    def addMenuItem(self,
                    parent=None,
                    label="",
                    command=_null_command,
                    icon="",
                    divider=False,
                    option_box=False,
                    check_box=False,
                    use_maya_icons=False,
                    optionVar_name=None,
                    default_value=False):

        if icon and not use_maya_icons:
            icon = self.iconPath + icon

        if divider:
            return pm.menuItem(p=parent, dl=label, i=icon, d=divider)

        elif option_box:
            return pm.menuItem(p=parent, l=label, i=icon, ob=option_box, c=command)

        elif check_box:
            if not optionVar_name:
                Logger.error("Menuitem: {0}::{1} is not connected to optionVar!".format(parent, label))
                return

            checkBox_value = optionVarFn.getOptionVar(optionVar_name, default=default_value)
            checkBox = pm.menuItem(p=parent, l=label, i=icon, cb=checkBox_value, c=partial(optionVarFn.toggleOptionVar, optionVar_name))
            return checkBox

        else:
            return pm.menuItem(p=parent, l=label, i=icon, c=command)

    def addSubMenu(self, parent, label, tear_off=False, icon=None, use_maya_icons=False):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon and not use_maya_icons:
            icon = self.ICON_PATH + icon

        return pm.menuItem(p=parent, l=label, i=icon, subMenu=True, to=tear_off)

    def build(self):
        Logger.info("Building {0} menu...".format(self.MENU_LABEL))
        self.menu = pm.menu(self.MENU_OBJECT, label=self.MENU_LABEL, parent=self.MAIN_WINDOW, tearOff=1)

        # Add items
        self.addMenuItem(self.menu, label="Build manager", command=functions.mainMenu.build_manager)

        # Tools
        self.tools_menu = self.addSubMenu(self.menu, label="Tools", tear_off=1)
        if "dsRenamingTool" in pm.moduleInfo(lm=1):
            self.addMenuItem(self.tools_menu, "Renaming tool", command=external.tools.renaming_tool, icon="rename.png", use_maya_icons=1)
            Logger.info("dsRenamingTool detected. Shortcut was added to Tools menu")

        # Prefs
        self.addMenuItem(self.menu, divider=1)
        self.addMenuItem(self.menu, label="Preferences", command=functions.mainMenu.prefs_manager)

        Logger.info("Successfully added menu: {0}".format(self.MENU_LABEL))


if __name__ == "__main__":
    luna_menu = LunaMenu()
