import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
import cv2
import threading

class VideoChatApp(App):
    def build(self):
        # Initialize UI
        self.main_layout = BoxLayout(orientation='vertical')
        self.camera_layout = BoxLayout(orientation='vertical')
        self.popup_layout = BoxLayout(orientation='vertical')
        self.popup = Popup(title='New Video Source Detected', content=self.popup_layout, size_hint=(None, None), size=(400, 400))
        self.popup.dismiss()

        # Initialize camera
        self.camera = None
        self.selected_source = None

        # Start thread for checking new devices
        self.new_device_thread = threading.Thread(target=self.check_new_devices)
        self.new_device_thread.daemon = True
        self.new_device_thread.start()

        # Add camera layout to main layout
        self.main_layout.add_widget(self.camera_layout)

        return self.main_layout

    def check_new_devices(self):
        while True:
            new_sources = self.get_camera_sources()
            if self.selected_source not in new_sources:
                self.show_popup(new_sources)
            # Sleep for some time before checking again (e.g., every 5 seconds)
            time.sleep(5)

    def get_camera_sources(self):
        # Get list of available camera sources
        sources = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                sources.append(i)
                cap.release()
        return sources

    def show_popup(self, new_sources):
        # Create popup to show new sources
        self.popup_layout.clear_widgets()
        for source in new_sources:
            btn = Button(text=f"New Source Detected: Camera {source}", size_hint=(1, None), height=40)
            btn.bind(on_release=lambda btn: self.select_camera(source))
            self.popup_layout.add_widget(btn)
        self.popup.open()

    def select_camera(self, source):
        # Stop current camera
        if self.camera:
            self.camera_layout.remove_widget(self.camera)
        # Create new camera with selected source
        self.camera = Camera(resolution=(640, 480), index=source)
        self.camera_layout.add_widget(self.camera)
        self.selected_source = source
        self.popup.dismiss()

if __name__ == '__main__':
    VideoChatApp().run()
