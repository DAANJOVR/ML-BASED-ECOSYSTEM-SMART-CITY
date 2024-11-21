import tkinter as tk
import speech_recognition as sr
import datetime
import subprocess
import pyttsx3
import webbrowser
import os
import cv2
import random
import requests
from tkinter import PhotoImage
import serial  # For Arduino communication

# Initialize the serial communication with Arduino
arduino = serial.Serial('COM3', 9600)  # Replace with your Arduino port

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use the second voice (female)
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def capture_photo():
    """Function to capture a photo using the webcam."""
    speak("Taking a photo in 3 seconds. Please smile!")
    cv2.waitKey(3000)
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        photo_path = "captured_photo.jpg"
        cv2.imwrite(photo_path, frame)
        speak("Photo taken and saved.")
        output_text.set(f"Photo saved as {photo_path}.")
    else:
        speak("Sorry, I couldn't take a photo.")
    cap.release()
    cv2.destroyAllWindows()

def open_website(website_name):
    """Open a website based on the user's command."""
    websites = {
        'youtube': 'https://www.youtube.com',
        'facebook': 'https://www.facebook.com',
        'google': 'https://www.google.com',
        'x': 'https://www.x.com',
        'instagram': 'https://www.instagram.com',
        'github': 'https://www.github.com',
        'wikipedia': 'https://en.wikipedia.org',
        'reddit': 'https://www.reddit.com',
        'music': 'https://music.youtube.com/watch?v=CKpbdCciELk&list=OLAK5uy_lk4hlzR_Y1Mk5x6hjZJbwNgugWtMlrj3I',
    }
    website_url = websites.get(website_name, f"https://www.google.com/search?q={website_name}")
    webbrowser.open(website_url)
    speak(f"Opening {website_name}.")
    output_text.set(f"Opening {website_name}.")

def process_command(text):
    """Process the recognized speech command."""
    text = text.lower()

    # Handle relay control (locking/unlocking door) and buzzer control
    if 'emergency' in text:
        arduino.write(b'EMERGENCY\n')  # Trigger the emergency response on Arduino (unlock door and start buzzer)
        speak("Emergency detected! Door unlocked and siren activated.")
        output_text.set("Emergency detected! Door unlocked and siren activated.")

    elif 'stop siren' in text:
        arduino.write(b'STOP\n')  # Trigger the stop response on Arduino (stop buzzer and lock door)
        speak("Siren stopped and door locked.")
        output_text.set("Siren stopped and door locked.")

    elif 'chrome' in text:
        speak('Opening Chrome..')
        subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
        output_text.set("Chrome opened.")

    elif 'time' in text:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")
        output_text.set(f"The current time is {current_time}.")

    elif 'search for' in text:
        search_query = text.replace("search for", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        speak(f"Here are the search results for {search_query}.")
        output_text.set(f"Searching for: {search_query}")

    elif 'send a message' in text:
        message = text.replace("send a message", "").strip()
        speak("Message sent!")  # Placeholder response
        output_text.set(f"Message sent: {message}")

    elif 'open notepad' in text:
        speak('Opening Notepad..')
        subprocess.Popen(['notepad.exe'])
        output_text.set("Notepad opened.")

    elif 'open file explorer' in text:
        speak('Opening File Explorer..')
        subprocess.Popen('explorer')
        output_text.set("File Explorer opened.")

    elif 'open camera' in text:
        speak('Opening Camera..')
        subprocess.Popen('start microsoft.windows.camera:', shell=True)
        output_text.set("Camera opened.")

    elif 'take a photo' in text:
        capture_photo()

    elif 'open' in text:
        website_name = text.replace("open", "").strip()
        if website_name:
            open_website(website_name)

    else:
        speak("Sorry, I didn't understand that.")
        output_text.set("Sorry, I didn't understand that.")

def record_speech():
    """Function to record speech and process the command."""
    with sr.Microphone() as source:
        output_text.set("Clearing background noises... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        output_text.set("Listening... Please speak now.")
        
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()
            output_text.set(f"Recognized Text: {text}")
            process_command(text)
        except sr.UnknownValueError:
            output_text.set("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            output_text.set(f"Could not request results; {e}")
        except Exception as e:
            output_text.set(f"An error occurred: {e}")

# Function to trigger emergency mode via button
def trigger_emergency():
    arduino.write(b'EMERGENCY\n')  # Send the emergency signal to Arduino
    speak("Emergency detected! Door unlocked and siren activated.")
    output_text.set("Emergency detected! Door unlocked and siren activated.")

# Function to stop the siren via button
def stop_siren():
    arduino.write(b'STOP\n')  # Send the stop signal to Arduino
    speak("Siren stopped and door locked.")
    output_text.set("Siren stopped and door locked.")

# Set up the GUI
root = tk.Tk()
root.title("ATLAS-Voice Assistant")
root.geometry("400x350")

# Load the background image
bg_image = PhotoImage(file="assistant.gif")  # Make sure you have a file named assistant.gif
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Label to display the instructions
instruction_label = tk.Label(root, text="Press 'Record' and start speaking:", bg="white", font=("Arial", 12))
instruction_label.pack(pady=10)

# Button to start recording
record_button = tk.Button(root, text="Record", command=record_speech, font=("Arial", 12), bg="lightblue")
record_button.pack(pady=10)

# Emergency button
emergency_button = tk.Button(root, text="Emergency", command=trigger_emergency, font=("Arial", 12), bg="red")
emergency_button.pack(pady=10)

# Stop siren button
stop_siren_button = tk.Button(root, text="Stop Siren", command=stop_siren, font=("Arial", 12), bg="green")
stop_siren_button.pack(pady=10)

# Text box to display the recognized text and responses
output_text = tk.StringVar()
output_text.set("Press 'Record' to start.")
output_label = tk.Label(root, textvariable=output_text, wraplength=300, justify="center", bg="white", font=("Arial", 12))
output_label.pack(pady=10)

# Run the GUI event loop
root.mainloop()
