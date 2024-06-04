import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math

# Initialize variables
cap = None
hand_detector = mp.solutions.hands.Hands()
screen_width, screen_height = pyautogui.size()
index_x = 0
index_y = 0
video_sources = []
finger1 = ''  # Variable to store value from first entry field
finger2 = ''  # Variable to store value from second entry field
move_dist = ''  # Variable to store value from first entry field
click_dist = ''
active_hand_index = None  # Index of the active hand

# Load video sources
def load_video_sources():
    for i in range(10):  # Assuming max 10 video sources
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            video_sources.append(cap)
            cap.release()

# Create dropdown menu
def create_dropdown(parent_frame):
    main_button = ttk.Button(parent_frame, text='Select Video Source')
    main_button.pack()

    dropdown = tk.Menu(parent_frame, tearoff=0)
    for i, source in enumerate(video_sources):
        dropdown.add_command(label=f'Source {i}', command=lambda i=i: set_video_source(i))

    main_button['menu'] = dropdown

# Set video source
def set_video_source(index):
    global cap
    if cap:
        cap.release()
    cap = cv2.VideoCapture(index)

# Create entry fields
def create_entry_fields(parent_frame):
    # First Entry Field
    entry1_label = tk.Label(parent_frame, text='Enter Finger 1 (Example: 8)')
    entry1_label.pack()
    entry1 = tk.Entry(parent_frame)
    entry1.pack()
    entry1.bind('<KeyRelease>', lambda event: on_entry1_text(entry1.get()))

    # Second Entry Field
    entry2_label = tk.Label(parent_frame, text='Enter Finger 2 (Example: 4)')
    entry2_label.pack()
    entry2 = tk.Entry(parent_frame)
    entry2.pack()
    entry2.bind('<KeyRelease>', lambda event: on_entry2_text(entry2.get()))

    # Movement Entry Field
    entry_move_label = tk.Label(parent_frame, text='Enter Movement Distance (Example: 150)')
    entry_move_label.pack()
    entry_move = tk.Entry(parent_frame)
    entry_move.pack()
    entry_move.bind('<KeyRelease>', lambda event: on_movement_dist_text(entry_move.get()))

    # Click Entry Field
    entry_click_label = tk.Label(parent_frame, text='Enter Click Distance (Example: 50)')
    entry_click_label.pack()
    entry_click = tk.Entry(parent_frame)
    entry_click.pack()
    entry_click.bind('<KeyRelease>', lambda event: on_click_dist_text(entry_click.get()))

# Update function
def update():
    if not cap:
        return

    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)

        # Check if hands are detected
        if output.multi_hand_landmarks:
            # If the active hand is not yet set, or if the active hand is not detected, set it to the first detected hand
            if not active_hand_index or active_hand_index >= len(output.multi_hand_landmarks):
                active_hand_index = 0

            # Get the landmarks of the active hand
            hand = output.multi_hand_landmarks[active_hand_index]
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == int(finger1):
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    cv2.putText(frame, 'Finger 1', (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == int(finger2):
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    cv2.putText(frame, 'Finger 2', (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                    thumb_x = screen_width / frame_width * x
                    thumb_y= screen_height / frame_height * y
                    distance = math.sqrt((thumb_x - index_x)**2 + (thumb_y - index_y)**2)
                    if distance < int(click_dist):
                        pyautogui.click()
                        pyautogui.sleep(0.5)
                    elif distance < int(move_dist):
                        pyautogui.moveTo(index_x, index_y)

        # Display the frame
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        label.after(10, update)

# Key release event handlers
def on_entry1_text(value):
    global finger1
    finger1 = value

def on_entry2_text(value):
    global finger2
    finger2 = value

def on_movement_dist_text(value):
    global move_dist
    move_dist = value

def on_click_dist_text(value):
    global click_dist
    click_dist = value

# Main function
def main():
    global root, label

    # Initialize Tkinter
    root = tk.Tk()
    root.title('Virtual Mouse')

    # Load video sources
    load_video_sources()

    # Create dropdown menu
    create_dropdown(root)

    # Create entry fields
    create_entry_fields(root)

    # Create label to display the video
    label = tk.Label(root)
    label.pack()

    # Start the update loop
    update()

    # Run the Tkinter mainloop
    root.mainloop()

if __name__ == '__main__':
    main()