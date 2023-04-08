# 1key_sleep
Press shotcut key to sleep system or turn off display, on MacOS.
 
Release v1.0.2 support the menu language with English，Simplified Chinese, Traditional Chinese, Japanese and Korean.

## How to use?
When this program is running, press the shortcut key will trigger the following functions:

FIRST-FUNCTION_KEY+MASTER_KEY="Turn off display"

"FIRSTFUNCTION_KEY"+"SECOND_FUNCTION_KEY"+"MASTER_KEY"="System sleep"

At the same time, the "Moon" icon is displayed in the MacOS system status bar, 
and the menu appears by clicking on it: "Turn off display", "System sleep", "Exit",

Clicking on the menu also triggers the corresponding function.

Note: When running the app for the first time, a pop-up message will prompt '1KeySleep' to receive buttons from any application program. At this time, 'System Preferences' should be opened,

Allow 1KeySleep in the 'Security and Privacy' - 'Privacy' - 'Input Listening' and 'Auxiliary Functions' columns (check after unlocking)

It is recommended to add an app to the 'System Preferences' -' Users and Groups' - 'Login Items' to automatically launch this program with the system.

## Shortcut customization:

FUNCTION_ KEY should be one of control/option/command/shift,

MASTER_ KEY can be any key.

For the packaged app, right-click on "Display Package Content" - Contents Resources and find keysetting.cfg,

Open this file with 'text editing', modify the key values in the first three lines, save, and then run again.

For the py file, keysetting.cfg will be generated in the folder "../Resources" during the first run.

Another method is to directly modify the key definitions in the py code, which are located in<class Constants>,

External files will be read first, so if you want the settings of the py file to take effect, you need to first delete the external keysetting.cfg file.