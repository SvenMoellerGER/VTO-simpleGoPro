import tkinter as tk
from datetime import datetime
from goprocam import GoProCamera, constants
import tkinter.messagebox as messagebox


class GoProControllerGUI:
    def __init__(self, master):
        self.master = master
        master.title("GoPro Controller")

        self.camera = GoProCamera.GoPro()

        # Load the image
        image_path = "longjump.png"  # Replace with the actual image file path
        original_image = tk.PhotoImage(file=image_path)

        # Resize the image to have a maximum width of 400 pixels
        max_width = 300
        image_width = original_image.width()
        if image_width > max_width:
            scale_factor = max_width / image_width
            self.logo_image = original_image.subsample(int(1 / scale_factor), int(1 / scale_factor))
        else:
            self.logo_image = original_image

        # Display the image using a Label with increased pady
        self.logo_label = tk.Label(master, image=self.logo_image)
        self.logo_label.pack(pady=20)  # Increase space between image and buttons

        # Adjust the width and height of the buttons
        button_width = 25
        button_height = 2

        self.record_button = tk.Button(master, text="Start Recording", command=self.start_recording, width=button_width,
                                       height=button_height)
        self.record_button.pack(pady=10)  # Add space between buttons

        self.download_button = tk.Button(master, text="Download Latest Video", command=self.download_latest_video,
                                         width=button_width, height=button_height)
        self.download_button.pack(pady=10)  # Add space between buttons

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_application, width=button_width,
                                     height=button_height)
        self.exit_button.pack(pady=10)  # Add space between buttons

        # Set the minimum size of the window
        master.minsize(500, 300)

    def dateandtime(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return dt_string

    def start_recording(self):
        dt = self.dateandtime()
        print(f"Started recording at {dt}")
        self.camera.shoot_video(5)  # Start recording, 5 secs

    def download_latest_video(self):
        dt = self.dateandtime()
        try:
            self.camera.downloadLastMedia()
            print(f"Downloaded latest video successfully {dt}")
        except Exception as e:
            print(f"Failed to download latest video. Error: {str(e)}")
            messagebox.showerror("Download Error", f"Failed to download latest video. Error: {str(e)}")

    def exit_application(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GoProControllerGUI(root)
    root.mainloop()
