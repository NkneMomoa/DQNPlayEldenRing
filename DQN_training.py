import time

import cv2
import numpy as np
import pandas as pd
import directkeys

from DQN_EldenRing import DQN
from getkeys import key_check
from grabscreen import grab_screen
from restart import restart


def pause_game(paused):
    keys = key_check()
    if 'T' in keys:
        if paused:
            paused = False
            print('start game')
            time.sleep(1)
        else:
            paused = True
            print('pause game')
            time.sleep(1)
    if paused:
        print('paused')
        while True:
            keys = key_check()
            # pauses game and can get annoying.
            if 'T' in keys:
                if paused:
                    paused = False
                    print('start game')
                    time.sleep(1)
                    break
                else:
                    paused = True
                    time.sleep(1)
    return paused


def self_blood_count(self_gray):
    self_blood = 0
    for self_bd_num in self_gray[0]:
        # print(self_bd_num)
        if self_bd_num > 58 and self_bd_num < 63:
            self_blood += 1
    # print("player blood:", self_blood)
    return self_blood


def self_endurance_count(endurance_gray):
    self_endurance = 0
    for endurance_bd_num in endurance_gray[0]:
        # print(endurance_bd_num)
        if endurance_bd_num > 65 and endurance_bd_num < 70:
            self_endurance += 1
    # print("endurance:", self_endurance)
    return self_endurance


def boss_blood_count(boss_gray):
    boss_blood = 0
    for boss_bd_num in boss_gray[0]:
        # print(boss_bd_num)
        if boss_bd_num > 27 and boss_bd_num < 30:
            boss_blood += 1
    # print("boss blood:", boss_blood)
    return boss_blood


def take_action(action):
    if action == 0:  # n_choose
        pass
        print(' ')
    elif action == 1:
        directkeys.attack()
        print('do attack')
    elif action == 2:
        directkeys.jump()
        print('do jump')
    elif action == 3:
        directkeys.go_forward()
        print('do go_forward')
    elif action == 4:
        directkeys.go_right()
        print('do go_right')
    elif action == 5:
        directkeys.go_back()
        print('do go_back')
    elif action == 6:
        directkeys.go_left()
        print('do go_left')
    elif action == 7:
        directkeys.left_dodge()
        print('do left_dodge')
    elif action == 8:
        directkeys.right_dodge()
        print('do right_dodge')
    elif action == 9:
        directkeys.forward_dodge()
        print('do forward_dodge')
    elif action == 10:
        directkeys.back_dodge()
        print('do back_dodge')


def action_judge(boss_blood, next_boss_blood, self_blood, next_self_blood, self_endurance, next_endurance_blood, stop,
                 emergence_break):
    # get action reward
    # emergence_break is used to break down training
    if next_self_blood < 1:  # self dead
        if emergence_break < 1:
            reward = -100
            done = 1
            stop = 0
            emergence_break += 1
            return reward, done, stop, emergence_break
        else:
            reward = -100
            done = 1
            stop = 0
            emergence_break = 100
            return reward, done, stop, emergence_break
    elif next_boss_blood < 10:  # boss dead
        if emergence_break < 2:
            reward = 100
            done = 0
            stop = 0
            emergence_break += 1
            return reward, done, stop, emergence_break
        else:
            reward = 100
            done = 0
            stop = 0
            emergence_break = 100
            return reward, done, stop, emergence_break
    else:
        self_blood_reward = 0
        boss_blood_reward = 0
        endurance_reward = 0
        # print(next_self_blood - self_blood)
        # print(next_boss_blood - boss_blood)
        if next_self_blood - self_blood < -5:
            if stop == 0:
                self_blood_reward = -45
                stop = 1
                # 防止连续取帧时一直计算掉血
        else:
            stop = 0
        if next_boss_blood - boss_blood <= -10:
            boss_blood_reward = 30
        if next_endurance_blood - self_endurance < -3 and next_endurance_blood < 3:  # endurance empty
            endurance_reward = -10
        reward = self_blood_reward + boss_blood_reward + endurance_reward
        done = 0
        emergence_break = 0
        return reward, done, stop, emergence_break


DQN_model_path = "model_gpu"
DQN_loss_path = "loss_gpu/"
WIDTH = 144
HEIGHT = 68
window_size = (225, 130 , 801, 402) # 576 272， 288 136， 144 68 ，72 34， 36 17
# station window_size
self_blood_window = (90, 59, 362, 62)
self_endurance_window = (90, 78, 359, 82)
boss_blood_window = (257, 496, 778, 500)
# used to get boss and self blood

action_size = 11


