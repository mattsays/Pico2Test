import tkinter as tk
from tkinter import messagebox
import numpy as np

# Constants
GRID_SIZE = 28
CELL_SIZE = 10
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Initialize the grid (0 = white, 255 = black in MNIST)
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)

class MNISTDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MNIST Digit Drawing")
        self.root.resizable(False, False)
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(padx=10, pady=10)
        
        # Draw grid lines
        for i in range(0, WIDTH + 1, CELL_SIZE):
            self.canvas.create_line(i, 0, i, HEIGHT, fill="lightgray")
            self.canvas.create_line(0, i, WIDTH, i, fill="lightgray")
        
        # Intensity slider
        self.intensity_frame = tk.Frame(root)
        self.intensity_frame.pack(pady=5)
        
        tk.Label(self.intensity_frame, text="Drawing Intensity:").pack(side=tk.LEFT)
        self.intensity_slider = tk.Scale(self.intensity_frame, from_=1, to=9, orient=tk.HORIZONTAL)
        self.intensity_slider.set(9)
        self.intensity_slider.pack(side=tk.LEFT)
        
        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)
        
        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = tk.Button(self.button_frame, text="Save", command=self.export_grid)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Mouse events
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", self.draw)
        
        # Status label
        self.status_label = tk.Label(root, text="Draw a digit (28x28)", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
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
    
    def export_grid(self):
        # Format as comma-separated values in curly braces
        output = "{"
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                output += str(grid[y][x])
                if x < GRID_SIZE - 1 or y < GRID_SIZE - 1:
                    output += ", "
        output += "}"
        
        # Save to file
        with open("mnist_digit.txt", "w") as f:
            f.write(output)
        
        self.status_label.config(text="Exported to mnist_digit.txt")
        messagebox.showinfo("Export Successful", "Digit exported to mnist_digit.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = MNISTDrawingApp(root)
    root.mainloop()
