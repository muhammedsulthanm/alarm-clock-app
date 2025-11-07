⏰ Alarm Clock App using Python

A modern, lightweight, and user-friendly Python-based Alarm Clock built using CustomTkinter, Datetime, Threading, and Pygame.
This application features a sleek GUI, accurate alarm triggering, and a fully working Snooze feature.


---

✅ Features

🔔 Set custom alarm time

🎨 Modern & responsive GUI using CustomTkinter

⏳ Accurate real-time clock tracking

😴 Snooze button to delay the alarm

🔊 Alarm sound playback using Pygame

💬 Popup notifications for alarm & snooze

✅ Works completely offline

🚀 Smooth user experience with multi-threading



---

🛠 Modules & Libraries Used

Module	Purpose

customtkinter	Builds the modern GUI
datetime	Retrieves and formats current time
time	Handles basic time functions
threading	Runs alarm logic without freezing GUI
pygame	Plays the alarm sound
tkinter.messagebox	Shows popup alerts



---

📌 How It Works

1. User enters the alarm time via GUI.


2. App compares input time with the system time continuously.


3. When the time matches:

✅ Alarm sound plays

✅ Popup message appears



4. User can:

Stop the alarm, or

Snooze → Alarm repeats after a fixed delay





---

🚀 Snooze Feature Logic

Adds a fixed delay (e.g., +5 minutes)

Updates the alarm time internally

Restarts the alarm thread without freezing the GUI



---

📂 Project Structure

📁 AlarmClock-App
│── alarm.py              # Main application code
│── alarm_sound.mp3       # Alarm sound file
│── README.md             # Documentation


---

▶ Installation & Usage

⿡ Install Dependencies

pip install customtkinter pygame

⿢ Run the App

python alarm.py


---

🖼 Screenshots

(Add after uploading images)

Main Interface



Alarm Triggered



Snooze Option




---

✨ Future Enhancements

Multiple alarms

Custom snooze duration

GUI theme switcher (light/dark mode)

Better alarm sound selection

Cloud-based reminder sync



---

👨‍💻 Team Members

Srishrayas R (25BAI0226)

Ayush CK (25BAI0206)

Bhuvan (25BAI0228)

Muhammed Sulthan M (25BAI0234)



---
