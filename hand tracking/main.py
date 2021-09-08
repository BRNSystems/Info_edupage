import math
import os
import cv2
import mediapipe as mp
import pyautogui

os.chdir("..")


class Hands_AI:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        pyautogui.PAUSE = 0.01
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1, min_tracking_confidence=0.95, min_detection_confidence=0.90)
        self.mpDraw = mp.solutions.drawing_utils
        self.mov_dis = 0.2479
        self.click_dis = 0.2823
        self.sensitivity = 3.5
        self.x, self.y = None, None
        self.click = False

    def get_distance(self, first, second, height, width):
        dist_x = (self.results.multi_hand_landmarks[0].landmark[first].x -
                  self.results.multi_hand_landmarks[0].landmark[
                      second].x) * width
        dist_y = (self.results.multi_hand_landmarks[0].landmark[first].y -
                  self.results.multi_hand_landmarks[0].landmark[
                      second].y) * height
        return math.sqrt(abs(dist_x ** 2 + dist_y ** 2))

    def run(self, q):
        while True:
            success, img = self.cap.read()
            self.h, self.w, self.c = img.shape
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(imgRGB)
            if self.results.multi_hand_landmarks:
                dist_palm = round(self.get_distance(0, 5, self.h, self.w))
                if not self.x and not self.y:
                    self.x, self.y = self.results.multi_hand_landmarks[0].landmark[4].x * self.w, \
                                     self.results.multi_hand_landmarks[0].landmark[4].y * self.h
                dis_1 = self.get_distance(12, 8, self.h, self.w)
                cv2.putText(img,
                            f"""MOVE: {round(dis_1)}/{round(self.mov_dis * dist_palm, 2)} - {"true" if dis_1 < self.mov_dis * dist_palm else "false"}""",
                            (0, 15),
                            cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
                cv2.putText(img,
                            f"""CLICK: {round(self.get_distance(5, 3, self.h, self.w))}/{round(self.click_dis * dist_palm, 2)} - {"true" if self.get_distance(5, 3, self.h, self.w) < self.click_dis * dist_palm else "false"}""",
                            (0, 40),
                            cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
                cv2.putText(img,
                            f"""DRAG: {"true" if dis_1 < self.mov_dis * dist_palm and self.get_distance(5, 3, self.h, self.w) < self.click_dis * dist_palm else "false"}""",
                            (0, 65),
                            cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), thickness=2)
                for handLms in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                if dis_1 < self.mov_dis * dist_palm and self.get_distance(5, 3, self.h,
                                                                          self.w) < self.click_dis * dist_palm:
                    pyautogui.mouseDown()
                    pyautogui.moveRel(
                        -(self.results.multi_hand_landmarks[0].landmark[8].x * self.w - self.x) * self.sensitivity,
                        (self.results.multi_hand_landmarks[0].landmark[8].y * self.h - self.y) * self.sensitivity,
                        duration=0.001)
                elif dis_1 < self.mov_dis * dist_palm:
                    pyautogui.mouseUp()
                    pyautogui.moveRel(
                        -(self.results.multi_hand_landmarks[0].landmark[8].x * self.w - self.x) * self.sensitivity,
                        (self.results.multi_hand_landmarks[0].landmark[8].y * self.h - self.y) * self.sensitivity,
                        duration=0.001)

                elif self.get_distance(5, 3, self.h, self.w) < self.click_dis * dist_palm and not self.click:
                    pyautogui.mouseUp()
                    pyautogui.click()
                    self.click = True
                else:
                    pyautogui.mouseUp()
                    self.click = False
                self.x, self.y = self.results.multi_hand_landmarks[0].landmark[8].x * self.w, \
                                 self.results.multi_hand_landmarks[0].landmark[8].y * self.h
            else:
                self.x, self.y = None, None
            cv2.imshow("Image", img)
            cv2.imwrite("UI/video_capture_.png", img)
            try:
                os.remove("UI/video_capture.png")
                os.rename("UI/video_capture_.png", "UI/video_capture.png")
            except:
                pass
            cv2.waitKey(1)


if __name__ == '__main__':
    ai = Hands_AI()
    ai.run("X")