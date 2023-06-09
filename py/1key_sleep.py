"""
****A app for MacOS that press shortcut key to turn off display / system sleep****

Pressing the shortcut key will trigger the following functions:
CONTROL + F15 to Turn off display
CONTROL + COMMAND + F15 to System sleep

At the same time, the "Moon" icon is displayed in the Mac OS system status bar,
and the menu appears by clicking on it:
 - Turn off display
 - System sleep
 - Quit
Clicking on the menu also triggers the corresponding function.

Default FIRST_MODIFIERS_KEY are defined to 'CONTROL',
SECOND_MODIFIERS_KEY defined to 'OPTION',
and MASTER_KEY defined to 'F15'. you can change it by yourself.

Note: When running the app for the first time, a pop-up message will prompt '1KeySleep'
to receive buttons from any application program. At this, 'System Preferences' should be opened,
Allow 1KeySleep in the 'Security and Privacy' - 'Privacy' - 'Input Listening'
and 'Auxiliary Functions' columns (check after unlocking)

It is recommended to add an app to the 'System Preferences' -' Users and Groups'
- 'Login Items' to automatically launch this program with the system.

Shortcut customization:
MODIFIERS_KEY should be one of CONTROL / OPTION / COMMAND / SHIFT,
MASTER_KEY can be any key.

For the packaged app, right-click on 'Display Package Content' - Contents/Resources/
and find the file 'keysetting.cfg', Open it with text editor, modify the key values in
the first three lines, save, and then run again.

For the py file, 'keysetting.cfg' will be generated in the folder "../Resources/"
during the first run.

Another method is to directly modify the key definitions in the py source code,
which are located in , but the external config file will be read first when program running,
so you need delete the external file 'keysetting.cfg' before run it.

MacOs Bigsur + Python 3.8.3 + pyinstaller 5.9 compilation passed
(c) 2023 by Chflame, email:chflame@163.com
"""

import os
import sys
import gettext
from threading import Thread
from pynput import keyboard
import rumps

# set constants
class Constants:
    KEY_NAME_NOTICE = """
# Please press the following key names to set the keys
# 
# Letters and numbers directly express:
# a b ... 1 2 ...
# Symbols directly express too, but expressed with shift + other keys
# (such as ~ ! @ # $ % ^ & * etc.) are not supported
# ` = [ ] ; , . / ' ...
#
# Modification key (both sides equal): 
# control key: ctrl
# option key: alt
# command key: cmd
# shift key: shift
# When the shift key is used as the FIRST_MODIFIERS_KEY, some key values will change 
# and it is not recommended to use it with alphanumeric keys
#
# F keys (PrtSc, ScrLk, Pause are recognized as F13, F14, F15 in MacOS):
# f1 f2 ... f15
#
# Other keys: 
# up down left right page_up page_down home end insert delete tab 
# caps_lock backspace esc space enter
#
# Keypad enter:
# pad_enter  
#
# keypad NumLock：
# num_lock
#
# Fn: 
# fn
# The Fn key has different key codes on various keyboards, and uncertain whether it 
# can be triggered normally. It is also prone to conflicts with other modifiers key 
# and is NOT RECOMMENDED to use.
#
# Other Keys that are not within the above range have not been supported.
"""
    # default key
    DEFAULT_FIRST_MODIFIERS_KEY = "ctrl"
    DEFAULT_SECOND_MODIFIERS_KEY = "alt"
    DEFAULT_MASTER_KEY = "f15"

    # saved setting file name
    SETTING_FILENAME = os.path.join(os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),
                         "Resources"), "keysetting.cfg")
    # icon file name
    ICON_FILENAME = os.path.join(os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),
                        "Resources"), "1KeySleep.icns")

# Key events, sleep functions
class KeyboardMonitor:

    # sign of the function key press down
    first_key_is_press:bool = False
    second_key_is_press:bool = False

    # when key press
    def on_press(self, key):
        press_key = str(key).replace("Key.", "").replace("'", "").replace("_r", "")
        # key insert
        if str(key) == "'\\x05'":
            press_key = "insert"
        # keypad enter
        elif str(key) == "'\\x03'":
            press_key = "pad_enter"
        # key '
        elif str(key) == '''"'"''':
            press_key = "'"
        # key \
        elif str(key) == "'\\\\'":
            press_key = '\\'
        # key NumLock
        elif str(key) == "'\\x1b'":
            press_key = "num_lock"
        # key fn
        elif str(key) == "<179>":
            press_key = "fn"

        if press_key == StatusBarApp.MASTER_KEY and self.first_key_is_press \
                and self.second_key_is_press:
            self.system_sleep()
        elif press_key == StatusBarApp.MASTER_KEY and self.first_key_is_press:
            self.turn_off_display()
        elif press_key == StatusBarApp.FIRST_MODIFIERS_KEY:
            self.first_key_is_press = True
        elif press_key == StatusBarApp.SECOND_MODIFIERS_KEY:
            self.second_key_is_press = True

    # when key release
    def on_release(self, key):
        release_key = str(key).replace("Key.", "").replace("'", "").replace("_r", "")
        if str(key) == "<179>":
            release_key = "fn"
        if release_key == StatusBarApp.FIRST_MODIFIERS_KEY:
            self.first_key_is_press = False
        elif release_key == StatusBarApp.SECOND_MODIFIERS_KEY:
            self.second_key_is_press = False

    # function of system sleep
    def system_sleep(self):
        os.system("pmset sleepnow")

    # function of turn off display
    def turn_off_display(self):
        os.system("pmset displaysleepnow")


