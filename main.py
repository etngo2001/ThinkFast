import tkinter as tk

window = tk.Tk()
window.title("Think Fast Client")
window_icon = tk.PhotoImage(file='logo.png')
window.iconphoto(True, window_icon)

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size
window_width = 1280
window_height = 720

# Calculate the X and Y coordinates to center the window
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


window.mainloop()