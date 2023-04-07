"""
Windows 一键睡眠
ctrl + pause(scrlock) = 关闭显示器
ctrl + menu + pause(scrlock) = 系统睡眠

"""

import win32api
import win32security
from pynput import keyboard
from ctypes import windll

class Constant:
    # 设置按键
    DEFAULT_FIRST_FUNCTION_KEY = "Key.ctrl"
    DEFAULT_SECOND_FUNCTION_KEY = "Key.menu"
    # ctrl+pause or scrlock
    DEFAULT_MASTER_KEY = "<3>"

# 判断按键事件
class KeyboardMonitor:

    # 修饰键按下变量
    first_function_key_press:bool = False
    second_function_key_press:bool = False

    def on_press(self, key):
        # print(key)
        press_key = str(key)
        # 左右ctrl键同等
        if press_key.endswith("_r"):
            press_key = press_key.replace("_r", "")
        elif press_key.endswith("_l"):
            press_key = press_key.replace("_l", "")

        # 如果满足条件，执行睡眠任务
        if press_key == Constant.DEFAULT_MASTER_KEY and self.first_function_key_press and self.second_function_key_press:
            self.suspend(True)
        elif press_key == Constant.DEFAULT_MASTER_KEY and self.first_function_key_press:
            self.screen_off()
        # 设置修饰键变量
        elif press_key == Constant.DEFAULT_FIRST_FUNCTION_KEY:
            self.first_function_key_press = True
        elif press_key == Constant.DEFAULT_SECOND_FUNCTION_KEY:
            self.second_function_key_press = True

    def on_release(self, key):
        release_key = str(key)
        # 左右ctrl键同等
        if release_key.endswith("_r"):
            release_key = release_key.replace("_r", "")
        elif release_key.endswith("_l"):
            release_key = release_key.replace("_l", "")
        # 设置修饰键变量复原
        if release_key == Constant.DEFAULT_FIRST_FUNCTION_KEY:
            self.first_function_key_press = False
        if release_key == Constant.DEFAULT_SECOND_FUNCTION_KEY:
            self.second_function_key_press = False

    # 系统睡眠
    def suspend(self, hibernate=False):
        priv_flags = (win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY)
        hToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), priv_flags)
        priv_id = win32security.LookupPrivilegeValue(None, win32security.SE_SHUTDOWN_NAME)
        old_privs = win32security.AdjustTokenPrivileges(hToken, 0,
                    [(priv_id, win32security.SE_PRIVILEGE_ENABLED)])
        try:
            windll.powrprof.SetSuspendState(not hibernate, True, False)
        except:
            win32api.SetSystemPowerState(not hibernate, True)
        win32security.AdjustTokenPrivileges(hToken, 0, old_privs)

    # 显示器睡眠
    def screen_off(self):
        windll.user32.PostMessageW(0xffff, 0x0112, 0xF170, 2)
        shell32 = windll.LoadLibrary("shell32.dll")
        shell32.ShellExecuteW(None, 'open', 'rundll32.exe', 'USER32,LockWorkStation', '', 5)

# 后台按键监控
def run_monitor():
    k = KeyboardMonitor()
    listener = keyboard.Listener(on_press=k.on_press, on_release=k.on_release)
    listener.start()
    listener.join()

if __name__ == "__main__":

    # 运行按键监控
    run_monitor()
