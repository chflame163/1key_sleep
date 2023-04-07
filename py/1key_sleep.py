"""
****Mac版一键睡眠, 用快捷键实现关闭显示器/系统睡眠****

按快捷键将触发以下功能：
"FIRST_FUNCTION_KEY" + "MASTER_KEY" = "关闭显示器"
"FIRST_FUNCTION_KEY" + "SECOND_FUNCTION_KEY" + "MASTER_KEY" = "系统睡眠"
同时在Mac OS系统状态栏显示"月亮"图标，点击出现菜单："关闭显示器"、"系统睡眠"、"退出"，
点击菜单亦触发对应功能。
注：初次运行app时，弹窗提示'"1KeySleep"想接收来着任何应用程序的按键'，此时应打开'系统偏好设置'，
   在'安全性与隐私'-'隐私'-'输入监听'和'辅助功能'栏目中允许1KeySleep(解锁后勾选)
   建议在'系统偏好设置'-'用户与群组'-'登录项'中加入app，随系统自动启动本程序。

快捷键自定义：
FUNCTION_KEY 应为 control / option / command / shift 其中之一，
MASTER_KEY 则可以是任何键。
对于打包的app， 右键点击-"显示包内容"-Contents-Resources，找到keysetting.cfg，
用'文本编辑'打开这个文件，修改前三行的键值，保存然后重新运行。
对于py文件，keysetting.cfg将在首次运行时生成于文件夹"../Resources"下。
另一种方法是直接修改py代码中的按键定义，这些定义位于<class Constants>，
外部文件会优先读取，因此，如果想让py文件的设定生效，需先删除外部的keysetting.cfg文件。

MacOs Bigsur 11.6.8 + Python 3.8.3 + pyinstaller 5.9.0 编译app通过
(c) 2023 by CHFLAME, email:chflame@163.com
"""

import os
import sys
from threading import Thread
from pynput import keyboard
import rumps

# 设置常量
class Constants:
    KEY_NAME_NOTICE = """
# 请按下列键名设置按键
# 
# 字母和数字用单引号包围:
# 'a'  'b' ... '1'  '2' ...
# 符号用单引号包围(除特殊字符外):
# '`'  '='  '['  ';'  ','  '/' ...
# 特殊字符:
# 反斜杠需转义并用单引号包围: '\\\\'
# 单引号用双引号包围: "'"
#
# 以下键名无需加引号
# 功能修饰键(两侧等同): 
# control键: Key.ctrl
# option键: Key.alt
# command键: Key.cmd
# shift键: Key.shift
# 
# F键(PrtSc, ScrLk, Pause在Mac中被识别为F13, F14, F15): 
# Key.f1  Key.f2 ... Key.f15
# 
# 其他键: 
# Key.page_up  Key.page_down  Key.home  Key.end  Key.insert  Key.delete
# Key.up  Key.down  Key.left  Key.right  key.tab  Key.caps_lock
# Key.backspace  Key.esc  Key.space  Key.enter  Key.pad_enter  
#
# 以下键不确定能否触发
# NumLock, fn, 以及其他不在上述范围内的的按键
"""
    # 默认按键
    DEFAULT_FIRST_FUNCTION_KEY = "Key.ctrl"
    DEFAULT_SECOND_FUNCTION_KEY = "Key.alt"
    DEFAULT_MASTER_KEY = "Key.f15"

    # 保存设置文件名
    SETTING_FILENAME = os.path.join(os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),
                         "Resources"), "keysetting.cfg")
    # 图标文件名
    ICON_FILENAME = os.path.join(os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),
                        "Resources"), "1KeySleep.icns")

# 判断按键事件，睡眠函数
class KeyboardMonitor:

    # Ctrl键按下标识变量
    FIRST_FUNCTION_KEY_press:bool = False
    SECOND_FUNCTION_KEY_press:bool = False

    # 键按下
    def on_press(self, key):
        print(key)
        print(self.FIRST_FUNCTION_KEY_press,self.SECOND_FUNCTION_KEY_press)
        press_key = str(key)
        # 处理右修饰键
        if press_key.endswith("_r"):
            press_key = press_key.replace("_r", "")
        # 处理insert
        elif press_key == "'\\x05'":
            press_key = "Key.insert"
        # 处理小键盘enter
        elif press_key == "'\\x03'":
            press_key = "Key.pad_enter"

        if press_key == StatusBarApp.MASTER_KEY and self.FIRST_FUNCTION_KEY_press \
                and self.SECOND_FUNCTION_KEY_press:
            self.system_sleep()
        elif press_key == StatusBarApp.MASTER_KEY and self.FIRST_FUNCTION_KEY_press:
            self.turn_off_display()
        elif press_key == StatusBarApp.FIRST_FUNCTION_KEY:
            self.FIRST_FUNCTION_KEY_press = True
        elif press_key == StatusBarApp.SECOND_FUNCTION_KEY:
            self.SECOND_FUNCTION_KEY_press = True

    # 键弹起
    def on_release(self, key):
        release_key = str(key)
        if release_key.endswith("_r"):
            release_key = release_key.replace("_r", "")
        if release_key == StatusBarApp.FIRST_FUNCTION_KEY:
            self.FIRST_FUNCTION_KEY_press = False
        elif release_key == StatusBarApp.SECOND_FUNCTION_KEY:
            self.SECOND_FUNCTION_KEY_press = False

    # 系统睡眠
    def system_sleep(self):
        os.system("pmset sleepnow")

    # 关闭显示器
    def turn_off_display(self):
        os.system("pmset displaysleepnow")


