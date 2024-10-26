# AI Car Simulation

Welcome to the AI Car Simulation! This project uses Python and Pygame to simulate car movement using a NEAT (NeuroEvolution of Augmenting Topologies) neural network. The goal is to have AI-controlled cars navigate a track while avoiding collisions.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)

## Features

- Realistic car movement and rotation mechanics
- AI-controlled cars using NEAT
- Collision detection using pixel color
- Radar system for obstacle detection
- Customizable track and car graphics

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-Car-Simulation.git
2. Navigate to the project directory:
   ```bash
      cd AI-Car-Simulation

3. Install the required dependencies:
   ```bash
      pip install pygame neat-python
   

## Usage
1. Run the simulation:
   ```bash
   python main.py

Observe the AI cars navigating the track and adapting their strategies.

## How It Works
Car Class: Defines the properties and behaviors of the car, including movement, radar, and collision detection.
Radar System: Uses a set of angles to detect obstacles by checking the pixel color at the radar endpoints.
NEAT Algorithm: Evolves a population of neural networks that control the cars, optimizing their performance over generations.
Contributing
Contributions are welcome! If you have suggestions for improvements or features, feel free to open an issue or submit a pull request.
