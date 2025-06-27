import tkinter as tk
import random
import time
import math

class Particle:
    """
    Represents a single gas particle in the simulation.
    Handles its position, velocity, state (gas/dissolved), and drawing.
    """
    def __init__(self, canvas_width, liquid_level, state='gas'):
        self.radius = 3
        self.state = state  # 'gas' or 'dissolved'
        self.color_gas = '#4299e1'  # Blue
        self.color_dissolved = '#805ad5'  # Purple
        self.color = self.color_gas if self.state == 'gas' else self.color_dissolved
        self.canvas_width = canvas_width
        self.liquid_level = liquid_level

        self.spawn(canvas_width, liquid_level)

    def spawn(self, canvas_width, liquid_level):
        """
        Initializes particle's position and velocity based on its state and canvas dimensions.
        """
        if self.state == 'gas':
            self.x = random.uniform(self.radius, canvas_width - self.radius)
            self.y = random.uniform(self.radius, liquid_level - self.radius)
        else: # state == 'dissolved'
            self.x = random.uniform(self.radius, canvas_width - self.radius)
            # Ensure dissolved particles spawn strictly below the liquid level and above the canvas bottom
            self.y = random.uniform(liquid_level + self.radius, GasSolubilitySimulation.canvas_height - self.radius)
        
        angle = random.uniform(0, 2 * math.pi) # 2 * PI
        speed = 1.5 + random.uniform(0, 0.5)  # Base speed
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)

    def draw(self, canvas):
        """
        Draws the particle on the given Tkinter canvas.
        """
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius,
                           fill=self.color, outline="")

    def update(self, delta_time, temperature, canvas_width, canvas_height, liquid_level):
        """
        Updates the particle's position and handles collisions with boundaries.
        Includes overshoot correction to prevent particles from passing through walls.
        """
        temp_factor = temperature * 0.5 + 0.5  # Scale temperature effect
        self.x += self.vx * temp_factor * delta_time
        self.y += self.vy * temp_factor * delta_time

        # Boundary collisions for gas phase
        if self.state == 'gas':
            if self.x - self.radius < 0: # Left wall
                self.x = self.radius + (0 - (self.x - self.radius)) # Correct for overshoot
                self.vx *= -1
            elif self.x + self.radius > canvas_width: # Right wall
                self.x = canvas_width - self.radius - (self.x + self.radius - canvas_width) # Correct for overshoot
                self.vx *= -1
            if self.y - self.radius < 0: # Top wall
                self.y = self.radius + (0 - (self.y - self.radius)) # Correct for overshoot
                self.vy *= -1
        else: # Dissolved phase particles stay within liquid boundaries
            if self.x - self.radius < 0: # Left wall
                self.x = self.radius + (0 - (self.x - self.radius)) # Correct for overshoot
                self.vx *= -1
            elif self.x + self.radius > canvas_width: # Right wall
                self.x = canvas_width - self.radius - (self.x + self.radius - canvas_width) # Correct for overshoot
                self.vx *= -1
            if self.y + self.radius > canvas_height: # Bottom wall
                self.y = canvas_height - self.radius - (self.y + self.radius - canvas_height) # Correct for overshoot
                self.vy *= -1

