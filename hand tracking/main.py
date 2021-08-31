import cv2
import mediapipe as mp
import time
import math
import pyautogui

cap = cv2.VideoCapture(0)
pyautogui.PAUSE = 0.01
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_tracking_confidence=0.80, min_detection_confidence=0.90)
mpDraw = mp.solutions.drawing_utils
testing = 23
click_dis = 35
sensitivity = 3.5


def get_distance(first, second, height, width):
    dist_x = (results.multi_hand_landmarks[0].landmark[first].x - results.multi_hand_landmarks[0].landmark[
        second].x) * width
    dist_y = (results.multi_hand_landmarks[0].landmark[first].y - results.multi_hand_landmarks[0].landmark[
        second].y) * height
    return math.sqrt(abs(dist_x ** 2 + dist_y ** 2))


x, y = None, None

while True:
    success, img = cap.read()
    h, w, c = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        dist_palm = round(get_distance(0, 9, h, w) / 100, 3)
        if not x and not y:
            x, y = results.multi_hand_landmarks[0].landmark[4].x * w, results.multi_hand_landmarks[0].landmark[4].y * h
        dis_1 = get_distance(4, 8, h, w)
        cv2.putText(img, f"""dist 4-8: {round(dis_1)}/{round(testing * dist_palm, 2)}""", (0, 15),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
        cv2.putText(img, f"""MOVE: {"True" if dis_1 < testing else "False"}""", (0, 40),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
        cv2.putText(img, f"""dist 4-12: {round(get_distance(12, 4, h, w))}/{round(click_dis * dist_palm, 2)}""",
                    (0, 65),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
        cv2.putText(img, f"""CLICK: {"True" if get_distance(12, 4, h, w) < click_dis * dist_palm else "False"}""",
                    (0, 90),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
        cv2.putText(img, f"""dsit 0-9: {dist_palm}""", (0, 115),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms)
        if dis_1 < testing * dist_palm and get_distance(12, 4, h, w) < click_dis * dist_palm:
            pyautogui.dragRel(-(results.multi_hand_landmarks[0].landmark[3].x * w - x) * sensitivity,
                              (results.multi_hand_landmarks[0].landmark[3].y * h - y) * sensitivity, duration=0.001)
        elif dis_1 < testing * dist_palm:
            pyautogui.moveRel(-(results.multi_hand_landmarks[0].landmark[3].x * w - x) * sensitivity,
                              (results.multi_hand_landmarks[0].landmark[3].y * h - y) * sensitivity, duration=0.001)

        elif get_distance(12, 4, h, w) < click_dis * dist_palm and not click:
            pyautogui.click()
            click = True
            # mouse.click("left")
            print("clicked")
        else:
            click = False
        x, y = results.multi_hand_landmarks[0].landmark[3].x * w, results.multi_hand_landmarks[0].landmark[3].y * h
    else:
        x, y = None, None
    cv2.imshow("Image", img)
    cv2.waitKey(1)
