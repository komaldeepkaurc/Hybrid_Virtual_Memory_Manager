# Hybrid Virtual Memory Management

**Course:** CSE316 - Operating Systems  
**Institution:** Lovely Professional University

## Project Overview

This project simulates a **Hybrid Virtual Memory Management** system using Python. It demonstrates key memory management techniques such as paging and segmentation by simulating page faults using multiple page replacement algorithms (FIFO, LRU, and Optimal) on reference strings. The simulation is presented via an interactive GUI with live-updating charts and detailed log panels to help analyze and understand the behavior of different memory management strategies.

## Features

- **Hybrid Simulation:**  
  - **Paging Simulation:**  
    - Simulates page faults based on real reference strings.
    - Supports three page replacement algorithms: FIFO, LRU, and Optimal.
    - Displays page fault counts graphically.
  - **Segmentation Simulation:**  
    - Compares required segment sizes versus allocated RAM.
    - Visualizes segmentation allocation with grouped bar charts.
  - **File Simulation:**  
    - Allows setting simulation parameters (Total RAM and Page Size).
    - Enables users to add files (representing processes) with file size, allocated RAM, and a generated reference string.
    - Provides a log panel to track file additions and parameter settings.

- **Interactive GUI:**  
  - Built using Tkinter and Matplotlib.
  - Live updating graphs and log panels for detailed simulation insights.
  - Adjustable simulation parameters and algorithm selection.

## Installation

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/your-username/hybrid-virtual-memory-management.git
   cd hybrid-virtual-memory-management
