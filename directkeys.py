import ctypes
import time

SendInput = ctypes.windll.user32.SendInput
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
M = 0x32
J = 0x24
K = 0x25
E = 0x12
Space = 0x39
LSHIFT = 0x2A
R = 0x13
V = 0x2F
Q = 0x10
I = 0x17
O = 0x18
P = 0x19
C = 0x2E
F = 0x21
up = 0xC8
down = 0xD0
left = 0xCB
right = 0xCD
esc = 0x01

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def heavy_attack():
    PressKey(O)
    time.sleep(0.05)
    ReleaseKey(O)
    # time.sleep(0.1)


def certain():
    PressKey(E)
    time.sleep(0.05)
    ReleaseKey(E)
    # time.sleep(0.1)

def doleft():
    PressKey(left)
    time.sleep(0.05)
    ReleaseKey(left)
    # time.sleep(0.1)

def attack():
    PressKey(I)
    time.sleep(0.5)
    ReleaseKey(I)
    #time.sleep(0.2)

def go_forward():
    PressKey(W)
    time.sleep(0.4)
    ReleaseKey(W)


def go_back():
    PressKey(S)
    time.sleep(0.4)
    ReleaseKey(S)


def go_left():
    PressKey(A)
    time.sleep(0.4)
    ReleaseKey(A)


def go_right():
    PressKey(D)
    time.sleep(0.4)
    ReleaseKey(D)


def jump():
    PressKey(F)
    time.sleep(0.1)
    ReleaseKey(F)
    #time.sleep(0.3)


def dodge():  # 闪避
    PressKey(Space)
    time.sleep(0.1)
    ReleaseKey(Space)
    # time.sleep(0.1)


def lock_vision():
    PressKey(Q)
    time.sleep(0.3)
    ReleaseKey(Q)
    time.sleep(0.1)


def go_forward_QL(t):
    PressKey(W)
    time.sleep(t)
    ReleaseKey(W)


def go_right_QL(t):
    PressKey(D)
    time.sleep(t)
    ReleaseKey(D)


def forward_jump(t):
    PressKey(W)
    time.sleep(t)
    PressKey(F)
    ReleaseKey(W)
    ReleaseKey(F)


def left_dodge():
    PressKey(A)
    PressKey(Space)
    time.sleep(0.2)
    ReleaseKey(Space)
    time.sleep(0.2)
    ReleaseKey(A)
    #time.sleep(0.2)


def right_dodge():
    PressKey(D)
    PressKey(Space)
    time.sleep(0.2)
    ReleaseKey(Space)
    time.sleep(0.2)
    ReleaseKey(D)
    #time.sleep(0.2)

def forward_dodge():
    PressKey(W)
    PressKey(Space)
    time.sleep(0.2)
    ReleaseKey(Space)
    time.sleep(0.2)
    ReleaseKey(W)
    #time.sleep(0.2)


def back_dodge():
    PressKey(S)
    PressKey(Space)
    time.sleep(0.2)
    ReleaseKey(Space)
    time.sleep(0.2)
    ReleaseKey(S)
    #time.sleep(0.2)


def press_esc():
    PressKey(esc)
    time.sleep(0.3)
    ReleaseKey(esc)


# if __name__ == '__main__':
#      time.sleep(5)
#      time1 = time.time()
#      while(True):
#          if abs(time.time()-time1) > 5:
#              break
# #         else:
# #             PressKey(M)
# #             time.sleep(0.1)
# #             ReleaseKey(M)
# #             time.sleep(0.2)
# #
# #
# #