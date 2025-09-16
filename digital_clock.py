import tkinter as tk
from time import strftime

# Create the main application window
root = tk.Tk()
root.title("Digital Clock")

# Define the clock Label
clock_label = tk.Label(root,
                       font=("Helvetica", 48),
                       bg="black", fg="cyan")
clock_label.pack(anchor="center", fill="both", expand=True)

# Function to update the time
def update_time():
    current_time = strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time)

# Start the clock
update_time()

# Run the application
root.mainloop()
import tkinter as tk
from time import strftime

# Create the main application window
root = tk.Tk()
root.title("Digital Clock")

# Define the clock Label
clock_label = tk.Label(root,
                       font=("Helvetica", 48),
                       bg="black", fg="cyan")
clock_label.pack(anchor="center", fill="both", expand=True)

# Function to update the time
def update_time():
    current_time = strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time)

# Start the clock
update_time()

# Run the application
root.mainloop()