# MacOS statusbar menu
class StatusBarApp(rumps.App):

    def __init__(self):
        super(StatusBarApp, self).__init__("1KeySleep",
                icon=Constants.ICON_FILENAME, quit_button=None)

    # key name for menu display, replacing the modifier key symbol,
    # and capitalizing the initial letter
    def order_key_name(self, keyname:str) -> str:
        ret_str =  keyname.replace("cmd", "⌘"
                        ).replace("ctrl", "⌃"
                        ).replace("alt", "⌥"
                        ).replace("shift", "⇧"
                        ).title().rstrip()
        return ret_str

    # load settings from an external file
    def load_setting(self):
        try:
            with open(Constants.SETTING_FILENAME, "r") as f:
                setting_list = f.readlines()
        except:
            pass
        if setting_list:
            FIRST_MODIFIERS_KEY = setting_list[0][setting_list[0].find("=") + 1:-1]
            SECOND_MODIFIERS_KEY = setting_list[1][setting_list[1].find("=") + 1:-1]
            MASTER_KEY = setting_list[2][setting_list[2].find("=") + 1:-1]

            return FIRST_MODIFIERS_KEY.lower().lstrip().rstrip(), \
                   SECOND_MODIFIERS_KEY.lower().lstrip().rstrip(), \
                   MASTER_KEY.lower().lstrip().rstrip()
        else:
            return Constants.DEFAULT_FIRST_MODIFIERS_KEY, \
                   Constants.DEFAULT_SECOND_MODIFIERS_KEY, \
                   Constants.DEFAULT_MASTER_KEY

    def save_setting(self):

        NOTIC_HEAD_TEXT = ("# *********************NOTICE***********************\n" +
                          "# Set the key name in the first three lines, please keep the original format.\n" +
                          "# Excess characters may cause errors" )
        write_str = ("FIRST_MODIFIERS_KEY=" + Constants.DEFAULT_FIRST_MODIFIERS_KEY + "\n" +
                     "SECOND_MODIFIERS_KEY=" + Constants.DEFAULT_SECOND_MODIFIERS_KEY + "\n" +
                     "MASTER_KEY=" + Constants.DEFAULT_MASTER_KEY + "\n" + "\n" +
                     NOTIC_HEAD_TEXT + Constants.KEY_NAME_NOTICE
                    )
        try:
            with open(Constants.SETTING_FILENAME, "w") as f:
                f.write(write_str)
        except OSError:
            pass

    # this method is take place of 'locale.getdefaultlocale()'
    # because I don't know why that return None in packaged MacOS app
    def get_sys_encodeing(self):
        mac_external_string_encodings: dict = {1: "Japanese",
                                               2: "ChineseTrad",
                                               3: "Korean",
                                               25: "ChineseSimp"
                                               }
        try:
            hex_encoding = os.environ.get('__CF_USER_TEXT_ENCODING').split(":")[1]
            lang_index = int(hex_encoding, base=16)
        except:
            pass
        return mac_external_string_encodings.get(lang_index, "Other") 

    # if not exist settings file, save one
    if not os.path.isfile(Constants.SETTING_FILENAME):
        save_setting(None)

    # load setting
    FIRST_MODIFIERS_KEY, SECOND_MODIFIERS_KEY, MASTER_KEY = load_setting(None)

    # define Language translator
    lang_dir = os.path.join(os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),
                                    "Resources"), "locale")
    lang = get_sys_encodeing(None)
    if lang == "ChineseSimp":
        translator = gettext.translation("multi_language", localedir = lang_dir, languages = ["zh_CN"])
    elif lang == "ChineseTrad":
        translator = gettext.translation("multi_language", localedir = lang_dir, languages = ["zh_TW"])
    elif lang == "Japanese":
        translator = gettext.translation("multi_language", localedir = lang_dir, languages = ["ja_JP"])
    elif lang == "Korean":
        translator = gettext.translation("multi_language", localedir = lang_dir, languages = ["ko_KR"])
    else:
        translator = gettext.translation("multi_language", localedir=lang_dir, languages=["en_US"])

    translator.install("multi_language")
    _ = translator.gettext

    # set status bar menu text
    first_keyname = order_key_name(None, FIRST_MODIFIERS_KEY)
    second_keyname = order_key_name(None, SECOND_MODIFIERS_KEY)
    master_keyname = order_key_name(None, MASTER_KEY)
    menu_turn_off_display_text = ("🖥 " + _("Turn off display")
                                  + first_keyname + " "
                                  + master_keyname)
    menu_system_sleep_text = ("💡 " + _("System sleep")
                              + first_keyname + " "
                              + second_keyname + " "
                              + master_keyname)
    menu_exit_text = "🏃🏻 " + _("Quit")

    @rumps.clicked(menu_turn_off_display_text)
    def turn_off_display(self, *args):
        KeyboardMonitor.turn_off_display(None)

    @rumps.clicked(menu_system_sleep_text)
    def system_sleep(self, *args):
        KeyboardMonitor.system_sleep(None)

    @rumps.clicked(menu_exit_text)
    def exit(self, *args):
        rumps.quit_application()

# keyboard monitor thread
def run_monitor():
    kb_monitor = KeyboardMonitor()
    listener = keyboard.Listener(on_press=kb_monitor.on_press, on_release=kb_monitor.on_release)
    listener.start()
    listener.join()

if __name__ == "__main__":
    # set threads
    thread_kb_monitor = Thread(target=run_monitor)
    thread_kb_monitor.setDaemon(True)
    status_bar_app = StatusBarApp()
    thread_kb_monitor.start()
    status_bar_app.run()