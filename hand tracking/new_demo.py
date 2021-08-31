import cv2
import mediapipe as mp
import time
import math
import threading
import pyautogui

cap = cv2.VideoCapture(0)
pyautogui.PAUSE = 0.01
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_tracking_confidence=0.95, min_detection_confidence=0.90)
mpDraw = mp.solutions.drawing_utils
mov_dis = 0.2379
click_dis = 0.2823
sensitivity = 3.5

testing8_12 = []
testing0_5 = []

testing3_5 = []

def get_distance(first, second, height, width):
    dist_x = (results.multi_hand_landmarks[0].landmark[first].x - results.multi_hand_landmarks[0].landmark[
        second].x) * width
    dist_y = (results.multi_hand_landmarks[0].landmark[first].y - results.multi_hand_landmarks[0].landmark[
        second].y) * height
    return math.sqrt(abs(dist_x ** 2 + dist_y ** 2))

def dist(point1, point2, pointa, pointb, pointc, pointd):
    dis12 = get_distance(point1, point2, h, w)
    distab = get_distance(pointa, pointb, h, w)
    distcd = get_distance(pointc, pointd, h, w)
    testing8_12.append(dis12)
    testing0_5.append(distab)
    testing3_5.append(distcd)
    print(f"8-12:  {round(sum(testing8_12)/len(testing8_12), 2)} | 0-5  {round(sum(testing0_5)/len(testing0_5), 2)} | 3-5  {round(sum(testing3_5)/len(testing3_5), 2)}")



x, y = None, None
click = False

while True:
    success, img = cap.read()
    h, w, c = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        dist_palm = round(get_distance(0, 5, h, w))
        if not x and not y:
            x, y = results.multi_hand_landmarks[0].landmark[4].x * w, results.multi_hand_landmarks[0].landmark[4].y * h
        dis_1 = get_distance(12, 8, h, w)
        cv2.putText(img, f"""MOVE: {round(dis_1)}/{round(mov_dis * dist_palm, 2)} - {"true" if dis_1 < mov_dis * dist_palm else "false"}""", (0, 15),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
        cv2.putText(img, f"""CLICK: {round(get_distance(5, 3, h, w))}/{round(click_dis * dist_palm, 2)} - {"true" if get_distance(5, 3, h, w) < click_dis * dist_palm else "false"}""", (0, 40),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
        cv2.putText(img,
                    f"""DRAG: {"true" if dis_1 < mov_dis * dist_palm and get_distance(5, 3, h, w) < click_dis * dist_palm else "false"}""",
                    (0, 65),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        if dis_1 < mov_dis * dist_palm and get_distance(5, 3, h, w) < click_dis * dist_palm:
            pyautogui.mouseDown()
            pyautogui.moveRel(-(results.multi_hand_landmarks[0].landmark[8].x * w - x) * sensitivity,
                              (results.multi_hand_landmarks[0].landmark[8].y * h - y) * sensitivity, duration=0.001)
        elif dis_1 < mov_dis * dist_palm:
            pyautogui.mouseUp()
            pyautogui.moveRel(-(results.multi_hand_landmarks[0].landmark[8].x * w - x) * sensitivity,
                              (results.multi_hand_landmarks[0].landmark[8].y * h - y) * sensitivity, duration=0.001)

        elif get_distance(5, 3, h, w) < click_dis * dist_palm and not click:
            pyautogui.mouseUp()
            pyautogui.click()
            click = True
        else:
            pyautogui.mouseUp()
            click = False
        x, y = results.multi_hand_landmarks[0].landmark[8].x * w, results.multi_hand_landmarks[0].landmark[8].y * h
        dist(8, 12, 0, 5, 3, 5)
    else:
        x, y = None, None
    cv2.imshow("Image", img)
    cv2.waitKey(1)
