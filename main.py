import pyautogui
import os
import time
import random
import ctypes
import sys
import threading
import win32gui
import win32con
import win32api
from pynput import keyboard
#from threading import Thread
# 保护措施，避免失控
pyautogui.FAILSAFE = True
# 为所有的PyAutoGUI函数增加延迟。默认延迟时间是0.1秒。
pyautogui.PAUSE = 0.1
# 文件路径
path3 = "chosen.png"
path4 = "pause.png"
path5 = "talking.png"
coldInitFlag = False

# 各阶段停留时间，单位秒
waitTime_Talk = 0.5
waitTime_optionClick = 3.0
waitTime_noDialogClick = 2.0
waitTime_dialogClick = 1.0

# 点击时间混淆
timeFilter = 0.002

# 自动点击的速度等级, 1最慢, 5最快
SpdLevel = 3
SpdLevelTable = [1, 2, 4, 6, 8, 10, 12, 14, 30, 50]

# log是否需打印:0:false,1:true
logLevel = 0

# 原神启动标志
yuanshenRunning = False
lock = threading.Lock()

# 快捷键判断是否开启脚本
enableFlag = False


class timerThread(threading.Thread):
    def run(self):
        while (True):
            isRunning()
            time.sleep(12)

# 每15秒检测一次原神是否启动或已被最小化


def isRunning():
    global yuanshenRunning
    # process = len(os.popen('''tasklist | findstr YuanShen.exe''').readlines())
    # print(process)
    window = win32gui.FindWindow(None, "崩坏：星穹铁道")
    minimized = True
    if window:
        tup = win32gui.GetWindowPlacement(window)
        if tup[1] == win32con.SW_SHOWMINIMIZED:
            minimized = True
        else:
            minimized = False

    lock.acquire()
    if (False == minimized):
        yuanshenRunning = True
    else:
        yuanshenRunning = False
    lock.release()
    if (False == yuanshenRunning):
        logPrint("游戏未启动")


def logPrint(strlog):
    global logLevel
    if (0 != logLevel):
        print(strlog)


def wait(x):
    logPrint("等待 " + str(x) + "s")
    tep = int(x * 10)
    for i in range(0, tep):
        # logPrint(i + 1)
        time.sleep(0.1)


def getFilteredTime(x, deltaTime=5, xFilter=1.0):
    return x + timeFilter * random.randint(-deltaTime, deltaTime) * xFilter


def click():
    try:
        coords = pyautogui.locateOnScreen(path3, confidence=0.8)
        coords2 = pyautogui.locateOnScreen(path5, confidence=0.8)
        if (coords2 is not None):
            if(coords is not None):
                xy = pyautogui.center(coords)
                logPrint("已找到对话选项")
                wait(getFilteredTime(waitTime_Talk))  # 等waitTime秒把话说完
                pyautogui.moveTo(
                    x=getFilteredTime(
                        xy.x, 20, 100), y=getFilteredTime(
                        xy.y, 2, 100), duration=getFilteredTime(
                        0.2, 1))
                pyautogui.click()
                logPrint("已点击选项")
                return 1
            else:
                xy2 = pyautogui.center(coords2)
                logPrint("已找到对话框")
                wait(getFilteredTime(waitTime_Talk))  # 等waitTime秒把话说完
                tx = getFilteredTime(xy2.x - 450,500,100)
                ty = getFilteredTime(xy2.y + 300,100,100)
                pyautogui.moveTo(
                    x=tx,
                    y=ty,
                    duration=getFilteredTime(0.2, 1))
                pyautogui.mouseDown()
                time.sleep(0.05)
                pyautogui.mouseUp() 
                print("已点击对话框，加速对话")
                return 2

    except BaseException:
        print("程序出错了")   
        logPrint("未找到对话")
        return 0


def creatCfgFile():
    global coldInitFlag
    global SpdLevel
    global logLevel
    if (os.path.exists("Genshin.cfg")):
        coldInitFlag = False
        file = open(".\\Genshin.cfg", "r")
        strLines = file.readlines()
        for strLine in strLines:
            if (strLine.split("Speed=")[0].strip() == "" and int(
                    strLine.strip().split("Speed=")[1]) in range(1, 6)):
                SpdLevel = int(strLine.split("Speed=")[1].strip())
                continue
            if (strLine.split("log=")[0].strip() == "" and int(
                    strLine.strip().split("log=")[1]) in range(0, 2)):
                logLevel = int(strLine.split("log=")[1].strip())
                continue
        file.close()
    else:
        coldInitFlag = True
        file = open(".\\Genshin.cfg", "w+")
        file.write(f"#可配置10种点击速度档，1最慢，10最快,在Speed=后加数字即可配置\n")
        file.write("Speed=3\n")
        file.write("log=0\n")
        file.close()
    return coldInitFlag


def iniCfg():
    global waitTime_Talk
    global waitTime_optionClick
    global waitTime_noDialogClick
    global waitTime_dialogClick
    waitTime_Talk /= SpdLevelTable[SpdLevel - 1]
    waitTime_optionClick /= SpdLevelTable[SpdLevel - 1]
    waitTime_noDialogClick /= SpdLevelTable[SpdLevel - 1]
    waitTime_dialogClick /= SpdLevelTable[SpdLevel - 1]


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except BaseException:
        return False


# 以管理员身份运行
if is_admin():
    pass
else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)


def main():
    global enableFlag

    creatCfgFile()
    op = "OK"
    iniCfg()
    on_activate()
    if (coldInitFlag):
        op = pyautogui.confirm(
            text=f'请将游戏分辨率调整为1366*768，\n确认后将自动进行剧情对话点击\n本程序目录{os.getcwd()}下Genshin.cfg文件可配置点击速度\n默认速度等级:2',
            title='崩铁剧情小助手',
            buttons=[
                'OK',
                'Cancel'])
    scanTimer = timerThread()
    scanTimer.start()

    if (op == 'OK'):
        while (True):
            c = 0xFF
            # 只有在原神启动且脚本激活时才进行对话检测
            if (True == yuanshenRunning and enableFlag):
                c = click()
            else:
                time.sleep(2)
            # 点到对话选项(1)或者对话框(2)之后x秒
            if (1 == c):
                wait(getFilteredTime(waitTime_optionClick))
            elif (2 == c):
                wait(getFilteredTime(waitTime_dialogClick))
            else:
                wait(getFilteredTime(waitTime_noDialogClick))
    else:
        pyautogui.alert(text='感谢您的使用，再见', title='原神剧情小助手', button='OK')

def on_activate():
    global enableFlag
    enableFlag = not enableFlag
    if True == enableFlag:
        print('助手状态: 已开启, 可按 Ctrl+Shift+9 关闭')
    else:
        print('助手状态: 已关闭, 可按 Ctrl+Shift+9 开启')


def for_canonical(f):
    return lambda k: f(l.canonical(k))

if __name__ == '__main__':
    mThread = threading.Thread(target=main)
    mThread.start()
    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<shift>+9'), on_activate)
    with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)
    ) as l:
        {l.join()}
    mThread.join()
