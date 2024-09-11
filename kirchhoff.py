import tkinter as tk
from tkinter import messagebox
import numpy as np


class CircuitSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Circuit Solver")

        # Initialize the number of resistors and nodes (Knoten)
        self.num_resistors = 3
        self.num_nodes = self.num_resistors + 1  # N Resistor = N+1 Nodes (Knoten)

        # Create buttons to add/remove resistors
        self.add_button = tk.Button(master, text="+", command=self.add_resistor)
        self.add_button.grid(row=0, column=4)
        self.remove_button = tk.Button(master, text="-", command=self.remove_resistor)
        self.remove_button.grid(row=0, column=5)

        # Initialize entries lists
        self.entries = []
        self.voltage_entries = []

        # Create initial entries
        self.create_entries()

        # Calculate button
        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=1, columnspan=6)

        # Result label
        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=2, columnspan=6)

    def create_entries(self):
        for i in range(self.num_resistors):
            tk.Label(self.master, text=f"Resistor {i + 1} (Ohms)").grid(row=i + 3, column=0)
            entry = tk.Entry(self.master)
            entry.grid(row=i + 3, column=1)
            self.entries.append(entry)

        tk.Label(self.master, text="Source Voltage (V)").grid(row=self.num_resistors + 3, column=0)
        entry = tk.Entry(self.master)
        entry.grid(row=self.num_resistors + 3, column=1)
        self.voltage_entries.append(entry)

    def add_resistor(self):
        self.num_resistors += 1
        self.num_nodes = self.num_resistors + 1  # Update node count
        self.clear_entries()
        self.create_entries()

    def remove_resistor(self):
        if self.num_resistors > 1:
            self.num_resistors -= 1
            self.num_nodes = self.num_resistors + 1  # Update node count
            self.clear_entries()
            self.create_entries()
        else:
            messagebox.showwarning("Warning", "You must have at least one resistor.")

    def clear_entries(self):
        for widget in self.master.grid_slaves():
            if int(widget.grid_info()["row"]) > 2:
                widget.grid_forget()
        self.entries = []
        self.voltage_entries = []

    def calculate(self):
        try:
            # Get resistor values from entries
            resistors = np.array([float(entry.get()) for entry in self.entries])
            source_voltage = float(self.voltage_entries[0].get())  # Eingabe der Spannungsquelle

            # Create a resistance matrix (Ohm's law: V = IR, so R = V/I)
            R = np.diag(resistors)

            # Kirchhoff's current law (KCL) and Ohm's law for nodal analysis
            # For simplicity, assume a voltage of 0 at the ground node (last node)
            voltages = np.zeros(self.num_nodes)
            voltages[0] = source_voltage  # Set source voltage at the first node

            # Calculate total resistance and current
            total_resistance = np.sum(resistors)
            current = source_voltage / total_resistance  # I = V / R

            # Calculate voltage drop across each resistor
            voltage_drops = current * resistors

            # Calculate the node voltages (relative to ground)
            for i in range(1, self.num_nodes):
                voltages[i] = voltages[i - 1] - voltage_drops[i - 1]

            # Display the results
            result_text = f"Source Voltage: {source_voltage:.2f} V\n"
            result_text += "Calculated Node Voltages (V):\n"
            for i in range(1, self.num_nodes):
                result_text += f"V{i}: {voltages[i]:.2f} V\n"

            self.result_label.config(text=result_text)

        except ValueError:
            messagebox.showerror("Input error", "Please enter valid numbers for resistors and voltage.")
        except np.linalg.LinAlgError:
            messagebox.showerror("Calculation error", "System of equations could not be solved.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CircuitSolver(root)
    root.mainloop()