EPISODES = 500
big_BATCH_SIZE = 30
UPDATE_STEP = 50
# times that evaluate the network
num_step = 0
# used to save loss graph
target_step = 0
# used to update target Q network
paused = True
# used to stop training
df = pd.DataFrame(columns=['episode', 'total_reward', 'target_step', 'Evaluation Average Reward'])

if __name__ == '__main__':
    agent = DQN(WIDTH, HEIGHT, action_size, DQN_model_path, DQN_loss_path)
    # DQN init
    paused = pause_game(paused)
    # paused at the begin
    emergence_break = 0

    # emergence_break is used to break down training
    for episode in range(EPISODES):
        screen_gray = cv2.cvtColor(grab_screen(window_size), cv2.COLOR_BGR2GRAY)
        # collect station gray graph
        blood_window_gray = cv2.cvtColor(grab_screen(self_blood_window), cv2.COLOR_BGR2GRAY)
        endurance_window_gray = cv2.cvtColor(grab_screen(self_endurance_window), cv2.COLOR_BGR2GRAY)
        boss_window_gray = cv2.cvtColor(grab_screen(boss_blood_window), cv2.COLOR_BGR2GRAY)
        # collect blood gray graph for count self and boss blood
        station = cv2.resize(screen_gray, (WIDTH, HEIGHT))
        # change graph to WIDTH * HEIGHT for station input
        boss_blood = boss_blood_count(boss_window_gray)
        self_blood = self_blood_count(blood_window_gray)
        self_endurance = self_endurance_count(endurance_window_gray)
        # count init blood
        target_step = 0
        # used to update target Q network
        done = 0
        total_reward = 0
        stop = 0
        # 用于防止连续帧重复计算reward
        last_time = time.time()
        while True:
            station = np.array(station).reshape(-1, HEIGHT, WIDTH, 1)[0]
            # reshape station for tf input placeholder
            print('loop took {} seconds'.format(time.time() - last_time))
            last_time = time.time()
            target_step += 1
            # take station then the station change
            screen_gray = cv2.cvtColor(grab_screen(window_size), cv2.COLOR_BGR2GRAY)
            # collect station gray graph
            blood_window_gray = cv2.cvtColor(grab_screen(self_blood_window), cv2.COLOR_BGR2GRAY)
            endurance_window_gwray = cv2.cvtColor(grab_screen(self_endurance_window), cv2.COLOR_BGR2GRAY)
            boss_window_gray = cv2.cvtColor(grab_screen(boss_blood_window), cv2.COLOR_BGR2GRAY)
            # get the action by state
            action = agent.Choose_Action(station)
            take_action(action)
            # attack成功率
            #time.sleep(0.1)
            # collect blood gray graph for count self and boss blood
            next_station = cv2.resize(screen_gray, (WIDTH, HEIGHT))
            next_station = np.array(next_station).reshape(-1, HEIGHT, WIDTH, 1)[0]
            next_boss_blood = boss_blood_count(boss_window_gray)
            next_self_blood = self_blood_count(blood_window_gray)
            next_endurance = self_endurance_count(endurance_window_gray)
            reward, done, stop, emergence_break, = action_judge(boss_blood, next_boss_blood,
                                                               self_blood, next_self_blood,
                                                               self_endurance, next_endurance,
                                                               stop, emergence_break)
            # get action reward
            if emergence_break == 100:
                # emergence break , save model and paused
                # 遇到紧急情况，保存数据，并且暂停
                print("emergence_break")
                agent.save_model()
                paused = True
            agent.Store_Data(station, action, reward, next_station, done)
            if len(agent.replay_buffer) > big_BATCH_SIZE:
                num_step += 1
                # save loss graph
                # print('train')
                agent.Train_Network(big_BATCH_SIZE, num_step)
            if target_step % UPDATE_STEP == 0:
                agent.Update_Target_Network()
                # update target Q network
            station = next_station
            self_blood = next_self_blood
            boss_blood = next_boss_blood
            self_endurance = next_endurance
            total_reward += reward
            paused = pause_game(paused)
            if done == 1:
                print("You Dead, wait the countdown to restart")
                for i in list(range(25))[::-1]:
                    time.sleep(1)
                restart()
                paused = False
                break
        if episode % 5 == 0:
            agent.save_model()
            # save model
        df.loc[episode] = {'episode': episode, 'total_reward': total_reward, 'target_step': target_step, 'Evaluation Average Reward': total_reward / target_step}
        print(df)
        df.to_csv("C:/Users/Momoa/PycharmProjects/pythonProject/Elden Ring/reward/reward_info.csv", encoding='utf-8', index=False)
