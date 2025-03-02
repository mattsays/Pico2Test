import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import numpy as np
import serial
import serial.tools.list_ports
import threading
import time

# Constants
GRID_SIZE = 28
CELL_SIZE = 10
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Initialize the grid (0 = white, 255 = black in MNIST)
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)

class MNISTDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zant - MNIST Demo")
        self.root.resizable(False, False)
        
        # Serial connection
        self.serial_connection = None
        self.reading_serial = False
        
        # Main frame for organizing layout
        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)
        
        # Left frame for drawing controls
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=5)
        
        # Create canvas
        self.canvas = tk.Canvas(left_frame, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(pady=10)
        
        # Draw grid lines
        for i in range(0, WIDTH + 1, CELL_SIZE):
            self.canvas.create_line(i, 0, i, HEIGHT, fill="lightgray")
            self.canvas.create_line(0, i, WIDTH, i, fill="lightgray")
        
        # Intensity slider
        self.intensity_frame = tk.Frame(left_frame)
        self.intensity_frame.pack(pady=5)
        
        tk.Label(self.intensity_frame, text="Drawing Intensity:").pack(side=tk.LEFT)
        self.intensity_slider = tk.Scale(self.intensity_frame, from_=1, to=9, orient=tk.HORIZONTAL)
        self.intensity_slider.set(9)
        self.intensity_slider.pack(side=tk.LEFT)
        
        # Buttons
        self.button_frame = tk.Frame(left_frame)
        self.button_frame.pack(pady=5)
        
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.send_button = tk.Button(self.button_frame, text="Send to Pico", command=self.send_to_pico)
        self.send_button.pack(side=tk.LEFT, padx=5)
        self.send_button.config(state=tk.DISABLED)  # Initially disabled until connected
        
        # Right frame for serial controls and output
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=5)
        
        # Serial Connection Frame
        self.serial_frame = tk.Frame(right_frame)
        self.serial_frame.pack(pady=5, fill=tk.X)
        
        tk.Label(self.serial_frame, text="Port:").pack(side=tk.LEFT)
        self.port_combobox = ttk.Combobox(self.serial_frame, width=15)
        self.port_combobox.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = tk.Button(self.serial_frame, text="Refresh", command=self.refresh_ports)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        
        self.connect_button = tk.Button(self.serial_frame, text="Connect", command=self.toggle_connection)
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        # Output box for serial data
        tk.Label(right_frame, text="Serial Output:").pack(anchor=tk.W)
        self.output_text = scrolledtext.ScrolledText(right_frame, width=40, height=20, wrap=tk.WORD)
        self.output_text.pack(pady=5, fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)
        
        # Clear output button
        self.clear_output_button = tk.Button(right_frame, text="Clear Output", command=self.clear_output)
        self.clear_output_button.pack(pady=5)
        
        # Refresh the port list initially
        self.refresh_ports()
        
        # Mouse events
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.draw)
        
        # Status label
        self.status_label = tk.Label(root, text="Draw a digit (28x28)", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def refresh_ports(self):
        # Get list of available serial ports
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combobox['values'] = ports
        
        # Select first port if available
        if ports:
            self.port_combobox.current(0)
    
    def toggle_connection(self):
        if self.serial_connection is None:
            # Connect
            try:
                selected_port = self.port_combobox.get()
                if not selected_port:
                    messagebox.showerror("Error", "No port selected")
                    return
                
                self.serial_connection = serial.Serial(selected_port, 115200, timeout=1)
                self.connect_button.config(text="Disconnect")
                self.send_button.config(state=tk.NORMAL)
                self.status_label.config(text=f"Connected to {selected_port}")
                
                # Start reading serial data
                self.reading_serial = True
                self.serial_reader_thread = threading.Thread(target=self.read_serial_data)
                self.serial_reader_thread.daemon = True
                self.serial_reader_thread.start()
                
            except Exception as e:
                messagebox.showerror("Connection Error", str(e))
                self.serial_connection = None
        else:
            # Disconnect
            self.reading_serial = False
            try:
                self.serial_connection.close()
            except:
                pass
            finally:
                self.serial_connection = None
                self.connect_button.config(text="Connect")
                self.send_button.config(state=tk.DISABLED)
                self.status_label.config(text="Disconnected")
    
    def read_serial_data(self):
        """Thread function to continuously read data from serial"""
        while self.reading_serial and self.serial_connection:
            try:
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.readline().decode('utf-8').strip()
                    if data:
                        self.update_output_text(data + '\n')
            except Exception as e:
                self.update_output_text(f"Serial read error: {str(e)}\n")
                break
    
    def update_output_text(self, text):
        """Update the output text box from the main thread"""
        def update():
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, text)
            self.output_text.see(tk.END)  # Auto-scroll to the end
            self.output_text.config(state=tk.DISABLED)
        self.root.after(0, update)  # Schedule the update in the main thread
    
    def clear_output(self):
        """Clear the output text box"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def draw(self, event):
        # Convert canvas coordinates to grid coordinates
        grid_x = event.x // CELL_SIZE
        grid_y = event.y // CELL_SIZE
        
        # Ensure we're within bounds
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            # Get intensity from slider (scale 1-9 to intensity values)
            intensity_value = self.intensity_slider.get() * 28
            
            # Draw with a brush (3x3 area with center being darkest)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = grid_x + dx, grid_y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        # Center pixel gets full intensity, surrounding pixels get less
                        if dx == 0 and dy == 0:
                            new_val = min(255, grid[ny][nx] + intensity_value)
                        else:
                            new_val = min(255, grid[ny][nx] + intensity_value // 2)
                        
                        grid[ny][nx] = new_val
                        
                        # Calculate color (0 = white, 255 = black)
                        color_val = 255 - new_val
                        color = f'#{color_val:02x}{color_val:02x}{color_val:02x}'
                        
                        # Draw rectangle on canvas
                        x1, y1 = nx * CELL_SIZE, ny * CELL_SIZE
                        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
    
    def clear_canvas(self):
        # Clear grid
        grid.fill(0)
        
        # Clear canvas
        self.canvas.delete("all")
        
        # Redraw grid lines
        for i in range(0, WIDTH + 1, CELL_SIZE):
            self.canvas.create_line(i, 0, i, HEIGHT, fill="lightgray")
            self.canvas.create_line(0, i, WIDTH, i, fill="lightgray")
    
    def send_to_pico(self):
        if not self.serial_connection:
            messagebox.showerror("Error", "Not connected to a serial port")
            return
        
        try:
            # First send the total number of values (28x28 = 784)
            total_values = GRID_SIZE * GRID_SIZE
            self.update_output_text(f"Sending {total_values} values...\n")
            
            # Send each pixel value one by one
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    # Send the value and wait for a brief moment
                    self.serial_connection.write(f"{255 if grid[y][x] > 0 else 0}\n".encode())
                    if (y * GRID_SIZE + x) % 100 == 0:  # Update status every 100 pixels
                        self.status_label.config(text=f"Sending: {y * GRID_SIZE + x + 1}/{total_values}")
                        self.root.update()  # Keep UI responsive
            
            self.status_label.config(text="Digit sent to Pico successfully")
            self.update_output_text("All data sent successfully.\n")
            
        except Exception as e:
            error_msg = f"Failed to send data: {str(e)}"
            self.status_label.config(text=error_msg)
            self.update_output_text(error_msg + "\n")
            messagebox.showerror("Send Error", error_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = MNISTDrawingApp(root)
    root.mainloop()