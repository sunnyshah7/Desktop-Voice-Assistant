# 🎙️ AI Voice Assistant for Office Tasks

A Python-powered voice assistant that helps you **send emails**, **manage your calendar**, **launch applications**, **tell jokes**, **play YouTube songs**, and much more — all using your voice.

> Developed with `speech_recognition`, `pyttsx3`, `Google APIs`, and natural language processing tools.

---

## ✨ Features

| Feature            | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| 🎧 Voice Commands   | Activate tasks by simply speaking to your assistant.                        |
| 📧 Send Emails      | Dictate recipient, subject, and message to send an email securely via Gmail.|
| 📅 Google Calendar  | Add events to your Google Calendar via voice, using natural language time. |
| 📌 Notes            | Take office notes and store them locally with timestamps.                   |
| 😂 Tell Jokes       | Get a random joke on command.                                               |
| 🎵 Play YouTube     | Search and play songs directly on YouTube.                                 |
| 🖥️ Launch Apps      | Open Outlook, Teams, Excel, Chrome, Notepad, etc.                          |
| 🌐 Open Websites    | Open company tools like ServiceNow, Outlook Web, etc.                      |
| 🛡️ Secure Auth      | Sensitive credentials stored using environment variables.                  |

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/voice-assistant.git
cd voice-assistant

2. Create and Activate Virtual Environment
    python -m venv .venv
    .venv\Scripts\activate    # On Windows

3. Install Dependencies
    pip install -r requirements.txt

4. Create .env File
    Create a .env file in the root directory and add:
    SENDER_EMAIL=your_email@gmail.com
    APP_PASSWORD=your_gmail_app_password

5. Enable Google Calendar API
    Go to Google Cloud Console
    Create a new project
    Enable Google Calendar API
    Configure OAuth Consent Screen (External, testing OK)
    Create OAuth Client ID (choose Desktop App)
    Download the credentials.json file and place it in the root directory.

🔊 How to Use
    Run the script:
    python assistant.py

Then speak any of the following:

Command Example	What Happens:
    play Let it go	Plays Let it go on YouTube
    send email	Prompts for recipient, subject, and body
    add  event	Adds an event like "tomorrow at 5 PM"
    take a note	Appends your note in office_notes.txt
    open outlook / open teams	Launches respective apps
    open mail / open servicenow	Opens webmail or your ticketing portal
    joke Tells a random joke
    exit Gracefully shuts down

🔐 Security Notes
    Sensitive data is never hardcoded — stored in .env.
    .env and token.json are listed in .gitignore and won’t be pushed to GitHub.
    Emails are sent securely through Gmail’s App Password system.

🧠 Technologies Used
    Python 3.x
    speech_recognition
    pyttsx3 (Text-to-speech)
    pywhatkit (YouTube + Web search)
    google-auth, google-api-python-client (Calendar)
    python-dotenv
    dateparser (Natural language time parsing)


📂 Folder Structure
    voice-assistant/
    │
    ├── assistant.py            # Main program
    ├── credentials.json        # Google API credentials
    ├── token.json              # Stores user token after first login
    ├── office_notes.txt        # Your saved notes
    ├── .env                    # Gmail credentials (ignored from Git)
    ├── .gitignore              # Files to ignore
    ├── README.md               # This file
    └── requirements.txt        # Dependencies

🙋‍♂️ Author
    Developed with ❤️ by Sunny Kumar Shah
    Feel free to connect or contribute!

⭐ Contribute
    Fork the repo
    Create a new branch (git checkout -b feature-name)
    Commit your changes (git commit -am 'Add feature')
    Push and create a Pull Request.
