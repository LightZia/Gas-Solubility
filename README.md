Gas Solubility Simulation
This project implements an interactive, Python-based simulation to visualize the principles of gas solubility in a liquid. Built using tkinter, it allows users to experiment with various parameters and observe their impact on the dynamic equilibrium between gas and dissolved particles.

Objective
The primary goal of this simulation is to qualitatively demonstrate and visualize the factors affecting gas solubility. It aims to help users understand:

Dynamic Equilibrium: The continuous movement of gas particles between the gas phase and the dissolved phase, and how a balance is achieved when dissolution and escape rates are equal.

Influence of Variables: The impact of physical (Temperature, Pressure) and chemical (Henry's Law Constant, Polarity, Chemical Reaction) parameters on the equilibrium concentration of dissolved gas.

Microscopic Behavior: How macroscopic phenomena like solubility emerge from the probabilistic interactions of individual particles.

Core Concepts Illustrated
The simulation models several fundamental principles from chemistry and physics:

Kinetic Molecular Theory: Particles are in constant, random motion, with their kinetic energy directly proportional to temperature.

Dynamic Equilibrium: The system reaches equilibrium when the rates of gas dissolution into the liquid and escape from the liquid are equal.

Henry's Law: The simulation demonstrates that higher gas pressure increases the probability of dissolution. A lower Henry's Law Constant (K 
H
​
 ) in this model also leads to higher solubility, inversely reflecting the P=K 
H
​
 ⋅C relationship.

Temperature Effects: Increasing temperature generally decreases gas solubility, as higher particle kinetic energy promotes escape from the liquid.

Polarity (Like Dissolves Like): A higher "Polarity Match" value increases dissolution probability, simulating stronger intermolecular attractions between gas and liquid.

Chemical Reaction (as a Sink): When enabled, this feature simulates a chemical reaction consuming dissolved gas. Consumed particles are replaced by new gas particles, illustrating how a continuous reaction prevents equilibrium and drives further dissolution.

Closed System: The total number of particles in the simulation remains constant; any particles "consumed" by the reaction are replaced by new gas particles, simulating a continuous supply.

How to Run
To run this simulation, you will need Python installed on your local machine with tkinter (usually included with Python installations).

Save the Code: Save the Python code from the gas_solubility_python_sim Canvas into a file (e.g., solubility_sim.py).

Run from Terminal: Open your terminal or command prompt, navigate to the directory where you saved the file, and execute:

python solubility_sim.py

Controls
The simulation features an interactive GUI with the following controls:

Temperature (Slider): Adjusts the kinetic energy of particles, affecting dissolution and escape rates.

Pressure (Slider): Influences the frequency of gas particle collisions with the liquid surface.

KH Value (Slider): Simulates the Henry's Law Constant; a lower value indicates higher inherent gas solubility.

Polarity Match (Slider): Represents the molecular compatibility between gas and liquid; a higher value favors dissolution.

Reaction (Checkbox): Toggles a simulated chemical reaction that consumes dissolved gas.

Reset (Button): Resets all parameters to their default values and re-initializes the particle distribution.

Project Structure (Conceptual)
The Python code is organized into two main classes:

Particle Class: Manages the individual gas molecules, including their position, velocity, state (gas/dissolved), color, and drawing on the canvas. It also handles collision detection with boundaries.

GasSolubilitySimulation Class: Oversees the entire simulation environment. This includes setting up the Tkinter GUI (canvas, sliders, labels), initializing and managing the collection of Particle objects, implementing the probabilistic logic for dissolution and escape at the gas-liquid interface, managing the chemical reaction, and running the main animation loop.

License
This project is made available under the MIT License.

MIT License

Copyright (c) [Year] [Your Name or Project Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Remember to replace [Year] with the current year and [Your Name or Project Name] with your name or the name of your GitHub repository.
