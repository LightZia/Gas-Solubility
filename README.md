This document explains the underlying concepts and the working mechanism of the Python-based Gas Solubility Simulation.

Objective of the Simulation
The primary objective of this simulation is to provide a qualitative and interactive visualization of the factors affecting gas solubility in a liquid. It aims to help users understand:

Dynamic Equilibrium: How gas particles constantly move between the gas phase and the dissolved phase, reaching a balance where the rate of dissolution equals the rate of escape.

Influence of Variables: The impact of various physical and chemical parameters (Temperature, Pressure, Henry's Law Constant, Polarity, and Chemical Reaction) on this equilibrium and the overall concentration of dissolved gas.

Microscopic Behavior: How macroscopic phenomena like solubility emerge from the probabilistic interactions of individual particles.

Core Concepts Represented
The simulation models several fundamental principles of chemistry and physics related to gas solubility:

Kinetic Molecular Theory: Particles are in constant, random motion. Their kinetic energy is directly related to temperature. Higher temperature means faster-moving particles.

Dynamic Equilibrium: Gas molecules are continuously dissolving into the liquid and escaping from it. When the rates of these two processes become equal, the system reaches a state of dynamic equilibrium, and the net concentration of dissolved gas remains constant, even though individual particles are still moving between phases.

Henry's Law: This law states that the amount of a given gas dissolved in a given type and volume of liquid is directly proportional to the partial pressure of the gas in equilibrium with the liquid. In the simulation:

Pressure: Higher pressure increases the frequency of gas particles colliding with the liquid surface, thereby increasing the probability of dissolution.

Henry's Law Constant (K 
H
​
 ): While Henry's Law is typically stated as P=K 
H
​
 ⋅C (where P is partial pressure, C is concentration), in our simulation, a lower KH Value increases the dissolution probability. This inversely models the effect: a lower K 
H
​
  means a higher solubility at a given pressure.

Temperature Effects: Gas solubility generally decreases with increasing temperature.

In the simulation, higher temperature increases the kinetic energy of both gas and dissolved particles. This makes it easier for dissolved particles to overcome intermolecular forces in the liquid and escape, and harder for gas particles to be "captured" by the liquid.

Polarity (Like Dissolves Like): This principle states that substances with similar intermolecular forces tend to dissolve in each other.

In the simulation, a higher Polarity Match increases the probability of dissolution. This represents a stronger attraction between the gas and liquid molecules, making it more favorable for the gas to dissolve.

Chemical Reaction (as a Sink): If a dissolved gas reacts chemically with the liquid or a component in the liquid, it is continuously removed from the solution.

In the simulation, enabling the Reaction checkbox causes dissolved particles to be periodically removed. To maintain a constant total particle count (representing a continuous supply of gas), new gas particles are introduced. This demonstrates how a reaction prevents the system from reaching equilibrium, as the dissolved gas is constantly consumed, driving further dissolution.

Closed System: The total number of particles in the simulation remains constant. When particles are removed due to a "reaction," an equal number of new gas particles are introduced at the top to maintain the particle count, simulating a continuous supply of gas to the system.

How the Code Works
The Python code is structured into two main classes: Particle and GasSolubilitySimulation, leveraging the tkinter library for the graphical user interface.

1. Particle Class
Purpose: Represents a single gas molecule in the simulation.

Attributes:

x, y: Current position of the particle on the canvas.

vx, vy: Velocity components (horizontal and vertical).

radius: Size of the particle.

state: 'gas' or 'dissolved', determining its current phase.

