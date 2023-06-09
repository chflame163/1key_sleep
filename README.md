# 1key_sleep
A app for MacOS that press the shortcut key to turn off display / system sleep. 
Release v1.0.2 support the menu language with English，Simplified Chinese, Traditional Chinese, Japanese and Korean.

## How to use?
When this program is running, press the shortcut key will trigger the following functions:  
- press CONTROL + F15 to Turn off display  
- press CONTROL + OPTION + F15 to System sleep  

At the same time, the "Moon" icon displayed in the MacOS system status bar, the menu appears by clicking on it:  
- "Turn off display"  
- "System sleep"  
- "Quit"  

Clicking on the menu also triggers the corresponding function.  

Default FIRST_MODIFIERS_KEY are defined to 'CONTROL', SECOND_MODIFIERS_KEY defined to 'OPTION', and MASTER_KEY defined to 'F15'. you can change it by yourself. 

Note: When running the app for the first time, a pop-up message will prompt '1KeySleep' to receive buttons from any application program. At this time, 'System Preferences' should be opened, Allow 1KeySleep in the 'Security and Privacy' - 'Privacy' - 'Input Listening' and 'Auxiliary Functions' columns (check after unlocking)

It is recommended to add an app to the 'System Preferences' -' Users and Groups' - 'Login Items' to automatically launch this program with the system.

## Shortcut customization:

- Modifiers key should be one of CONTROL / OPTION / COMMAND / SHIFT

- Master key can be any

For the packaged app, right-click on the file icon "Display Package Content" - Contents Resources and find keysetting.cfg, Open this file with a text editor, modify the key values in the first three lines, save, and then run again.  

For the py file, keysetting.cfg will be generated in the folder "../Resources" during the first run.  

Another method is to directly modify the key definitions in the py source code, which are located in <class Constants>, but the external config file will be read first when program running, so you need delete the external file 'keysetting.cfg' before run it.
