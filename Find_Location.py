import win32gui
import win32ui
import win32con
import win32api
import time
def findTitle(window_title):
    '''
    查找指定标题窗口句柄
    @param window_title: 标题名
    @return: 窗口句柄
    '''
    hWndList = []
    # 函数功能：该函数枚举所有屏幕上的顶层窗口，办法是先将句柄传给每一个窗口，然后再传送给应用程序定义的回调函数。
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for hwnd in hWndList:
        # 函数功能：该函数获得指定窗口所属的类的类名。
        # clsname = win32gui.GetClassName(hwnd)
        # 函数功能：该函数将指定窗口的标题条文本（如果存在）拷贝到一个缓存区内
        title = win32gui.GetWindowText(hwnd)
        if (title == window_title):
            print("标题：", title, "句柄：", hwnd)
            break
    return hwnd

window_title =  u'笑傲江湖[19:00正式开区]'
hwnd = findTitle(window_title)
print(hwnd)

while True:
    #   GetCursorPos 获取鼠标指针的当前位置
    p = win32api.GetCursorPos()
    print(p[0],p[1])
    #  GetWindowRect 获得整个窗口的范围矩形，窗口的边框、标题栏、滚动条及菜单等都在这个矩形内
    x,y,w,h = win32gui.GetWindowRect(hwnd)
    # 鼠标坐标减去指定窗口坐标为鼠标在窗口中的坐标值
    pos_x = p[0] - x
    pos_y = p[1] - y
    print(pos_x,pos_y)
    time.sleep(0.5)

