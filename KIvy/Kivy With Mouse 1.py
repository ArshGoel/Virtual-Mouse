import cv2
import mediapipe as mp
import pyautogui
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import math

class VirtualMouseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cap = cv2.VideoCapture(0)
        self.hand_detector = mp.solutions.hands.Hands()
        self.screen_width, self.screen_height = pyautogui.size()
        self.index_x = 0  # Initialize index_x attribute
        self.index_y = 0

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.img = Image()
        self.layout.add_widget(self.img)
        Clock.schedule_interval(self.update, 1/30)  # Update at 30fps
        return self.layout

    def update(self, dt):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = self.hand_detector.process(rgb_frame)
            hands = output.multi_hand_landmarks
            if hands:
                for hand in hands:
                    landmarks = hand.landmark
                    for id, landmark in enumerate(landmarks):
                        x = int(landmark.x * frame_width)
                        y = int(landmark.y * frame_height)
                        if id == 8:
                            cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                            self.index_x = self.screen_width / frame_width * x
                            self.index_y = self.screen_height / frame_height * y

                        if id == 4:
                            cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                            thumb_x = self.screen_width / frame_width * x
                            thumb_y = self.screen_height / frame_height * y
                            distance = math.sqrt((thumb_x - self.index_x)**2 + (thumb_y - self.index_y)**2)
                            if distance < 30:
                                pyautogui.click()
                                pyautogui.sleep(0.5)
                            elif distance < 100:
                                pyautogui.moveTo(self.index_x, self.index_y)

            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

    def on_stop(self):
        self.cap.release()

if __name__ == '__main__':
    VirtualMouseApp().run()