class GasSolubilitySimulation:
    """
    Main class for the gas solubility simulation, managing the GUI and simulation logic.
    """
    canvas_width = 800
    canvas_height = 500
    liquid_height_ratio = 0.5
    initial_gas_particles = 500

    def __init__(self, master):
        self.master = master
        master.title("Gas Solubility Simulation")
        master.geometry(f"{self.canvas_width + 300}x{self.canvas_height + 50}") # Adjust window size for controls
        master.resizable(False, False) # Prevent window resizing for simplicity

        self.liquid_level = self.canvas_height * (1 - self.liquid_height_ratio)

        self.particles = []
        self.last_time = time.perf_counter()

        self.setup_ui()
        self.initialize_particles()
        self.animate()

    def setup_ui(self):
        """
        Sets up the Tkinter GUI elements (canvas, sliders, labels, buttons).
        """
        # Main frame for layout
        main_frame = tk.Frame(self.master, bg='#e0f2f7', padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Simulation Canvas
        self.canvas = tk.Canvas(main_frame, width=self.canvas_width, height=self.canvas_height,
                                bg='#f0f8ff', bd=2, relief=tk.SOLID, highlightbackground="#a7d9f7")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.canvas.create_rectangle(0, self.liquid_level, self.canvas_width, self.canvas_height,
                                     fill='#add8e6', outline="") # Draw liquid phase

        # Controls Frame
        controls_frame = tk.Frame(main_frame, bg='#f8faff', bd=1, relief=tk.SOLID, padx=15, pady=15)
        controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky='ns')

        tk.Label(controls_frame, text="Simulation Controls", font=("Inter", 14, "bold"), bg='#f8faff', fg='#333').pack(pady=10)

        # Sliders and Labels
        self.temperature = tk.DoubleVar(value=1.0)
        self.pressure = tk.DoubleVar(value=1.0)
        self.kh_value = tk.DoubleVar(value=1.0)
        self.polarity = tk.DoubleVar(value=0.5)
        self.reaction_active = tk.BooleanVar(value=False)

        self.create_slider(controls_frame, "Temperature", self.temperature, 0.1, 2.0, 0.01)
        self.create_slider(controls_frame, "Pressure", self.pressure, 0.1, 2.0, 0.01)
        self.create_slider(controls_frame, "KH Value", self.kh_value, 0.1, 2.0, 0.01, "(Lower KH = Higher Solubility)")
        self.create_slider(controls_frame, "Polarity Match", self.polarity, 0.1, 1.0, 0.01, "(Higher = Better Match)")

        # Reaction Checkbox
        tk.Checkbutton(controls_frame, text="Reaction", variable=self.reaction_active,
                       font=("Inter", 10), bg='#f8faff', fg='#333',
                       selectcolor='#d1eaff', activebackground='#f8faff',
                       command=self.update_counts).pack(pady=5) # Call update_counts to refresh UI

        # Particle Count Display
        self.gas_count_label = tk.Label(main_frame, text="Gas Particles: 0", font=("Inter", 12, "bold"), bg='#e0f2f7', fg='#333')
        self.gas_count_label.grid(row=1, column=0, sticky='w', padx=10)
        self.dissolved_count_label = tk.Label(main_frame, text="Dissolved Particles: 0", font=("Inter", 12, "bold"), bg='#e0f2f7', fg='#333')
        self.dissolved_count_label.grid(row=1, column=0, sticky='e', padx=10)

        # Reset Button
        reset_button = tk.Button(controls_frame, text="Reset", command=self.reset_simulation,
                                 bg='#007bff', fg='white', font=("Inter", 12, "bold"),
                                 relief=tk.RAISED, bd=3,
                                 activebackground='#0056b3', activeforeground='white')
        reset_button.pack(pady=20, ipadx=10, ipady=5)

    def create_slider(self, parent, label_text, variable, from_val, to_val, resolution, info_text=""):
        """
        Helper function to create a slider with its label and value display.
        """
        frame = tk.Frame(parent, bg='#f8faff')
        frame.pack(pady=8, fill=tk.X)

        tk.Label(frame, text=label_text, font=("Inter", 10, "bold"), bg='#f8faff', fg='#333').pack()
        
        slider = tk.Scale(frame, variable=variable, from_=from_val, to=to_val,
                          orient=tk.HORIZONTAL, resolution=resolution, showvalue=0,
                          command=lambda val: self.update_counts(), # Update counts on slider change
                          length=200, sliderrelief=tk.FLAT, bd=0,
                          troughcolor='#d1eaff', activebackground='#007bff', highlightthickness=0)
        slider.pack(fill=tk.X, padx=5)

        value_label = tk.Label(frame, text=f"{variable.get():.2f}", font=("Inter", 9), bg='#f8faff', fg='#555')
        value_label.pack()
        variable.trace_add("write", lambda *args: value_label.config(text=f"{variable.get():.2f}"))

        if info_text:
            tk.Label(frame, text=info_text, font=("Inter", 8), bg='#f8faff', fg='#555').pack()

    def initialize_particles(self):
        """
        Creates the initial set of gas particles.
        """
        self.particles = []
        for _ in range(self.initial_gas_particles):
            self.particles.append(Particle(self.canvas_width, self.liquid_level, 'gas'))
        self.update_counts()

    def update_counts(self):
        """
        Updates the displayed count of gas and dissolved particles.
        """
        gas_count = sum(1 for p in self.particles if p.state == 'gas')
        dissolved_count = len(self.particles) - gas_count
        self.gas_count_label.config(text=f"Gas Particles: {gas_count}")
        self.dissolved_count_label.config(text=f"Dissolved Particles: {dissolved_count}")

    def animate(self):
        """
        The main animation loop for the simulation.
        """
        current_time = time.perf_counter()
        delta_time = (current_time - self.last_time) * 60 # Scale to roughly 60 FPS
        self.last_time = current_time

        self.canvas.delete("all") # Clear canvas

        # Redraw liquid phase background
        self.canvas.create_rectangle(0, self.liquid_level, self.canvas_width, self.canvas_height,
                                     fill='#add8e6', outline="")

        particles_to_remove = []

        for i, p in enumerate(self.particles):
            p.update(delta_time, self.temperature.get(), self.canvas_width, self.canvas_height, self.liquid_level)

            # Gas-Liquid Interface Interactions
            if p.state == 'gas' and p.y + p.radius >= self.liquid_level:
                # Particle is hitting the liquid surface from gas phase
                dissolve_probability = min(1.0,
                    self.pressure.get() * self.polarity.get() / self.kh_value.get() * (1 - self.temperature.get() * 0.5) * 0.02
                )
                if random.random() < dissolve_probability:
                    p.state = 'dissolved';
                    p.color = p.color_dissolved
                    p.spawn(self.canvas_width, self.liquid_level) # Re-spawn in liquid to prevent sticking to interface
            elif p.state == 'dissolved' and p.y - p.radius <= self.liquid_level:
                # Particle is hitting the liquid surface from dissolved phase
                escape_probability = min(1.0,
                    self.temperature.get() / self.pressure.get() * (1 / self.polarity.get()) * self.kh_value.get() * 0.02
                )
                if random.random() < escape_probability:
                    p.state = 'gas'
                    p.color = p.color_gas
                    p.spawn(self.canvas_width, self.liquid_level) # Re-spawn in gas to prevent sticking to interface

            # Reaction effect: Remove dissolved particles over time
            if self.reaction_active.get() and p.state == 'dissolved':
                reaction_rate = 0.005 # Base reaction rate
                if random.random() < reaction_rate * delta_time:
                    particles_to_remove.append(i)
            
            p.draw(self.canvas)

        # Remove reacted particles (in reverse order to avoid index issues)
        for i in reversed(particles_to_remove):
            self.particles.pop(i)
        
        # If particles are removed by reaction, regenerate new gas particles to maintain total count
        while len(self.particles) < self.initial_gas_particles:
            self.particles.append(Particle(self.canvas_width, self.liquid_level, 'gas'))

        self.update_counts()
        self.master.after(16, self.animate) # Call animate again after 16ms (approx 60 FPS)

    def reset_simulation(self):
        """
        Resets all simulation parameters and re-initializes particles.
        """
        self.temperature.set(1.0)
        self.pressure.set(1.0)
        self.kh_value.set(1.0)
        self.polarity.set(0.5)
        self.reaction_active.set(False)
        self.initialize_particles()
        self.update_counts() # Ensure counts are updated immediately after reset

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    app = GasSolubilitySimulation(root)
    root.mainloop()
