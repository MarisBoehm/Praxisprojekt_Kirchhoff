import tkinter as tk
from tkinter import messagebox
import numpy as np
import math




def draw_rotated_rectangle(canvas, x1, y1, x2, y2, width, height):
    # Mittelpunkt zwischen den Knoten
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    # Berechne den Winkel der Linie zwischen den Knoten (in Bogenmaß)
    angle = math.atan2(y2 - y1, x2 - x1)

    # Berechne die vier Ecken des Rechtecks
    half_width = width / 2
    half_height = height / 2

    # Berechne die Ecken des Rechtecks relativ zum Mittelpunkt
    corners = [
        (-half_width, -half_height),
        (half_width, -half_height),
        (half_width, half_height),
        (-half_width, half_height)
    ]

    # Drehe die Ecken basierend auf dem Winkel
    rotated_corners = []
    for corner in corners:
        rotated_x = corner[0] * math.cos(angle) - corner[1] * math.sin(angle)
        rotated_y = corner[0] * math.sin(angle) + corner[1] * math.cos(angle)
        rotated_corners.append((mid_x + rotated_x, mid_y + rotated_y))

    # Zeichne das Rechteck durch Verbinden der Ecken
    canvas.create_polygon(rotated_corners[0][0], rotated_corners[0][1],
                          rotated_corners[1][0], rotated_corners[1][1],
                          rotated_corners[2][0], rotated_corners[2][1],
                          rotated_corners[3][0], rotated_corners[3][1],
                          outline="blue", fill="", width=3)
    return rotated_corners

