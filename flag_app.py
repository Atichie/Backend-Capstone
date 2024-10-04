import os
import tkinter as tk
from PIL import Image, ImageTk

if os.environ.get('DISPLAY', '') == '':
    print("No display found. Running in headless mode.")
else:
    class FlagApp:
        # Your FlagApp code here
        pass


# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = FlagApp()
    root.mainloop()
