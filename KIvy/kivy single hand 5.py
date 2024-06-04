import cv2
import mediapipe as mp
import pyautogui
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import math

class CustomDropDown(DropDown):
    pass

class VirtualMouseApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cap = None
        self.hand_detector = mp.solutions.hands.Hands()
        self.screen_width, self.screen_height = pyautogui.size()
        self.index_x = 0  
        self.index_y = 0
        self.video_sources = []
        self.dropdown = CustomDropDown()
        self.finger1 = ''  # Variable to store value from first entry field
        self.finger2 = ''  # Variable to store value from second entry field
        self.active_hand_index = None  # Index of the active hand

    def build(self):
        layout = BoxLayout(orientation='horizontal', spacing=10)
        
        # Left side layout for video capture
        left_layout = BoxLayout(orientation='vertical', spacing=10)
        self.img = Image()
        left_layout.add_widget(self.img)
        
        # Right side layout for text fields, video source selection, and distance label
        right_layout = BoxLayout(orientation='vertical', spacing=10)
        right_layout.size_hint_x = 0.6  # Set width ratio
        
        # Create entry fields and show image button
        entry_and_button_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.create_entry_field1_and_show_image_button(entry_and_button_layout)
        right_layout.add_widget(entry_and_button_layout)

        # Add a spacer to create space between the first entry field and the second one
        right_layout.add_widget(Label(size_hint_y=None, height=10))

        # Create the second entry field
        self.create_entry_field2(right_layout)
        
        # Create video source selection dropdown
        self.load_video_sources()
        self.create_dropdown(right_layout)
        
        # Add distance label
        self.distance_label = Label(text='', size_hint=(1, None), height=50, halign='center')
        right_layout.add_widget(self.distance_label)

        # Add left and right layouts to main layout
        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        
        Clock.schedule_interval(self.update, 1/30)
        return layout


    def load_video_sources(self):
        for i in range(10):  # Assuming max 10 video sources
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.video_sources.append(cap)
                cap.release()

    def create_dropdown(self, parent_layout):
        main_button = Button(text='Select Video Source', size_hint=(None, None), size=(250, 50))
        main_button.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.set_video_source)

        for i, source in enumerate(self.video_sources):
            btn = Button(text=f'Source {i}', size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))

        parent_layout.add_widget(main_button)

    def create_entry_field1_and_show_image_button(self, parent_layout):
    # First Entry Field
        self.entry1 = TextInput(hint_text='Enter Finger 1(Example: 8)', size_hint=(None, None), size=(250, 50), multiline=False)
        self.entry1.bind(text=self.on_entry1_text)  # Bind text change event
        parent_layout.add_widget(self.entry1)

        # Show Image Button
        self.image_popup_button = Button(size_hint=(None, None), size=(50, 50), background_normal=r'F:\PYTHON\Second Year Second Semister\virtual mouse\KIvy\logo.png', background_down=r"F:\PYTHON\Second Year Second Semister\virtual mouse\KIvy\logo.png")
        self.image_popup_button.bind(on_release=self.show_image_popup)
        parent_layout.add_widget(self.image_popup_button)

    def create_entry_field2(self, parent_layout):
        # Second Entry Field
        self.entry2 = TextInput(hint_text='Enter Finger 2(Example: 4)', size_hint=(None, None), size=(250, 50), multiline=False)
        self.entry2.bind(text=self.on_entry2_text)  # Bind text change event
        parent_layout.add_widget(self.entry2)

    def set_video_source(self, instance, text):
        index = int(text.split()[1])
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
            
            # Check if hands are detected
            if output.multi_hand_landmarks:
                # If the active hand is not yet set, or if the active hand is not detected, set it to the first detected hand
                if not self.active_hand_index or self.active_hand_index >= len(output.multi_hand_landmarks):
                    self.active_hand_index = 0
                
                # Get the landmarks of the active hand
                hand = output.multi_hand_landmarks[self.active_hand_index]
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    if id == int(self.finger1):
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        cv2.putText(frame, 'Finger 1', (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                        self.index_x = self.screen_width / frame_width * x
                        self.index_y = self.screen_height / frame_height * y

                    if id == int(self.finger2):
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                        cv2.putText(frame, 'Finger 2', (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                        thumb_x = self.screen_width / frame_width * x
                        thumb_y = self.screen_height / frame_height * y
                        distance = math.sqrt((thumb_x - self.index_x)**2 + (thumb_y - self.index_y)**2)
                        if distance < 30:
                            pyautogui.click()
                            pyautogui.sleep(0.5)
                        elif distance < 100:
                            pyautogui.moveTo(self.index_x, self.index_y)
                        self.distance_label.text = f'Distance: {distance:.2f}'

            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = texture

    def on_entry1_text(self, instance, value):
        self.finger1 = value

    def on_entry2_text(self, instance, value):
        self.finger2 = value

    def on_stop(self):
        if self.cap:
            self.cap.release()

    def show_image_popup(self, instance):
    # Create a scatter layout to display the image with zoom and pan capability
        scatter = ScatterLayout(do_translation=True, do_scale=True, do_rotation=False)

        # Load and add the image to the scatter layout
        img_source = r'F:\PYTHON\Second Year Second Semister\virtual mouse\KIvy\Info.jpeg'  # Replace 'your_image_path.jpg' with the path to your image
        img = Image(source=img_source)
        scatter.add_widget(img)

        # Create and open the popup with the scatter layout
        popup = Popup(title='Image Popup', content=scatter, size_hint=(None, None), size=(500, 500))
        popup.open()

    
if __name__ == '__main__':
    VirtualMouseApp().run()