color: Changes based on its state (#4299e1 for gas, #805ad5 for dissolved).

Methods:

__init__: Initializes a new particle, setting its initial position and velocity randomly within its respective phase area.

draw(canvas): Draws the particle as a circle on the Tkinter canvas.

update(delta_time, temperature, ...):

Calculates the new x and y positions based on vx, vy, temperature (which scales velocity), and delta_time (time elapsed since last frame).

Boundary Collision Detection: Checks if the particle hits any of the canvas walls (left, right, top, or bottom for dissolved particles). If so, it reverses the corresponding velocity component (vx or vy) and, importantly, corrects the position for "overshoot." This overshoot correction ensures particles don't visually "tunnel" through walls by placing them precisely at the boundary before reversing direction.

2. GasSolubilitySimulation Class
Purpose: Manages the overall simulation, including the Tkinter GUI, particle interactions, and main animation loop.

Attributes:

master: The root Tkinter window.

canvas: The Tkinter drawing area where particles and the liquid layer are displayed.

liquid_level: The y-coordinate separating the gas and liquid phases.

particles: A list containing all Particle objects in the simulation.

temperature, pressure, kh_value, polarity, reaction_active: Tkinter DoubleVar and BooleanVar objects linked to the slider/checkbox values, allowing real-time updates.

gas_count_label, dissolved_count_label: Tkinter Label widgets to display particle counts.

Methods:

__init__: Sets up the main window, initializes particle list and time tracking, calls setup_ui() to build the interface, initialize_particles() to create the initial particle set, and starts the animate() loop.

setup_ui():

Creates the main tk.Frame to organize the layout.

Instantiates the tk.Canvas for the simulation display.

Creates a separate tk.Frame for the control panel.

Uses tk.DoubleVar and tk.BooleanVar to link slider/checkbox values directly to Python variables, enabling two-way binding.

Calls create_slider() for each interactive parameter.

Sets up tk.Label widgets to display real-time gas and dissolved particle counts.

Adds a "Reset" button to revert parameters and restart the simulation.

create_slider(...): A helper method to easily create a tk.Scale (slider) widget with its corresponding label and current value display.

initialize_particles(): Populates the particles list with initial_gas_particles new Particle objects, all initially in the 'gas' state.

update_counts(): Calculates the current number of gas and dissolved particles and updates the text of their respective Tkinter labels. This method is called whenever a slider or checkbox value changes, or at each animation frame.

animate(): The core simulation loop.

Calculates delta_time to ensure consistent particle movement regardless of frame rate fluctuations.

Clears the canvas (canvas.delete("all")).

Redraws the liquid background.

Iterates through each particle in the self.particles list:

Calls p.update() to move the particle and handle wall collisions.

Gas-Liquid Interface Logic: This is where the solubility rules are applied probabilistically:

If a gas particle crosses into the liquid region (p.y + p.radius >= self.liquid_level): A random number is compared against a dissolve_probability. This probability is dynamically calculated based on pressure (positive effect), polarity (positive effect), kh_value (negative effect, as lower KH means higher solubility), and temperature (negative effect). If dissolution occurs, the particle's state changes to 'dissolved', its color changes, and it's given a new random velocity within the liquid. The p.spawn() method is called to immediately place it correctly within the liquid.

If a dissolved particle crosses into the gas region (p.y - p.radius <= self.liquid_level): A random number is compared against an escape_probability. This probability is the inverse of the dissolution logic (higher temperature, lower pressure, lower polarity, higher kh_value increase escape likelihood). If escape occurs, the particle's state changes to 'gas', its color changes, and it's given a new random velocity within the gas phase. The p.spawn() method is called to immediately place it correctly within the gas phase.

Reaction Logic: If reaction_active is true and a particle is dissolved, there's a small probability it will be added to a particles_to_remove list.

Calls p.draw() to render the particle on the canvas.

After iterating through all particles, it removes any particles marked for reaction.

Particle Regeneration: Crucially, if any particles were removed due to the "reaction," new gas particles are immediately added to the system until the initial_gas_particles count is restored. This simulates a continuous supply of gas to the system and maintains a constant total particle count.

Calls update_counts() to refresh the displayed numbers.

Schedules itself to run again after 16 milliseconds (self.master.after(16, self.animate)), aiming for approximately 60 frames per second.

reset_simulation(): Resets all DoubleVar and BooleanVar values to their default, then re-initializes all particles, effectively starting the simulation over with default parameters.

In summary, the code creates a visually intuitive model of gas solubility. By manipulating the sliders and the checkbox, you can directly observe how microscopic particle behaviors, governed by probabilistic rules derived from chemical and physical laws, lead to macroscopic changes in gas solubility.
