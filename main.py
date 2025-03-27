import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from math import ceil
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------------------------
# File Simulation Frame
# ------------------------------
class FileSimulationFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Simulation parameters:
        self.total_ram = None   # Total RAM for simulation (in KB)
        self.page_size = None   # Page size (in KB)
        # Files stored as: {
        #   file_name: {
        #       "size": file_size (KB),
        #       "alloc": allocated_ram (KB),
        #       "pages": required_pages (int),
        #       "reference_string": [list_of_page_references]
        #   }
        # }
        self.files = {}
        self.setup_ui()
        self.create_graph()
        self.create_log_panel()

    def setup_ui(self):
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Total RAM input (adjustable)
        tk.Label(control_frame, text="Total RAM (KB):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.total_ram_entry = tk.Entry(control_frame, width=25)
        self.total_ram_entry.grid(row=0, column=1, padx=5, pady=5)

        # Page Size input (adjustable)
        tk.Label(control_frame, text="Page Size (KB):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.page_size_entry = tk.Entry(control_frame, width=25)
        self.page_size_entry.grid(row=1, column=1, padx=5, pady=5)

        # File Name Input
        tk.Label(control_frame, text="File Name:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.file_name_entry = tk.Entry(control_frame, width=25)
        self.file_name_entry.grid(row=2, column=1, padx=5, pady=5)

        # File Size Input
        tk.Label(control_frame, text="File Size (KB):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.file_size_entry = tk.Entry(control_frame, width=25)
        self.file_size_entry.grid(row=3, column=1, padx=5, pady=5)

        # RAM Allocated for File Input
        tk.Label(control_frame, text="RAM Allocated (KB):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.ram_alloc_entry = tk.Entry(control_frame, width=25)
        self.ram_alloc_entry.grid(row=4, column=1, padx=5, pady=5)

        # Reference String Length
        tk.Label(control_frame, text="Ref String Length:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.ref_length_entry = tk.Entry(control_frame, width=25)
        self.ref_length_entry.grid(row=5, column=1, padx=5, pady=5)

        # Add File Button
        add_file_button = tk.Button(control_frame, text="Add File", command=self.add_file)
        add_file_button.grid(row=6, column=0, columnspan=2, pady=10)

    def create_graph(self):
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.update_graph()

    def create_log_panel(self):
        log_frame = tk.Frame(self)
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(log_frame, text="File Simulation Log:").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def add_file(self):
        # Set total RAM and page size if not yet set
        if self.total_ram is None:
            total_ram_str = self.total_ram_entry.get().strip()
            if not total_ram_str:
                messagebox.showerror("Input Error", "Please set the Total RAM for simulation!")
                return
            try:
                self.total_ram = float(total_ram_str)
            except ValueError:
                messagebox.showerror("Input Error", "Total RAM must be a valid number!")
                return
        if self.page_size is None:
            page_size_str = self.page_size_entry.get().strip()
            if not page_size_str:
                messagebox.showerror("Input Error", "Please set the Page Size!")
                return
            try:
                self.page_size = float(page_size_str)
            except ValueError:
                messagebox.showerror("Input Error", "Page Size must be a valid number!")
                return

        file_name = self.file_name_entry.get().strip()
        file_size_str = self.file_size_entry.get().strip()
        ram_alloc_str = self.ram_alloc_entry.get().strip()
        ref_length_str = self.ref_length_entry.get().strip()

        if not file_name or not file_size_str or not ram_alloc_str or not ref_length_str:
            messagebox.showerror("Input Error", "All file details must be provided!")
            return
        try:
            file_size = float(file_size_str)
            ram_alloc = float(ram_alloc_str)
            ref_length = int(ref_length_str)
        except ValueError:
            messagebox.showerror("Input Error", "File size, RAM allocated, and reference length must be valid numbers!")
            return

        required_pages = ceil(file_size / self.page_size)

        # Generate a random reference string of length ref_length, each referencing a page from 0..(required_pages-1)
        ref_string = [random.randint(0, max(0, required_pages - 1)) for _ in range(ref_length)]

        self.files[file_name] = {
            "size": file_size,
            "alloc": ram_alloc,
            "pages": required_pages,
            "reference_string": ref_string
        }
        self.log(f"Added file '{file_name}': Size={file_size}KB, Alloc={ram_alloc}KB, Pages={required_pages}, RefString={ref_string}")
        # Clear the file input fields
        self.file_name_entry.delete(0, tk.END)
        self.file_size_entry.delete(0, tk.END)
        self.ram_alloc_entry.delete(0, tk.END)
        self.ref_length_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"File '{file_name}' added!")
        self.update_graph()

    def update_graph(self):
        self.ax.clear()
        if not self.files:
            self.ax.text(0.5, 0.5, "No files added yet", ha="center", va="center", transform=self.ax.transAxes)
        else:
            file_names = sorted(self.files.keys())
            file_sizes = [self.files[f]["size"] for f in file_names]
            self.ax.bar(file_names, file_sizes, color="skyblue")
            self.ax.set_xlabel("File Name")
            self.ax.set_ylabel("File Size (KB)")
            self.ax.set_title("Files: Sizes")
            self.ax.set_ylim(0, max(file_sizes) + 10)
        self.canvas.draw()

    def get_simulation_data(self):
        """Return simulation data: total_ram, page_size, and files dictionary."""
        return self.total_ram, self.page_size, self.files

# ------------------------------
# Paging Simulation Frame with Real Reference-String Logic
# ------------------------------
class PagingSimulationFrame(tk.Frame):
    def __init__(self, master, file_sim_frame):
        super().__init__(master)
        self.file_sim_frame = file_sim_frame
        self.setup_ui()
        self.create_graph()
        self.create_log_panel()

    def setup_ui(self):
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Dropdown for algorithm selection
        tk.Label(control_frame, text="Replacement Algorithm:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.algorithm_var = tk.StringVar(value="FIFO")
        algo_options = ["FIFO", "LRU", "Optimal"]
        self.algo_menu = ttk.Combobox(control_frame, textvariable=self.algorithm_var, values=algo_options, state="readonly")
        self.algo_menu.grid(row=0, column=1, padx=5, pady=5)

        # Refresh Simulation Button
        refresh_button = tk.Button(control_frame, text="Refresh Paging Simulation", command=self.refresh_simulation)
        refresh_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_graph(self):
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.update_graph({})

    def create_log_panel(self):
        log_frame = tk.Frame(self)
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(log_frame, text="Paging Simulation Log:").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def refresh_simulation(self):
        total_ram, page_size, files = self.file_sim_frame.get_simulation_data()
        if total_ram is None or page_size is None or not files:
            messagebox.showerror("Data Error", "Please set Total RAM, Page Size, and add at least one file in File Simulation!")
            return

        # Simulate each file's reference string with chosen replacement algorithm
        paging_faults = {}
        algo = self.algorithm_var.get()
        self.log(f"Refreshing Paging Simulation with {algo}...")

        for fname in sorted(files.keys()):
            data = files[fname]
            required_pages = data["pages"]
            ref_string = data["reference_string"]
            # Determine how many frames are actually allocated:
            allocated_pages = ceil(data["alloc"] / page_size)

            # If allocated_pages=0, then we can't load any pages => every reference is a fault
            # If allocated_pages >= required_pages => we can keep all pages in memory => minimal faults
            faults = self.simulate_paging(algo, required_pages, ref_string, allocated_pages)
            paging_faults[fname] = faults
            self.log(f"File '{fname}': Pages={required_pages}, AllocFrames={allocated_pages}, Faults={faults}")

        self.update_graph(paging_faults)

    def simulate_paging(self, algo, required_pages, ref_string, allocated_frames):
        """Simulate page references using FIFO, LRU, or Optimal on a single file's reference string."""
        if allocated_frames <= 0:
            # All references will fault if we have zero frames allocated
            return len(ref_string)
        elif allocated_frames >= required_pages:
            # If allocated frames >= required_pages, we can keep all pages in memory
            # So the only faults are the first time we load each distinct page
            distinct_pages = set(ref_string)
            return len(distinct_pages)

        frames = []      # to hold pages in memory
        faults = 0
        # For LRU, track usage
        usage_map = {}   # page -> last used index
        # For Optimal, we look ahead in the reference string

        for i, page in enumerate(ref_string):
            if page in frames:
                # Hit
                if algo == "LRU":
                    usage_map[page] = i  # update last used index
            else:
                # Fault
                faults += 1
                if len(frames) < allocated_frames:
                    frames.append(page)
                    if algo == "LRU":
                        usage_map[page] = i
                else:
                    # Evict a page
                    if algo == "FIFO":
                        frames.pop(0)  # remove the oldest
                        frames.append(page)
                    elif algo == "LRU":
                        # Evict least recently used
                        lru_page = min(usage_map, key=usage_map.get)
                        frames.remove(lru_page)
                        usage_map.pop(lru_page)
                        frames.append(page)
                        usage_map[page] = i
                    elif algo == "Optimal":
                        # Evict the page that will not be used for the longest time
                        frames = self.evict_optimal(frames, ref_string, i)
                        frames.append(page)
        return faults

    def evict_optimal(self, frames, ref_string, current_index):
        """Evict the page from frames that won't be used for the longest time in the future."""
        future_indices = {}
        for page in frames:
            # Look ahead
            if page in ref_string[current_index+1:]:
                future_indices[page] = ref_string[current_index+1:].index(page) + current_index + 1
            else:
                future_indices[page] = float('inf')

        # Evict the page with the farthest future index
        page_to_evict = max(future_indices, key=future_indices.get)
        frames.remove(page_to_evict)
        return frames

    def update_graph(self, faults):
        self.ax.clear()
        if not faults:
            self.ax.text(0.5, 0.5, "No data to display.\nRefresh after adding files.", ha="center", va="center", transform=self.ax.transAxes)
        else:
            file_names = sorted(faults.keys())
            fault_counts = [faults[f] for f in file_names]
            self.ax.bar(file_names, fault_counts, color="#FF9999", edgecolor="black")
            self.ax.set_xlabel("File Name (Process)")
            self.ax.set_ylabel("Page Fault Count")
            self.ax.set_title("Paging Simulation: Page Faults (Reference-String Based)")
            self.ax.set_ylim(0, max(fault_counts) + 2)
        self.canvas.draw()

# ------------------------------
# Segmentation Simulation Frame (Same as before, or your existing logic)
# ------------------------------
class SegmentationSimulationFrame(tk.Frame):
    def __init__(self, master, file_sim_frame):
        super().__init__(master)
        self.file_sim_frame = file_sim_frame
        self.setup_ui()
        self.create_graph()
        self.create_log_panel()

    def setup_ui(self):
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        refresh_button = tk.Button(control_frame, text="Refresh Segmentation Simulation", command=self.refresh_simulation)
        refresh_button.pack(padx=5, pady=5)

    def create_graph(self):
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.update_graph({}, {})

    def create_log_panel(self):
        log_frame = tk.Frame(self)
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(log_frame, text="Segmentation Simulation Log:").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def refresh_simulation(self):
        total_ram, page_size, files = self.file_sim_frame.get_simulation_data()
        if total_ram is None or not files:
            messagebox.showerror("Data Error", "Please set Total RAM and add at least one file in File Simulation!")
            return

        required = {}
        allocated = {}
        self.log("Refreshing Segmentation Simulation:")
        for fname in sorted(files.keys()):
            fsize = files[fname]["size"]
            ram_alloc = files[fname]["alloc"]
            required[fname] = fsize
            allocated[fname] = ram_alloc
            self.log(f"File '{fname}': Required segment size = {fsize} KB, Allocated = {ram_alloc} KB")
        self.update_graph(required, allocated)

    def update_graph(self, required, allocated):
        self.ax.clear()
        if not required or not allocated:
            self.ax.text(0.5, 0.5, "No data to display.\nRefresh after adding files.", ha="center", va="center", transform=self.ax.transAxes)
        else:
            file_names = sorted(required.keys())
            req_values = [required[f] for f in file_names]
            alloc_values = [allocated[f] for f in file_names]
            x = range(len(file_names))
            width = 0.35

            self.ax.bar([i - width/2 for i in x], req_values, width=width, label="Required (File Size)", color="orchid")
            self.ax.bar([i + width/2 for i in x], alloc_values, width=width, label="Allocated (RAM)", color="teal")
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(file_names)
            self.ax.set_xlabel("File Name (Process)")
            self.ax.set_ylabel("Size (KB)")
            self.ax.set_title("Segmentation Simulation: Required vs Allocated")
            self.ax.legend()
            self.ax.set_ylim(0, max(max(req_values), max(alloc_values)) + 50)
        self.canvas.draw()

# ------------------------------
# Main Application with Notebook
# ------------------------------
class SimulationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Virtual Memory Management Simulation (Reference String Edition)")
        self.geometry("1000x900")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create File Simulation tab (shared simulation data)
        self.file_sim_tab = FileSimulationFrame(self.notebook)
        # Create Paging and Segmentation tabs and pass file simulation data
        self.paging_tab = PagingSimulationFrame(self.notebook, self.file_sim_tab)
        self.segmentation_tab = SegmentationSimulationFrame(self.notebook, self.file_sim_tab)

        self.notebook.add(self.file_sim_tab, text="File Simulation")
        self.notebook.add(self.paging_tab, text="Paging Simulation")
        self.notebook.add(self.segmentation_tab, text="Segmentation Simulation")

if __name__ == "__main__":
    app = SimulationApp()
    app.mainloop()
