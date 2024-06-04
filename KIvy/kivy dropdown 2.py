import cv2
import mediapipe as mp
import pyautogui
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import math

class VirtualMouseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cap = None
        self.hand_detector = mp.solutions.hands.Hands()
        self.screen_width, self.screen_height = pyautogui.size()
        self.index_x = 0  
        self.index_y = 0
        self.video_sources = []
        self.dropdown = DropDown()

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.img = Image()
        self.layout.add_widget(self.img)
        self.load_video_sources()
        self.create_dropdown()
        Clock.schedule_interval(self.update, 1/30)
        return self.layout

    def load_video_sources(self):
        for i in range(10):  # Assuming max 10 video sources
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.video_sources.append(cap)
                cap.release()

    def create_dropdown(self):
        main_button = Button(text='Select Source', size_hint=(None, None))
        main_button.bind(on_release=self.dropdown.open)
        self.layout.add_widget(main_button)

        for i, source in enumerate(self.video_sources):
            btn = Button(text=f'Source {i}', size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.set_video_source(btn.text.split()[1]))
            self.dropdown.add_widget(btn)

    def set_video_source(self, index):
        index = int(index)
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(index)

    def update(self, dt):
        if not self.cap:
            return

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
        if self.cap:
            self.cap.release()

if __name__ == '__main__':
    VirtualMouseApp().run()
