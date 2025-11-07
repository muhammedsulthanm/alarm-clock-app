import customtkinter as ctk
import time
import threading
import pygame
from tkinter import messagebox
import datetime

# Set global app theme
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

class AlarmClock(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Alarm Clock with Snooze")
        self.geometry("450x400")

        pygame.mixer.init()
        self.alarms = []  # list of strings "HH:MM"

        # UI Layout 
        frame_top = ctk.CTkFrame(self)
        frame_top.pack(pady=20, padx=20, fill="x")

        lbl = ctk.CTkLabel(frame_top, text="Set Alarm (HH:MM)", font=("Arial", 14))
        lbl.pack(anchor="w")

        self.time_entry = ctk.CTkEntry(frame_top, font=("Arial", 12))
        self.time_entry.pack(fill="x", pady=5)

        btn_frame = ctk.CTkFrame(frame_top)
        btn_frame.pack(fill="x", pady=5)
        self.set_button = ctk.CTkButton(btn_frame, text="Add Alarm", command=self.add_alarm)
        self.set_button.pack(side="left", expand=True, padx=(0,5))
        self.cancel_button = ctk.CTkButton(btn_frame, text="Remove Selected", command=self.remove_selected_alarm)
        self.cancel_button.pack(side="left", expand=True, padx=(5,0))

        self.current_time_label = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.current_time_label.pack(pady=10)

        
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        lbl_list = ctk.CTkLabel(list_frame, text="Alarms Set:", font=("Arial", 12))
        lbl_list.pack(anchor="w", pady=(0,5))
        self.alarms_listbox = ctk.CTkScrollableFrame(list_frame, width=300, height=150)
        self.alarms_listbox.pack(fill="both", expand=True)
        self.alarm_var = ctk.StringVar(value=None)

        self._update_alarms_list_ui()

        self.update_time()
        self.check_thread = threading.Thread(target=self.check_alarms, daemon=True)
        self.check_thread.start()

   
    def _update_alarms_list_ui(self):
        """Refresh the UI list of alarms safely on main thread."""
        for widget in self.alarms_listbox.winfo_children():
            widget.destroy()

        for alarm_time in self.alarms:
            rb = ctk.CTkRadioButton(self.alarms_listbox,
                                    text=alarm_time,
                                    variable=self.alarm_var,
                                    value=alarm_time,
                                    font=("Arial", 12))
            rb.pack(anchor="w", padx=5, pady=2)

    
    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.current_time_label.configure(text=f"Current Time: {current_time}")
        self.after(1000, self.update_time)

    
    def add_alarm(self):
        alarm_time = self.time_entry.get().strip()
        try:
            time.strptime(alarm_time, "%H:%M")
            if alarm_time in self.alarms:
                messagebox.showwarning("Warning", f"Alarm for {alarm_time} is already set.")
                return
            self.alarms.append(alarm_time)
            self._update_alarms_list_ui()
            messagebox.showinfo("Alarm Added", f"Alarm set for {alarm_time}")
        except ValueError:
            messagebox.showerror("Error", "Please enter time in HH:MM format (e.g., 14:30)")

    
    def remove_selected_alarm(self):
        selected = self.alarm_var.get()
        if not selected:
            messagebox.showinfo("No Selection", "Please select an alarm to remove.")
            return
        if selected in self.alarms:
            self.alarms.remove(selected)
            self.alarm_var.set(None)
            self._update_alarms_list_ui()
            messagebox.showinfo("Alarm Removed", f"Removed alarm for {selected}")
        else:
            messagebox.showerror("Error", "Selected alarm not found.")

    
    def check_alarms(self):
        """Background thread to monitor alarms."""
        while True:
            if self.alarms:
                current = time.strftime("%H:%M")
                for alarm_time in self.alarms.copy():
                    if current == alarm_time:
                        self.after(0, lambda t=alarm_time: self.play_alarm(t))
                        self.alarms.remove(alarm_time)
                        self.after(0, self._update_alarms_list_ui)
            time.sleep(1)

    
    def play_alarm(self, alarm_time):
        """Play alarm and show popup with Snooze and Stop buttons."""
        try:
            pygame.mixer.music.load("alarm_sound.mp3")
            pygame.mixer.music.play(-1)  # Loop until stopped
        except pygame.error:
            messagebox.showerror("Error", "Could not play alarm sound. Ensure 'alarm_sound.mp3' exists.")
            return

        # pop up for alarm ringing
        popup = ctk.CTkToplevel(self)
        popup.title("⏰ Alarm Ringing!")
        popup.geometry("320x200")
        popup.resizable(False, False)
        popup.grab_set()  

        frame = ctk.CTkFrame(popup, corner_radius=15)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        lbl = ctk.CTkLabel(frame, text=f"Alarm for {alarm_time}", font=("Arial", 16))
        lbl.pack(pady=15)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        stop_btn = ctk.CTkButton(btn_frame, text="🛑 Stop", width=100,
                                 fg_color="#E74C3C", hover_color="#C0392B",
                                 command=lambda: self.stop_alarm(popup))
        stop_btn.pack(side="left", padx=8)

        snooze_btn = ctk.CTkButton(btn_frame, text="😴 Snooze 5 min", width=120,
                                   fg_color="#3498DB", hover_color="#2980B9",
                                   command=lambda: self.snooze_alarm(popup, alarm_time))
        snooze_btn.pack(side="left", padx=8)

    
    def stop_alarm(self, popup):
        """Stop the alarm sound and close popup."""
        pygame.mixer.music.stop()
        popup.destroy()

    
    def snooze_alarm(self, popup, old_time):
        """Stop alarm and set new alarm 5 minutes later."""
        pygame.mixer.music.stop()
        popup.destroy()

        # snooze time
        try:
            now = datetime.datetime.now()
            h, m = map(int, old_time.split(":"))
            new_time_dt = (now.replace(hour=h, minute=m, second=0, microsecond=0)
                           + datetime.timedelta(minutes=5))
        except Exception:
            new_time_dt = datetime.datetime.now() + datetime.timedelta(minutes=5)

        new_time = new_time_dt.strftime("%H:%M")
        self.alarms.append(new_time)
        self.after(0, self._update_alarms_list_ui)
        messagebox.showinfo("Snoozed", f"Snoozed for 5 minutes (new alarm: {new_time})")


if __name__ == "__main__":
    app = AlarmClock()
    app.mainloop()
