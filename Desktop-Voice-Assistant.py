import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit
import pyjokes
import smtplib
import os
import webbrowser
import dateparser
import time


# Google Calendar
import datetime as dt
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# ----------- Voice Engine Setup ------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def talk(text):
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
    try:
        command = listener.recognize_google(audio).lower()
        if 'assistant' in command:
            command = command.replace('assistant', '').strip()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        talk("Sorry, I couldn't understand you.")
        return ""
    except sr.RequestError:
        talk("Sorry, I'm having trouble reaching Google's server")
        return ""

load_dotenv()  # Load variables from .env

sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("APP_PASSWORD")

# ----------- Send Email ------------
def send_email():
    talk("Who is the recipient?")
    recipient = listen_command().replace(" ", "")
    if "@" not in recipient:
        recipient += "@gmail.com"
    talk("What is the subject?")
    subject = listen_command()
    talk("What is the message?")
    message = listen_command()

    full_email = f"Subject: {subject}\n\n{message}"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)  # Replace with your credentials
        server.sendmail("your_email@gmail.com", recipient, full_email)
        server.quit()
        talk("Email sent successfully.")
    except Exception as e:
        print(e)
        talk("Failed to send the email.")

# ----------- Google Calendar Event ------------
def add_calendar_event():
    talk("What is the event title?")
    summary = listen_command()

    talk("When is the event? You can say things like 'tomorrow at 3 PM' or 'next Friday at 10 AM'")
    time_input = listen_command()
    event_time = dateparser.parse(time_input)

    if not event_time:
        event_time = dt.datetime.now() + dt.timedelta(minutes=10)
        talk("I couldn't understand the time. So I scheduled it 10 minutes from now.")

    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {'dateTime': event_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': (event_time + dt.timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Kolkata'},
    }

    service.events().insert(calendarId='primary', body=event).execute()
    talk("Event has been added to your calendar.")

# ----------- Take a Note ------------
def take_note():
    talk("What would you like me to write?")
    note = listen_command()
    with open("office_notes.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {note}\n")
    talk("Note saved successfully.")

# ----------- Open Applications ------------
def open_office_app(app_name):
    apps = {
        'outlook': 'start outlook',
        'teams': 'start teams',
        'excel': 'start excel',
        'notepad': 'notepad',
        'chrome': 'start chrome'
    }
    if app_name in apps:
        os.system(apps[app_name])
        talk(f"Opening {app_name}")
    else:
        talk(f"Sorry, I can't open {app_name} yet.")

# ----------- Open Office Websites ------------
def open_work_website(site_name):
    sites = {
        'servicenow': 'https://yourcompany.service-now.com',
        'mail': 'https://outlook.office.com',
    }
    if site_name in sites:
        webbrowser.open(sites[site_name])
        talk(f"Opening {site_name}")
    else:
        talk("I don't have that site saved yet.")

# ----------- Run Assistant (with return status) ------------
def run_assistant():
    attempts = 2
    while attempts > 0:
        command = listen_command()

        if not command or len(command.strip()) < 3:
            talk("I didn't catch that. Can you please repeat?")
            attempts -= 1
            continue

        if 'play' in command:
            song = command.replace('play', '')
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)
            return 'exit'  

        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The current time is {current_time}")
            return True

        elif 'who is' in command:
            person = command.replace('who is', '')
            try:
                info = wikipedia.summary(person, 1)
                talk(info)
            except:
                talk("Sorry, I couldn't find information on that.")
            return True

        elif 'joke' in command:
            talk(pyjokes.get_joke())
            return True

        elif 'send email' in command:
            send_email()
            return True

        elif 'add event' in command or 'calendar' in command:
            add_calendar_event()
            return True

        elif 'note' in command or 'take a note' in command:
            take_note()
            return True

        elif 'open' in command:
            for app in ['outlook', 'teams', 'excel', 'notepad', 'chrome']:
                if app in command:
                    open_office_app(app)
                    return True
            for site in [ 'servicenow', 'mail']:
                if site in command:
                    open_work_website(site)
                    return True
            talk("I didn't recognize that app or website.")
            return True

        elif 'exit' in command or 'stop' in command:
            talk("Goodbye!")
            exit()

        else:
            attempts -= 1
            if attempts > 0:
                talk("Sorry, I didn't understand. Could you repeat?")
            else:
                return False  # Exceeded attempts, let main decide what to do

    return False  # fallback if somehow loop exits without command

# ----------- Main with Exit Tracking ------------
if __name__ == "__main__":
    talk("Hello! I am your voice assistant. How can I help you today?")
    failure_attempts = 0
    while True:
        success = run_assistant()
        if not success:
            failure_attempts += 1
            if failure_attempts >= 2:
                talk("Too many failed attempts. Closing now.")
                time.sleep(3)
                break
        else:
            failure_attempts = 0  # reset on success
