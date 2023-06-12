# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:45:04 2020

@author: pang
"""

import cv2
import time
import grabscreen


def self_blood_count(self_gray):
    self_blood = 0
    for self_bd_num in self_gray[0]:
        # print(self_bd_num)
        if self_bd_num > 58 and self_bd_num < 63:
            self_blood += 1
    print("player blood:", self_blood)
    return self_blood


def self_endurance_count(endurance_gray):
    endurance_blood = 0
    for endurance_bd_num in endurance_gray[0]:
        #print(endurance_bd_num)
        if endurance_bd_num > 65 and endurance_bd_num < 70:
            endurance_blood += 1
    print("endurance:", endurance_blood)
    return endurance_blood


def boss_blood_count(boss_gray):
    boss_blood = 0
    for boss_bd_num in boss_gray[0]:
        # print(boss_bd_num)
        if boss_bd_num > 27 and boss_bd_num < 30:
            boss_blood += 1
    print("boss blood:", boss_blood)
    return boss_blood


wait_time = 1
L_t = 3

#window_size = (225, 132, 801, 484) # 384,344  192,172 96,86
#window_size = (355, 130 , 675, 402) # 320 272， 160 136， 80 68 ，40 34， 20 17
window_size = (225, 130 , 801, 402) # 576 272， 288 136， 144 68 ，72 34， 36 17
#355 130 655 360 ， 290 230
self_blood_window = (90, 59, 362, 62)
self_endurance_window = (90, 78, 359, 82)
boss_blood_window = (257, 496, 778, 500)

for i in list(range(wait_time))[::-1]:
    print(i + 1)
    time.sleep(1)

last_time = time.time()
while (True):

    screen_gray = cv2.cvtColor(grabscreen.grab_screen(self_blood_window), cv2.COLOR_BGR2GRAY)  # 灰度图像收集
    self_blood = self_blood_count(screen_gray)
    screen_gray2 = cv2.cvtColor(grabscreen.grab_screen(self_endurance_window), cv2.COLOR_BGR2GRAY)  # 灰度图像收集
    endurance_blood = self_endurance_count(screen_gray2)
    screen_gray3 = cv2.cvtColor(grabscreen.grab_screen(boss_blood_window), cv2.COLOR_BGR2GRAY)  # 灰度图像收集
    boss_blood = boss_blood_count(screen_gray3)
    capture_windows = cv2.cvtColor(grabscreen.grab_screen(window_size), cv2.COLOR_BGR2GRAY)  # 灰度图像收集

    cv2.imshow('Self_Blood', screen_gray)
    cv2.imshow('Endurance', screen_gray2)
    cv2.imshow('Boss_Blood', screen_gray3)
    cv2.imshow('Windows', capture_windows)
    # 测试时间用
    print('loop took {} seconds'.format(time.time() - last_time))
    last_time = time.time()

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
cv2.waitKey()  # 视频结束后，按任意键退出
cv2.destroyAllWindows()
