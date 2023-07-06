import sys  # needed to get exception info

# ...

def wait_for_button_press():
    try:
        photo_button.wait_for_press()
    except Exception as e:
        print(f"Error in wait_for_button_press: {e}")
        sys.exit(1)  # exit program

def take_photos():
    photo_list = []
    try:
        for i in range(5):
            stream = BytesIO()
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            photo = Image.open(stream)
            photo_list.append(photo)
    except Exception as e:
        print(f"Error in take_photos: {e}")
        sys.exit(1)  # exit program
    return photo_list

def create_gif(photo_list):
    gif_path = GIF_DIR + time.strftime("%Y%m%d-%H%M%S") + ".gif"
    try:
        photo_list[0].save(gif_path, save_all=True, append_images=photo_list[1:], optimize=False, duration=500, loop=0)
    except Exception as e:
        print(f"Error creating GIF: {e}")
        return None
    return gif_path

def display_gif(gif_path, label, root):
    try:
        gif = Image.open(gif_path)
        for frame in ImageSequence.Iterator(gif):
            frame_image = ImageTk.PhotoImage(frame)
            label.config(image=frame_image)
            label.image = frame_image
            root.update_idletasks()
            root.update()
            time.sleep(0.2)  # Display each frame for 0.2 seconds
    except Exception as e:
        print(f"Error displaying GIF: {e}")
