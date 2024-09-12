import tkinter as tk
from tkinter import messagebox, Toplevel  # Toplevel importieren
import numpy as np


class CircuitSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Schaltungssimulator")
        self.master.geometry("1200x600")  # Breiteres Fenster

        # Canvas to draw the circuit
        self.canvas = tk.Canvas(master, width=800, height=400, bg="white")  # Breiteres Canvas
        self.canvas.grid(row=0, column=0, rowspan=10, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.place_node_with_click)

        # Table frame to input resistors and voltages
        self.table_frame = tk.Frame(master)
        self.table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.resistor_entries = []
        self.knoten = []
        self.knoten_labels = []
        self.connections = {}  # Store connections (resistor values)
        self.direct_connections = []  # Store direct connections (without resistor)
        self.source_connected = False  # Check if the source is already connected
        self.ground_connected = False  # Check if ground is already connected
        self.is_placing_source = False
        self.is_placing_ground = False
        self.selected_node = None  # Track selected node for connections

        # Frame for buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Label for source voltage
        self.source_voltage_label = tk.Label(self.table_frame, text="Source Voltage (V):")
        self.source_voltage_label.grid(row=0, column=0, pady=5)
        self.source_voltage_entry = tk.Entry(self.table_frame)
        self.source_voltage_entry.grid(row=0, column=1, pady=5)

        # Real-time status label to check if all nodes are connected
        self.status_label = tk.Label(master, text="Verbindungsstatus: Nicht verbunden", fg="red")
        self.status_label.grid(row=10, column=0, columnspan=2, pady=10)

        # Matrix display
        self.matrix_display = tk.Text(master, width=50, height=20)  # Bereich zum Anzeigen der Matrix
        self.matrix_display.grid(row=0, column=2, padx=10, pady=10, rowspan=10)

        # Buttons to add source and ground
        self.add_source_button = tk.Button(self.button_frame, text="Quelle hinzufügen", command=self.add_source)
        self.add_source_button.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.add_ground_button = tk.Button(self.button_frame, text="Ground hinzufügen", command=self.add_ground)
        self.add_ground_button.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        # Calculate button
        self.calculate_button = tk.Button(self.button_frame, text="Berechnen", command=self.calculate)
        self.calculate_button.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

    def add_source(self):
        """Start placing the source node."""
        self.is_placing_source = True
        messagebox.showinfo("Info", "Klicken Sie auf das Canvas, um die Quelle zu platzieren.")

    def add_ground(self):
        """Start placing the ground node."""
        self.is_placing_ground = True
        messagebox.showinfo("Info", "Klicken Sie auf das Canvas, um Ground zu platzieren.")

    def place_node_with_click(self, event):
        """Place a node at the clicked location on the canvas."""
        x, y = event.x, event.y

        if self.is_placing_source:
            if not self.source_connected:
                self.create_source(x, y)
                self.source_connected = True
                self.is_placing_source = False
            else:
                messagebox.showerror("Fehler", "Die Quelle ist bereits verbunden.")
        elif self.is_placing_ground:
            if not self.ground_connected:
                self.create_ground(x, y)
                self.ground_connected = True
                self.is_placing_ground = False
            else:
                messagebox.showerror("Fehler", "Ground ist bereits verbunden.")
        else:
            self.create_node(x, y)
        self.update_connection_status()

    def create_source(self, x, y):
        """Create the source node (represented by a red square)."""
        self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="red")
        self.canvas.create_text(x, y - 20, text="Quelle", fill="red")

        # Draw line to the top of the canvas
        self.canvas.create_line(x, y, x, 0, fill="red", width=2)

    def create_ground(self, x, y):
        """Create the ground node (represented by a green square)."""
        self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10, fill="green")
        self.canvas.create_text(x, y - 20, text="Ground", fill="green")

        # Draw line to the bottom of the canvas
        self.canvas.create_line(x, y, x, 400, fill="green", width=2)

    def create_node(self, x, y):
        """Create a regular node at the given coordinates."""
        node_id = len(self.knoten)
        knoten = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue")
        self.knoten.append((knoten, x, y))

        # Label the node
        label = self.canvas.create_text(x, y - 15, text=f"Knoten {node_id}", fill="black")
        self.knoten_labels.append(label)

        # Button to add resistors or source
        btn = tk.Button(self.button_frame, text=f"Knoten {node_id} +",
                        command=lambda: self.select_node_for_connection(node_id))
        btn.grid(row=node_id + 4, column=0, padx=5, pady=5, sticky='nsew')

    def select_node_for_connection(self, node_id):
        """Select the current node for connecting to another node."""
        self.selected_node = node_id
        # Display connection options (Buttons for connection types)
        self.connection_options_window = Toplevel(self.master)
        self.connection_options_window.title("Verbindung Optionen")

        tk.Label(self.connection_options_window, text="Verbindungstyp wählen").pack(padx=10, pady=5)

        tk.Button(self.connection_options_window, text="Mit Widerstand verbinden",
                  command=self.connect_with_resistor).pack(padx=10, pady=5)
        tk.Button(self.connection_options_window, text="Ohne Widerstand verbinden",
                  command=self.connect_without_resistor).pack(padx=10, pady=5)
        tk.Button(self.connection_options_window, text="Mit Source verbinden", command=self.connect_with_source).pack(
            padx=10, pady=5)
        tk.Button(self.connection_options_window, text="Mit Ground verbinden", command=self.connect_with_ground).pack(
            padx=10, pady=5)
        tk.Button(self.connection_options_window, text="Abbrechen", command=self.cancel_connection).pack(padx=10,
                                                                                                         pady=5)

    def cancel_connection(self):
        """Cancel the connection process."""
        self.selected_node = None
        self.connection_options_window.destroy()

    def connect_with_resistor(self):
        """Connect the selected node to another node with a resistor."""
        self.connection_options_window.destroy()
        self.show_node_selection("Wählen Sie den Knoten, zu dem der Widerstand verbunden werden soll:",
                                 self.make_resistor_connection)

    def connect_without_resistor(self):
        """Connect the selected node to another node without a resistor."""
        self.connection_options_window.destroy()
        self.show_node_selection("Wählen Sie den Knoten, zu dem Sie direkt verbinden möchten:",
                                 self.make_direct_connection)

    def connect_with_source(self):
        """Connect the selected node to the source."""
        if not self.source_connected:
            messagebox.showerror("Fehler", "Die Quelle ist nicht verbunden!")
            return
        self.connection_options_window.destroy()
        self.make_source_connection()

    def connect_with_ground(self):
        """Connect the selected node to ground."""
        if not self.ground_connected:
            messagebox.showerror("Fehler", "Ground ist nicht verbunden!")
            return
        self.connection_options_window.destroy()
        self.make_ground_connection()

    def show_node_selection(self, title, action):
        """Show a window with buttons to select a node."""
        node_selection_window = Toplevel(self.master)
        node_selection_window.title(title)

        tk.Label(node_selection_window, text=title).pack(padx=10, pady=5)

        for i, (_, x, y) in enumerate(self.knoten):
            tk.Button(node_selection_window, text=f"Knoten {i}",
                      command=lambda i=i: self.node_selected(i, action, node_selection_window)).pack(padx=10, pady=5)

    def node_selected(self, node_id, action, window):
        """Callback when a node is selected."""
        window.destroy()
        action(node_id)

    def make_resistor_connection(self, target_node):
        """Create a resistor connection between the selected node and the target node."""
        x1, y1 = self.knoten[self.selected_node][1], self.knoten[self.selected_node][2]
        x2, y2 = self.knoten[target_node][1], self.knoten[target_node][2]
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2

        # Draw a line between nodes
        self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

        # Draw the resistor (represented by a rectangle), adjusting for direction
        if abs(x1 - x2) > abs(y1 - y2):  # Horizontal connection
            self.canvas.create_rectangle(mid_x - 20, mid_y - 5, mid_x + 20, mid_y + 5, fill="gray")
        else:  # Vertical connection
            self.canvas.create_rectangle(mid_x - 5, mid_y - 20, mid_x + 5, mid_y + 20, fill="gray")

        # Add entry for the resistor in the table
        row = len(self.resistor_entries) + 1
        label = tk.Label(self.table_frame, text=f"R{row} ({self.selected_node} -> {target_node}) (Ohms):")
        label.grid(row=row, column=0, pady=5)
        entry = tk.Entry(self.table_frame)
        entry.grid(row=row, column=1, pady=5)
        self.resistor_entries.append((entry, self.selected_node, target_node))

        # Add connection to the connection dictionary
        self.connections[(self.selected_node, target_node)] = entry

        self.update_connection_status()

    def make_direct_connection(self, target_node):
        """Create a direct connection between the selected node and the target node."""
        x1, y1 = self.knoten[self.selected_node][1], self.knoten[self.selected_node][2]
        x2, y2 = self.knoten[target_node][1], self.knoten[target_node][2]
        self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)

        # Store the direct connection
        self.direct_connections.append((self.selected_node, target_node))

        self.update_connection_status()

    def make_source_connection(self):
        """Connect the selected node to the source."""
        # Draw a line from the selected node to the source
        x1, y1 = self.knoten[self.selected_node][1], self.knoten[self.selected_node][2]
        x2, y2 = x1, 0  # Draw to the top of the canvas
        self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
        self.update_connection_status()

    def make_ground_connection(self):
        """Connect the selected node to ground."""
        # Draw a line from the selected node to ground
        x1, y1 = self.knoten[self.selected_node][1], self.knoten[self.selected_node][2]
        x2, y2 = x1, 400  # Draw to the bottom of the canvas
        self.canvas.create_line(x1, y1, x2, y2, fill="green", width=2)
        self.update_connection_status()

    def update_connection_status(self):
        """Check if all nodes are connected and update the status label."""
        num_nodes = len(self.knoten)
        if num_nodes <= 1:
            self.status_label.config(text="Verbindungsstatus: Nicht verbunden", fg="red")
            return

        # Check if all nodes are connected using DFS or BFS
        visited = [False] * num_nodes

        def dfs(node):
            visited[node] = True
            # Check direct resistor connections
            for (n1, n2), _ in self.connections.items():
                if n1 == node and not visited[n2]:
                    dfs(n2)
                elif n2 == node and not visited[n1]:
                    dfs(n1)
            # Check direct connections (without resistor)
            for n1, n2 in self.direct_connections:
                if n1 == node and not visited[n2]:
                    dfs(n2)
                elif n2 == node and not visited[n1]:
                    dfs(n1)

        # Start DFS from the first node
        dfs(0)

        if all(visited):
            self.status_label.config(text="Verbindungsstatus: Verbunden", fg="green")
        else:
            self.status_label.config(text="Verbindungsstatus: Nicht verbunden", fg="red")

    def calculate(self):
        try:
            # Get source voltage
            source_voltage = float(self.source_voltage_entry.get())

            # Create a conductance matrix (G = 1 / R)
            num_nodes = len(self.knoten)
            G = np.zeros((num_nodes, num_nodes))

            # Check if all resistor values are filled and valid
            for (node1, node2), entry in self.connections.items():
                resistance_value = entry.get()
                if not resistance_value:  # Check if field is empty
                    raise ValueError("Einige Widerstandswerte fehlen.")
                resistance = float(resistance_value)  # Convert to float
                if resistance == 0:
                    raise ValueError("Widerstandswerte dürfen nicht null sein.")
                conductance = 1 / resistance

                G[node1, node1] += conductance
                G[node2, node2] += conductance
                G[node1, node2] -= conductance
                G[node2, node1] -= conductance

            # Handle direct connections without resistors
            for n1, n2 in self.direct_connections:
                G[n1, n2] = G[n2, n1] = 0
                G[n1, n1] += 1e10  # Very high conductance to enforce equality of node voltages
                G[n2, n2] += 1e10
                G[n1, n2] -= 1e10
                G[n2, n1] -= 1e10

            # Ensure that at least one node is connected to ground
            if not self.ground_connected:
                raise ValueError("Es muss mindestens ein Knoten mit Ground verbunden sein.")

            # Voltage vector (B)
            B = np.zeros(num_nodes)
            B[0] = source_voltage  # Source is at node 0

            # Solve the system G * V = B for node voltages
            voltages = np.linalg.solve(G, B)

            # Display the system matrix in the text area
            self.display_matrix(G, B, voltages)

            # Display the results
            result_text = "Spannungen an den Knoten:\n"
            for i, v in enumerate(voltages):
                result_text += f"Knoten {i}: {v:.2f} V\n"
            messagebox.showinfo("Ergebnis", result_text)

        except ValueError as e:
            messagebox.showerror("Eingabefehler", f"Fehler: {str(e)}. Bitte alle Felder korrekt ausfüllen.")
        except np.linalg.LinAlgError:
            messagebox.showerror("Berechnungsfehler",
                                 "Das Gleichungssystem konnte nicht gelöst werden. Stellen Sie sicher, dass das System richtig verbunden ist.")

    def display_matrix(self, G, B, voltages):
        """Display the system matrix, right-hand side, and solution in the text area."""
        self.matrix_display.delete(1.0, tk.END)
        num_nodes = len(G)
        matrix_str = "System-Matrix (G):\n"
        for i in range(num_nodes):
            matrix_str += ' '.join([f"{G[i, j]:.3f}" for j in range(num_nodes)]) + '\n'
        matrix_str += "\nRechte Seite (B):\n"
        matrix_str += ' '.join([f"{B[i]:.3f}" for i in range(num_nodes)]) + '\n'
        matrix_str += "\nLösung (Spannungen an den Knoten):\n"
        for i, v in enumerate(voltages):
            matrix_str += f"Knoten {i}: {v:.3f} V\n"
        self.matrix_display.insert(tk.END, matrix_str)


if __name__ == "__main__":
    root = tk.Tk()
    app = CircuitSimulator(root)
    root.mainloop()
