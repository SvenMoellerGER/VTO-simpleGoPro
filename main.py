import tkinter as tk
from datetime import datetime
from goprocam import GoProCamera
import tkinter.messagebox as messagebox


class GoProController:
    def __init__(self):
        self.camera = GoProCamera.GoPro()

    def date_and_time(self):
        now = datetime.now()
        return now.strftime("%Y%m%d-%H%M%S")

    def start_recording(self):
        dt = self.date_and_time()
        try:
            print(f"Aufnahme gestartet um {dt}")
            self.camera.video_settings("R1080p", "120")
            self.camera.shoot_video(5)  # Aufnahme gestarten, 5 Sekunden
            print(f"Aufnahme beendet um {self.date_and_time()}")
        except Exception as e:
            print(f"Fehler beim Starten der Aufnahme. Fehler: {str(e)}")
            messagebox.showerror("Aufnahme Fehler", f"Fehler beim Starten der Aufnahme. Fehler: {str(e)}")

    def download_latest_video(self, stnr, versuch):
        dt = self.date_and_time()
        try:
            self.camera.downloadLastMedia(custom_filename=f"{dt}-{stnr}-V{versuch}.MP4")
            print(f"Neuestes Video erfolgreich heruntergeladen um {dt}")
        except Exception as e:
            print(f"Fehler beim Herunterladen des neuesten Videos. Fehler: {str(e)}")
            messagebox.showerror("Download Fehler", f"Fehler beim Herunterladen des neuesten Videos. Fehler: {str(e)}")


class GoProControllerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Absprungskontrolle für Horizontalsprünge")

        self.gopro_controller = GoProController()

        # Bild laden
        image_path = "resources/LogoVTO.png"
        original_image = tk.PhotoImage(file=image_path)

        # Bild auf eine maximale Breite von 400 Pixel skalieren
        max_width = 400
        image_width = original_image.width()
        if image_width > max_width:
            scale_factor = max_width / image_width
            self.logo_image = original_image.subsample(int(1 / scale_factor), int(1 / scale_factor))
        else:
            self.logo_image = original_image

        self.logo_label = tk.Label(master, image=self.logo_image)
        self.logo_label.grid(row=0, column=0, columnspan=4, pady=20,
                             sticky="nsew")

        # Beschriftungen und Eingabefelder für "StNr" und "Versuch Nr." erstellen
        label_font = ('Arial', 12, 'bold')  # Schriftgröße verdoppeln
        entry_font = ('Arial', 10)  # Schriftgröße für Eingabefelder

        self.versuch_label = tk.Label(master, text="Versuch Nr.:", font=label_font)
        self.versuch_label.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="e")
        self.versuch_entry = tk.Entry(master, font=entry_font, width=10, justify="center", bd=2, relief="groove")
        self.versuch_entry.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="w")

        self.stnr_label = tk.Label(master, text="StNr:", font=label_font)
        self.stnr_label.grid(row=1, column=2, padx=(10, 5), pady=10, sticky="e")
        self.stnr_entry = tk.Entry(master, font=entry_font, width=10, justify="center", bd=2, relief="groove")
        self.stnr_entry.grid(row=1, column=3, padx=(0, 10), pady=10, sticky="w")

        button_width = 20
        button_height = 2

        self.record_button = tk.Button(master, text="Aufnahme starten", font=entry_font,
                                       command=self.gopro_controller.start_recording,
                                       width=button_width, height=button_height, bg="#ffb5c5")
        self.record_button.grid(row=2, column=0, padx=30, pady=15, columnspan=4, sticky="nsew")

        self.download_button = tk.Button(master, text="Neuestes Video herunterladen", font=entry_font,
                                         command=lambda: self.gopro_controller.download_latest_video(
                                             self.stnr_entry.get(), self.versuch_entry.get()),
                                         width=button_width, height=button_height, bg="#ffff00")
        self.download_button.grid(row=3, column=0, padx=30, pady=15, columnspan=4, sticky="nsew")

        self.exit_button = tk.Button(master, text="Beenden", font=entry_font, command=self.master.destroy,
                                     width=button_width,
                                     height=button_height, bg="#90ee90")
        self.exit_button.grid(row=4, column=0, padx=30, pady=15, columnspan=4, sticky="nsew")

        # Minimale Größe des Fensters setzen
        master.minsize(500, 600)

        # Zeilen- und Spaltenverhältnisse für die Größenänderung konfigurieren
        for i in range(5):  # Anzahl der Zeilen
            master.grid_rowconfigure(i, weight=1)
        for i in range(4):  # Anzahl der Spalten
            master.grid_columnconfigure(i, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("resources/picto.ico")
    app = GoProControllerGUI(root)
    root.mainloop()