# Funktion zur Berechnung der Systemmatrix und Knotenspannungen für Schaltung 1
def calculate_matrix_schaltung1():
    try:
        # Eingabewerte für Widerstände und Spannungsquelle auslesen und leerzeichen entfernen
        R1 = float(entry_r1.get().strip())
        R2 = float(entry_r2.get().strip())
        R3 = float(entry_r3.get().strip())
        voltage = float(entry_voltage.get().strip())

        # Prüfen, ob alle Werte eingegeben wurden
        if R1 is None or R2 is None or R3 is None or voltage is None:
            raise ValueError("Fehlende Eingabe")

        # Erstellen der Leitwerte (Kehrwert der Widerstände)
        G1 = 1 / R1
        G2 = 1 / R2
        G3 = 1 / R3

        # Aufbau der Systemmatrix für Schaltung 1
        matrix = np.array([
            [G1, -G1, 0, 0, 0, 0],
            [-G1, G1 + G3, -G3, 0, 0, 0],
            [0, -G3, G3 + G2, -G2, 0, 0],
            [0, 0, -G2, G2, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])

        # Spannungsquelle setzt die Spannung zwischen Knoten 1 und 6
        isq = np.array([0, 0, 0, 0, -voltage, voltage])

        # Berechne die Knotenpotentiale
        potentials = np.linalg.solve(matrix, isq)

        # Darstellung der Matrix im Textfeld
        matrix_str = "System-Matrix | rechte Seite\n"
        for row in matrix:
            matrix_str += "  ".join(f"{val: .4f}" for val in row) + "\n"

        matrix_display.config(state=tk.NORMAL)
        matrix_display.delete(1.0, tk.END)
        matrix_display.insert(tk.END, matrix_str)
        matrix_display.config(state=tk.DISABLED)

        # Darstellung der Ergebnisse der Knotenspannungen
        results_str = "\nErgebnisse der Knotenspannungen:\n"
        for i, phi in enumerate(potentials, start=1):
            results_str += f"Knoten {i}: φ{i} = {phi:.4f} V\n"

        matrix_display.config(state=tk.NORMAL)
        matrix_display.insert(tk.END, results_str)
        matrix_display.config(state=tk.DISABLED)

    except np.linalg.LinAlgError:
        messagebox.showerror("Fehler", "Matrix ist singulär und kann nicht gelöst werden.")
    except ValueError as e:
        messagebox.showerror("Fehler", f"Bitte geben Sie gültige Zahlen ein. Fehler: {str(e)}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")


# Funktion zum Zeichnen der Schaltung 1 auf dem Canvas
def draw_circuit_schaltung1(canvas):

    # Canvas zurücksetzen
    canvas.delete("all")
    entry_r5.pack_forget()
    entry_r4.pack_forget()

    # Knoten zeichnen (gelbe Punkte)
    canvas.create_oval(45, 45, 55, 55, fill="yellow")  # Knoten 1
    canvas.create_oval(45, 245, 55, 255, fill="yellow")  # Knoten 2
    canvas.create_oval(195, 45, 205, 55, fill="yellow")  # Knoten 3
    canvas.create_oval(195, 245, 205, 255, fill="yellow")  # Knoten 4
    canvas.create_oval(345, 45, 355, 55, fill="yellow")  # Knoten 5
    canvas.create_oval(345, 245, 355, 255, fill="yellow")  # Knoten 6

    # Knotenbeschriftungen
    canvas.create_text(75, 45, text="1", fill="yellow")
    canvas.create_text(75, 255, text="2", fill="yellow")
    canvas.create_text(215, 45, text="3", fill="yellow")
    canvas.create_text(215, 255, text="4", fill="yellow")
    canvas.create_text(365, 45, text="5", fill="yellow")
    canvas.create_text(365, 255, text="6", fill="yellow")

    # Spannungsquelle (rote Linien, Minus oben und Plus unten)
    canvas.create_line(50, 50, 50, 250, fill="red", width=3)
    canvas.create_line(50, 80, 60, 80, fill="red", width=3)
    canvas.create_line(50, 220, 60, 220, fill="red", width=3)
    canvas.create_text(35, 70, text="(-)", fill="red")
    canvas.create_text(35, 230, text="(+)", fill="red")

    # Verbindungslinien (blau)
    canvas.create_line(55, 50, 120, 50, fill="blue", width=3)
    canvas.create_line(180, 50, 200, 50, fill="blue", width=3)
    canvas.create_line(55, 250, 200, 250, fill="blue", width=3)
    canvas.create_line(205, 250, 350, 250, fill="blue", width=3)
    canvas.create_line(350, 50, 350, 250, fill="blue", width=3)
    canvas.create_line(200, 55, 200, 140, fill="blue", width=3)
    canvas.create_line(200, 200, 200, 245, fill="blue", width=3)
    canvas.create_line(205, 50, 270, 50, fill="blue", width=3)
    canvas.create_line(330, 50, 345, 50, fill="blue", width=3)

    # Widerstände als Rechtecke
    canvas.create_rectangle(120, 40, 180, 60, outline="blue", width=3)
    canvas.create_rectangle(270, 40, 330, 60, outline="blue", width=3)
    canvas.create_rectangle(190, 140, 210, 200, outline="blue", width=3)

    # Text für Widerstände
    canvas.create_text(150, 30, text=f"R1 = {entry_r1.get()} Ohm", fill="blue")
    canvas.create_text(300, 30, text=f"R2 = {entry_r2.get()} Ohm", fill="blue")
    canvas.create_text(230, 170, text=f"R3 = {entry_r3.get()} Ohm", fill="blue")


# Funktion zum Zeichnen der Schaltung 2 auf dem Canvas (angepasst nach deinem Bild)
def draw_circuit_schaltung2(canvas):
    # Canvas zurücksetzen und das Zeichenfeld vergrößern
    shift_x=-75
    shift_y=-130
    canvas.delete("all")
    ohm4.pack()
    ohm5.pack()
    entry_r5.pack()
    entry_r4.pack()

    # Knoten zeichnen (gelbe Punkte)

    canvas.create_oval(275+shift_x, 150+shift_y, 285+shift_x, 160+shift_y, fill="yellow")  # Knoten 4
    canvas.create_oval(275+shift_x, 350+shift_y, 285+shift_x, 360+shift_y, fill="yellow")  # Knoten 3
    canvas.create_oval(400+shift_x, 250+shift_y, 410+shift_x, 260+shift_y, fill="yellow")  # Knoten 5
    canvas.create_oval(400+shift_x, 400+shift_y, 410+shift_x, 410+shift_y, fill="yellow")  # Knoten 6
    canvas.create_oval(150+shift_x, 250+shift_y, 160+shift_x, 260+shift_y, fill="yellow")  # Knoten 2
    canvas.create_oval(150+shift_x, 400+shift_y, 160+shift_x, 410+shift_y, fill="yellow")  # Knoten 1


    # Knotenbeschriftungen

    canvas.create_text(280 + shift_x, 140 + shift_y, text="4", fill="yellow")  # Knoten 4
    canvas.create_text(280 + shift_x, 370 + shift_y, text="3", fill="yellow")  # Knoten 3
    canvas.create_text(415 + shift_x, 245 + shift_y, text="5", fill="yellow")  # Knoten 5
    canvas.create_text(415 + shift_x, 415 + shift_y, text="6", fill="yellow")  # Knoten 6
    canvas.create_text(135 + shift_x, 245 + shift_y, text="2", fill="yellow")  # Knoten 2
    canvas.create_text(135 + shift_x, 415 + shift_y, text="1", fill="yellow")  # Knoten 1



    # Widerstände als Rechtecke

    rect_3_4 = draw_rotated_rectangle(canvas, 280 + shift_x, 350 + shift_y, 280 + shift_x, 150 + shift_y, 60,20)  # Knoten 3 und 4
    rect_2_3 = draw_rotated_rectangle(canvas, 150 + shift_x, 250 + shift_y, 275 + shift_x, 350 + shift_y, 60,20)  # Knoten 2 und 3
    rect_2_4 = draw_rotated_rectangle(canvas, 150 + shift_x, 250 + shift_y, 275 + shift_x, 150 + shift_y, 60,20)  # Knoten 2 und 4
    rect_4_5 = draw_rotated_rectangle(canvas, 275 + shift_x, 150 + shift_y, 400 + shift_x, 250 + shift_y, 60,20)  # Knoten 4 und 5
    rect_3_5 = draw_rotated_rectangle(canvas, 285 + shift_x, 354 + shift_y, 410 + shift_x, 253 + shift_y, 60,20)  # Knoten 5 und 3

    #linien zeichnen
    canvas.create_line(280+shift_x,159+shift_y,280+shift_x,222+shift_y,fill="blue",width=3)
    canvas.create_line(280 + shift_x, 280 + shift_y, 280 + shift_x, 350 + shift_y, fill="blue", width=3)#knoten 4 zu 3

    canvas.create_line(284 + shift_x, 355 + shift_y, 323 + shift_x, 323 + shift_y, fill="blue", width=3)#knoten 5
    canvas.create_line(402 + shift_x, 257 + shift_y,370 + shift_x, 285 + shift_y, fill="blue", width=3)#zu knoten 3

    canvas.create_line(402 + shift_x, 253 + shift_y, 362 + shift_x, 219 + shift_y, fill="blue", width=3)#knoten 5
    canvas.create_line(283 + shift_x, 157 + shift_y, 315 + shift_x,  182 + shift_y, fill="blue", width=3)#knoten 4

    canvas.create_line(277 + shift_x, 153 + shift_y, 235 + shift_x, 180 + shift_y, fill="blue", width=3)#knoten 4 zu
    canvas.create_line(157 + shift_x, 253 + shift_y, 192 + shift_x, 220 + shift_y, fill="blue", width=3)#knoten 2

    canvas.create_line(157 + shift_x, 257 + shift_y, 190 + shift_x, 284 + shift_y, fill="blue", width=3)#knoten 2
    canvas.create_line(277 + shift_x, 353 + shift_y, 235 + shift_x, 320 + shift_y, fill="blue", width=3)#knoten 3

    canvas.create_line(155 + shift_x, 260 + shift_y, 155 + shift_x, 400 + shift_y, fill="blue", width=3)#knoten 1 zu 2

    canvas.create_line(405 + shift_x, 400 + shift_y, 405 + shift_x, 260 + shift_y, fill="blue", width=3)#knoten 6 zu 5

    canvas.create_line(160 + shift_x, 405 + shift_y, 400 + shift_x, 405 + shift_y, fill="red", width=3)#knoten 1 zu 2

    canvas.create_line(360 + shift_x, 395 + shift_y,360 + shift_x, 405 + shift_y, fill="red", width=3)#pluspol
    canvas.create_line(205 + shift_x, 395 + shift_y, 205 + shift_x, 405 + shift_y, fill="red", width=3)# minuspol

    canvas.create_text(195+shift_x, 413+shift_y, text="(-)", fill="red")
    canvas.create_text(370+shift_x, 413+shift_y, text="(+)", fill="red")

    # Text für Widerstände
    canvas.create_text(240 + shift_x, 250 + shift_y, text=f"R1 = {entry_r1.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 2 und 3
    canvas.create_text(240 + shift_x, 160 + shift_y, text=f"R2 = {entry_r2.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 2 und 4
    canvas.create_text(320 + shift_x, 190 + shift_y, text=f"R3 = {entry_r3.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 4 und 5
    canvas.create_text(320 + shift_x, 300 + shift_y, text=f"R4 = {entry_r4.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 5 und 3
    canvas.create_text(280 + shift_x, 280 + shift_y, text=f"R5 = {entry_r5.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 3 und 4


# Hauptfenster und die restliche Logik bleibt unverändert
root = tk.Tk()
root.title("Schaltungssimulation mit visueller Darstellung und Matrixberechnung")

# Canvas für die Schaltung (größerer Canvas)
canvas = tk.Canvas(root, width=400, height=300, bg="gray")
canvas.pack()

# Button zum Zeichnen der Schaltungen
btn_draw_s1 = tk.Button(root, text="Schaltung 1 zeichnen", command=lambda: draw_circuit_schaltung1(canvas))
btn_draw_s1.pack()

btn_draw_s2 = tk.Button(root, text="Schaltung 2 zeichnen", command=lambda: draw_circuit_schaltung2(canvas))
btn_draw_s2.pack()

# Eingabefelder für Widerstände und Spannungsquellen
tk.Label(root, text="R1 (Ohm):").pack()
entry_r1 = tk.Entry(root)
entry_r1.pack()

tk.Label(root, text="R2 (Ohm):").pack()
entry_r2 = tk.Entry(root)
entry_r2.pack()

tk.Label(root, text="R3 (Ohm):").pack()
entry_r3 = tk.Entry(root)
entry_r3.pack()

ohm4=tk.Label(root, text="R4 (Ohm):")
entry_r4 = tk.Entry(root)


ohm5=tk.Label(root, text="R5 (Ohm):")
entry_r5 = tk.Entry(root)


tk.Label(root, text="Spannungsquelle (V):").pack()
entry_voltage = tk.Entry(root)
entry_voltage.pack()

# Button zum Berechnen der Matrix für Schaltung 1
btn_calculate = tk.Button(root, text="Berechnen", command=calculate_matrix_schaltung1)
btn_calculate.pack()

# Textfeld zur Anzeige der Matrix
matrix_display = tk.Text(root, height=15, width=80)
matrix_display.pack()

# Starte das Hauptfenster
root.mainloop()
