import numpy as np
import cv2 as cv
from win32api import GetSystemMetrics
import keyboard
import matplotlib.pyplot as plt

def get_optimal_font_scale(text, width):
    for scale in reversed(range(0, 150, 1)):
        textSize = cv.getTextSize(text, fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=scale/10, thickness=1)
        new_width = textSize[0][0]
        if (new_width <= width):
            print(new_width)
            return scale/10
    return 1

res = (GetSystemMetrics(0), GetSystemMetrics(1))
writer= cv.VideoWriter('basicvideo.mp4', cv.VideoWriter_fourcc(*'DIVX'), 60, res)
loading_screen = cv.resize(cv.imread('loading screen.png'), res)
center = (loading_screen.shape[0], loading_screen.shape[1])
color = np.array([100, 100, 100])
while True:
    cv.imshow('', loading_screen)
    cv.waitKey(1)
    writer.write(loading_screen)
    if keyboard.is_pressed('w'):
        break
background = cv.resize(cv.imread('Boston_harboar.png'), res)
counter = 0
turns = 0
color = np.array([124,252,0])
indian = cv.imread('the man.png')
man = indian[63:730,265:430]
k = (res[0] // 3) / man.shape[0]
man = cv.resize(man, (int(k * man.shape[1]), int(k * man.shape[0])))
arm = indian[232:392, 568:713]
arm = cv.resize(arm, (int(k * arm.shape[1]), int(k * arm.shape[0])))
leg = indian[498:687, 599:696]
leg = cv.resize(leg, (int(k * leg.shape[1]), int(k * leg.shape[0])))
crate = cv.resize(cv.imread('crate.png'), res)[int(176 *res[1] / 825) : int(548 * res[1] / 825), int(371 * res[0] / 1914) : int(746 * res[0] / 1914), :]
crate_pos = res[1] + int(np.random.random(1) * (background.shape[1] - crate.shape[1]))
background1 = np.concatenate((background.copy(), background.copy(), background.copy()), axis = 1)
background1[int(0.35 * background.shape[0]):crate.shape[0] + int(0.35 * background.shape[0]), crate_pos:crate_pos + crate.shape[1], :] = crate
answers = ['C', "A", 'B', 'C', 'A', 'A', 'B', 'C']
i = 1
while True:
    if counter == 2 * background.shape[1] - 2:
        counter = 0
        crate_pos = res[1] + int(np.random.random(1) * (background.shape[1] - crate.shape[1]))
        background1 = np.concatenate((background.copy(), background.copy(), background.copy()), axis = 1)
        background1[int(0.35 * background.shape[0]):crate.shape[0] + int(0.35 * background.shape[0]), crate_pos:crate_pos + crate.shape[1], :] = crate
    background2 = background1.copy()
    background2[int(1/3 * background.shape[0]) : int(1/3 * background.shape[0]) + man.shape[0], int(1/5 * background.shape[1]) + counter : int(1/5 * background.shape[1]) + man.shape[1] + counter] *= np.uint8(man == 0)
    background2[int(1/3 * background.shape[0]) : int(1/3 * background.shape[0]) + man.shape[0], int(1/5 * background.shape[1]) + counter : int(1/5 * background.shape[1]) + man.shape[1] + counter] += np.uint8(man)
    if (counter // 100) % 2 == 1:
        background2[int(1/3 * background.shape[0]) + int(man.shape[0] // 3.5): int(1/3 * background.shape[0]) + int(man.shape[0] // 3.5) + arm.shape[0], int(1/5 * background.shape[1]) + int(0.75 * man.shape[1]) + counter:int(1/5 * background.shape[1]) + int(0.75 * man.shape[1]) + counter + arm.shape[1], :] *= np.uint8(arm == 0)
        background2[int(1/3 * background.shape[0]) + int(man.shape[0] // 3.5): int(1/3 * background.shape[0]) + int(man.shape[0] // 3.5) + arm.shape[0], int(1/5 * background.shape[1]) + int(0.75 * man.shape[1]) + counter:int(1/5 * background.shape[1]) + int(0.75 * man.shape[1]) + counter + arm.shape[1], :] += np.uint8(arm)
        background2[int(1/3 * background.shape[0]) + man.shape[0] - leg.shape[0]: int(1/3 * background.shape[0]) + man.shape[0], int(1/5 * background.shape[1]) + int(0.75 * man.shape[1]) + counter:int(1/5 * background.shape[1]) + int(0.75 * man.shape[1]) + counter + leg.shape[1], :] *= np.uint8(leg == 0)
        background2[int(1/3 * background.shape[0]) + man.shape[0] - leg.shape[0]: int(1/3 * background.shape[0]) + man.shape[0], int(1/5 * background.shape[1]) + int(0.75 * man.shape[1]) + counter:int(1/5 * background.shape[1]) + int(0.75 * man.shape[1]) + counter + leg.shape[1], :] += np.uint8(leg)
    screen = background2[:, counter: counter + background.shape[1], :]
    if res[1] > crate_pos - counter >= 0:
        question = cv.resize(cv.imread('question' + str(i) + '.png'), (screen.shape[1] // 4, screen.shape[0] // 4))
        screen[:question.shape[0], :question.shape[1]] = question
        if keyboard.is_pressed('a'):
            if answers[i - 1] == 'A':
                screen[:int(0.1*screen.shape[0]),int(0.9 * screen.shape[1]):, :] = color
        if keyboard.is_pressed('b'):
            if answers[i - 1] == 'B':
                screen[:int(0.1*screen.shape[0]),int(0.9 * screen.shape[1]):, :] = color
        if keyboard.is_pressed('c'):
            if answers[i - 1] == 'C':
                screen[:int(0.1*screen.shape[0]),int(0.9 * screen.shape[1]):, :] = color
        if keyboard.is_pressed('d'):
            if answers[i - 1] == 'D':
                screen[:int(0.1*screen.shape[0]),int(0.9 * screen.shape[1]):, :] = color
    if 0 == crate_pos - counter:
        i += 1
    cv.imshow('', screen)
    cv.waitKey(1)
    writer.write(np.uint8(screen))
    counter += 1
    
    if keyboard.is_pressed('q'):
        break
write.release()