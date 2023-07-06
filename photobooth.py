from picamera import PiCamera
from gpiozero import Button
from PIL import Image, ImageSequence, ImageTk
from tkinter import Tk, Label
import os
import time
import glob
from io import BytesIO

# GPIO pins for the buttons
PHOTO_BUTTON_PIN = 17
SWITCH_BUTTON_PIN = 27

# directory to store gifs
GIF_DIR = "/home/pi/photobooth_gifs/"

# Initialize the camera, photo button, and switch button
camera = PiCamera()
photo_button = Button(PHOTO_BUTTON_PIN)
switch_button = Button(SWITCH_BUTTON_PIN)

def init_camera():
    camera.resolution = get_screen_resolution()

def get_screen_resolution():
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return (width, height)

def wait_for_button_press():
    photo_button.wait_for_press()

def take_photos():
    photo_list = []
    for i in range(5):
        stream = BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        photo = Image.open(stream)
        photo_list.append(photo)
    return photo_list

def preview_photos(photo_list, label, root):
    for photo in photo_list:
        photo_image = ImageTk.PhotoImage(photo)
        label.config(image=photo_image)
        label.image = photo_image
        root.update_idletasks()
        root.update()
        time.sleep(0.2)  # Display each photo for 0.2 seconds

def create_gif(photo_list):
    gif_path = GIF_DIR + time.strftime("%Y%m%d-%H%M%S") + ".gif"
    photo_list[0].save(gif_path, save_all=True, append_images=photo_list[1:], optimize=False, duration=500, loop=0)
    return gif_path

def display_gif(gif_path, label, root):
    gif = Image.open(gif_path)
    for frame in ImageSequence.Iterator(gif):
        frame_image = ImageTk.PhotoImage(frame)
        label.config(image=frame_image)
        label.image = frame_image
        root.update_idletasks()
        root.update()
        time.sleep(0.2)  # Display each frame for 0.2 seconds

def save_gif(gif_path):
    pass  # The GIF has already been saved in create_gif()

def cycle_through_gifs(label, root):
    gif_files = glob.glob(GIF_DIR + "*.gif")
    for gif_file in gif_files:
        display_gif(gif_file, label, root)

def main():
    init_camera()

    root = Tk()
    label = Label(root)
    label.pack()

    while True:
        if switch_button.is_pressed:
            cycle_through_gifs(label, root)
        else:
            wait_for_button_press()
            photo_list = take_photos()
            preview_photos(photo_list, label, root)
            gif_path = create_gif(photo_list)
            display_gif(gif_path, label, root)

if __name__ == "__main__":
    main()
