import PySimpleGUIQt as sg
import os
import threading
from time import sleep
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import math

delayed_sleep_active = False
cancel_delayed_sleep = False
remaining_time = 0

BASE64_ICON = """
iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAABHNCSVQICAgIfAhkiAAAAAFzUkdCAK7OHOkAAAAEZ0FNQQAAsY8L/GEFAAAACXBIWXMAABJ0AAASdAHeZh94AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAIgxJREFUeF7t3XmUnVWZ6OGXJKQXghBIUlUJtgLaKJcpDEoAISEhQ5sQCBkgAwSFllmvAo7IoNKN4m1RhiAgUwbCEANJGDJBogJqMzZIJNooGDNUhhtGA0ng1in2H/ePHtScqjr77OdZq1btd1eBa+E69f3O933nnG0i4t2WLwCgIJ3SdwCgIAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAokAACgQAIAAAok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yJkAKNCWLVviT8uXR3Nzc6xpXtP6vfL11saN0aNnz2hoaIieLV+V77t+YNfWywoA1BcBAAAFchMgABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABRIAABAgQQAABQn4v8BkwYEb20phMkAAAAASUVORK5CYII=
"""


def create_timer_image(minutes):
    width, height = 128, 128
    background = (50, 50, 50, 255)

    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw.ellipse((0, 0, width - 1, height - 1), fill=background)

    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    text = f"{minutes}m"
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top

    draw.text(
        ((width - text_width) / 2, (height - text_height) / 2),
        text,
        fill="white",
        font=font
    )

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')


def countdown(seconds, tray):
    global delayed_sleep_active, cancel_delayed_sleep, remaining_time

    delayed_sleep_active = True
    cancel_delayed_sleep = False
    remaining_time = seconds

    try:
        while remaining_time > 0 and not cancel_delayed_sleep:
            minutes = math.ceil(remaining_time / 60)
            timer_icon_path = create_timer_image(minutes)

            tooltip = f"Shutting down in {minutes} min {remaining_time % 60} sec"
            tray.update(filename=timer_icon_path, tooltip=tooltip)

            try:
                os.unlink(timer_icon_path)
            except:
                pass

            sleep(1)
            remaining_time -= 1

        tray.update(filename=r'image.png', tooltip="Sleep Control")
        if not cancel_delayed_sleep:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    finally:
        delayed_sleep_active = False


def cancel_sleep():
    global cancel_delayed_sleep
    cancel_delayed_sleep = True


def main():
    global delayed_sleep_active

    menu_def = ['BLANK', ['&Sleep', '&Delayed sleep', '---', 'Cancel delayed sleep', 'E&xit']]
    tooltip = 'Sleep Control'
    tray = sg.SystemTray(menu=menu_def, filename=BASE64_ICON, tooltip=tooltip)

    try:
        while True:
            try:
                menu_item = tray.read()
                if menu_item == 'Exit':

                    if delayed_sleep_active:
                        cancel_sleep()
                    break
                elif menu_item == 'Sleep':
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                elif menu_item == 'Delayed sleep':
                    if delayed_sleep_active:
                        sg.popup('Timer is already running')
                        continue
                    text = sg.popup_get_text('Time before sleep in minutes', title="Delayed sleep")
                    try:
                        minutes = int(text)
                        seconds = minutes * 60

                        threading.Thread(target=countdown, args=(seconds, tray), daemon=True).start()
                    except:
                        sg.popup_error('Please enter a valid number')
                elif menu_item == 'Cancel delayed sleep':
                    if delayed_sleep_active:
                        cancel_sleep()
                        sg.popup('Delayed sleep cancelled')
                    else:
                        sg.popup('No active delayed sleep to cancel')
            except Exception as e:
                print(f"Error: {e}")
                continue
    finally:
        try:
            os.unlink('image.png')
        except:
            pass


if __name__ == "__main__":
    main()
