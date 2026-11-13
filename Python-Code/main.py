import os
import tkinter as tk
from controller import DashboardController

# Dashboard initialisieren, Application-Klasse definieren
class DashboardRoot:
    def __init__(self):
        print("Aktuelles Verzeichnis:", os.getcwd())
        print("Dateien im Verzeichnis:", os.listdir())

        self.dashboard = tk.Tk()
        self.dashboard.title("Dashboard Studium - Cyber Security")
        self.dashboard.state("zoomed")

        self.controller = DashboardController(self.dashboard)
        self.controller.views_anfordern()

        self.dashboard.mainloop()

if __name__ == "__main__":
    DashboardRoot()