# 状态栏菜单
class StatusBarApp(rumps.App):

    def __init__(self):
        super(StatusBarApp, self).__init__("1KeySleep",
                icon=Constants.ICON_FILENAME, quit_button=None)

    # 用于显示的键名
    def order_key_name(self, keyname:str) -> str:
        ret_str =  keyname.replace("Key.", ""
                        ).replace("_r", ""
                        ).replace("'", ""
                        ).replace("cmd", "⌘"
                        ).replace("ctrl", "⌃"
                        ).replace("alt", "⌥"
                        ).replace("shift", "⇧"
                        ).title().rstrip()
        # 处理单引号
        if keyname == '''"'"''':
            ret_str = "'"
        elif keyname == "'\\x05'":
            ret_str = "insert"
        elif keyname == "'\\x03'":
            ret_str = "pad_enter"
        return ret_str

    # 从外部文件读取设置
    def load_setting(self):
        try:
            with open(Constants.SETTING_FILENAME, "r") as f:
                setting_list = f.readlines()
                print("success load settings")
        except:
            print(".cfg file not found!")
            pass
        if setting_list:
            FIRST_FUNCTION_KEY = setting_list[0][setting_list[0].find("=") + 1:-1]
            SECOND_FUNCTION_KEY = setting_list[1][setting_list[1].find("=") + 1:-1]
            MASTER_KEY = setting_list[2][setting_list[2].find("=") + 1:-1]

            return FIRST_FUNCTION_KEY, \
                   SECOND_FUNCTION_KEY, \
                   MASTER_KEY
        else:
            return Constants.DEFAULT_FIRST_FUNCTION_KEY, \
                   Constants.DEFAULT_SECOND_FUNCTION_KEY, \
                   Constants.DEFAULT_MASTER_KEY

    def save_setting(self):
        write_str = ("FIRST_FUNCTION_KEY=" + Constants.DEFAULT_FIRST_FUNCTION_KEY + "\n" +
                     "SECOND_FUNCTION_KEY=" + Constants.DEFAULT_SECOND_FUNCTION_KEY + "\n" +
                     "MASTER_KEY=" + Constants.DEFAULT_MASTER_KEY + "\n" + "\n" +
                     "# *********************NOTICE***********************\n"
                     "# 本文件前3行设置按键，保持原有格式，多余字符可能导致软件错误" +
                     Constants.KEY_NAME_NOTICE
                    )
        try:
            with open(Constants.SETTING_FILENAME, "w") as f:
                f.write(write_str)
                print("success save settings")
        except:
            print("save failed")
            pass

    # 如果没有设置文件则保存一个
    if not os.path.isfile(Constants.SETTING_FILENAME):
        save_setting(None)

    # 读取设置
    FIRST_FUNCTION_KEY, SECOND_FUNCTION_KEY, MASTER_KEY = load_setting(None)
    print(FIRST_FUNCTION_KEY,SECOND_FUNCTION_KEY,MASTER_KEY)
    # 设置任务栏菜单显示文字
    first_keyname = order_key_name(None, FIRST_FUNCTION_KEY)
    second_keyname = order_key_name(None, SECOND_FUNCTION_KEY)
    master_keyname = order_key_name(None, MASTER_KEY)

    menu_turn_off_display_text = ("🖥关闭显示器     "
                                  + first_keyname + " "
                                  + master_keyname)
    menu_system_sleep_text = ("💡系统睡眠         "
                              + first_keyname + " "
                              + second_keyname + " "
                              + master_keyname)
    menu_exit_text = "🏃🏻退出"

    @rumps.clicked(menu_turn_off_display_text)
    def turn_off_display(self, *args):
        KeyboardMonitor.turn_off_display(None)

    @rumps.clicked(menu_system_sleep_text)
    def system_sleep(self, *args):
        KeyboardMonitor.system_sleep(None)

    @rumps.clicked(menu_exit_text)
    def exit(self, *args):
        rumps.quit_application()

# 后台键盘监控线程
def run_monitor():
    kb_monitor = KeyboardMonitor()
    listener = keyboard.Listener(on_press=kb_monitor.on_press, on_release=kb_monitor.on_release)
    listener.start()
    listener.join()

if __name__ == "__main__":
    # 设置线程
    thread_kb_monitor = Thread(target=run_monitor)
    thread_kb_monitor.setDaemon(True)
    status_bar_app = StatusBarApp()
    thread_kb_monitor.start()
    status_bar_app.run()