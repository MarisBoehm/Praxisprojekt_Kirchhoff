import tkinter as tk
from tkinter import messagebox
import numpy as np
import math

current_circuit = None

def set_current_circuit(circuit_number):
    global current_circuit
    current_circuit = circuit_number

def berechnen():
    global current_circuit
    if current_circuit == 1:
        display_matrix_schaltung1()
        draw_circuit_schaltung1(canvas)
    elif current_circuit == 2:
        display_matrix_schaltung2()
        draw_circuit_schaltung2(canvas)
    elif current_circuit == 3:
        display_matrix_schaltung3()
        draw_circuit_schaltung3(canvas)
    elif current_circuit == 4:
        display_matrix_schaltung4()
        draw_circuit_schaltung4(canvas)
    else:
        messagebox.showerror("Fehler", "Keine Schaltung ausgewählt!")

def berechne_knotenpotenziale(I1, I2, R1, R2, R3, V1):
    # Setze Knoten 1 als Referenzknoten mit Potenzial 0
    V1 = 0

    # Berechne Knotenpotenzial V2
    V2 = V1 + I1 * R1

    # Berechne Knotenpotenzial V3 entweder über R2 oder R3
    V3_via_R2 = V2 + I2 * R2
    V3_via_R3 = V1 + I1 * R3  # Alternativ über R3

    return V1, V2, V3_via_R2, V3_via_R3

def draw_rect_between(canvas, x1, y1, x2, y2, rect_width, rect_height):
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    # Berechne den Winkel, um das Rechteck entlang der Knoten zu zeichnen
    angle = math.atan2(y2 - y1,
                       x2 - x1) + math.pi / 2  # + pi/2 dreht es um 90 Grad, sodass die kurze Seite zum Knoten zeigt

    half_width = rect_width / 2
    half_height = rect_height / 2

    # Ecken des Rechtecks relativ zum Mittelpunkt
    corners = [
        (-half_width, -half_height),
        (half_width, -half_height),
        (half_width, half_height),
        (-half_width, half_height)
    ]

    rotated_corners = []
    for corner in corners:
        rotated_x = corner[0] * math.cos(angle) - corner[1] * math.sin(angle)
        rotated_y = corner[0] * math.sin(angle) + corner[1] * math.cos(angle)
        rotated_corners.append((mid_x + rotated_x, mid_y + rotated_y))

    # Zeichne das Rechteck
    canvas.create_polygon(rotated_corners[0][0], rotated_corners[0][1],
                          rotated_corners[1][0], rotated_corners[1][1],
                          rotated_corners[2][0], rotated_corners[2][1],
                          rotated_corners[3][0], rotated_corners[3][1],
                          outline="blue", fill="", width=3)


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
def display_matrix_schaltung1():
    try:
        # Werte aus den Eingabefeldern holen und in float umwandeln
        R1 = float(entry_r1.get().strip())
        R2 = float(entry_r2.get().strip())
        R3 = float(entry_r3.get().strip())
        V1 = float(entry_voltage1.get().strip())

        # Koeffizientenmatrix A
        A = np.array([[R1 + R2, -R2],
                      [-R2, R2 + R3]])

        # Rechte Seite b
        b = np.array([V1, 0])

        # Lösung des Gleichungssystems A * x = b
        x = np.linalg.solve(A, b)

        IR1=x[0]
        IR3=x[1]
        IR2=IR1-IR3

        # Formatierte Darstellung mit festen Spaltenbreiten
        matrix_str = (
            "Matrix-Gleichung des Maschenstromverfahrens:\n\n"
            f"[{R1 :<8.2f} + {R2:<8.2f}, {-R2:<8.2f}]  * [I1]   =   [{V1:<5.2f}]\n"
            f"[{-R2:<8.2f}, {R2:<8.2f} + {R3:<8.2f}]    [I2]       [0]\n\n"
            
            "Maschenströme:\n"
            f"I1={x[0]:.3f} A\n"
            f"I2={x[1]:.3f} A\n\n"
            
            f"Knotenpotenziale:{'':<16.2} Ströme durch die Widerstände:\n"
            f"K1=0 V          {'':16.2} IR1={IR1:<8.3f} A\n"
            f"K2={V1:<5.3f} V      {'':<16.2}IR2={IR2:<8.3f} A\n"
            f"K3={V1-(R3*x[1]):<5.3f} V       {'':<16.2}IR3={IR3:<8.3f} A\n"
            f"K4={V1:<5.3f} V\n"
            f"K5={V1:<5.3f} V\n"
            f"K6={V1:<5.3f} V\n"
        )






        matrix_display.config(state=tk.NORMAL)
        matrix_display.delete(1.0, tk.END)
        matrix_display.insert(tk.END, matrix_str)
        matrix_display.config(state=tk.DISABLED)



    except np.linalg.LinAlgError:
        messagebox.showerror("Fehler", "Matrix ist singulär und kann nicht gelöst werden.")
    except ValueError as e:
        messagebox.showerror("Fehler", f"Bitte geben Sie gültige Zahlen ein.{str(e)}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")

def display_matrix_schaltung4():
    try:
        # Werte aus den Eingabefeldern holen und in float umwandeln
        R1 = float(entry_r1.get().strip())
        R2 = float(entry_r2.get().strip())
        R3 = float(entry_r3.get().strip())
        V1 = float(entry_voltage1.get().strip())
        V2 = float(entry_voltage2.get().strip())

        # Koeffizientenmatrix A
        A = np.array([[R1 + R2, R2],
                      [R2, R2 + R3]])

        # Rechte Seite b
        b = np.array([V1, V2])

        # Lösung des Gleichungssystems A * x = b
        x = np.linalg.solve(A, b)
        # Formatierte Darstellung mit festen Spaltenbreiten
        IM1=x[0]
        IM2=x[1]
        IR1=IM1
        IR2=IM1+IM2
        IR3=IM2
        VR3=R3*x[1]
        matrix_str = (
            "Matrix-Gleichung des Maschenstromverfahrens:\n\n"
            f"[{R1 :<8.2f} + {R2:<8.2f}, {R2:<8.2f}]  * [I1]   =   [{V1:<5.2f}]\n"
            f"[{R2:<8.2f}, {R2:<8.2f} + {R3:<8.2f}]    [I2]       [{V2:<5.2f}]\n\n"

            "Maschenströme:\n"
            f"I1={x[0]:.3f} A\n"
            f"I2={x[1]:.3f} A\n\n"

            f"Knotenpotenziale:{'':<16.2} Ströme durch die Widerstände:\n"
            f"K1=0 V           {'':16.2} IR1={IR1:<8.3f} A\n"
            f"K1={VR3:<5.3f} V       {'':16.2} IR2={IR2:<8.3f} A\n"
            f"K2={VR3:<5.3f} V       {'':16.2} IR3={IR3:<8.3f} A\n"
            f"K3=0 V\n"
            f"K4={V1+VR3:<5.3f} V\n"
            f"K5={V2:<5.3f} V\n"
            f"K6={V2:<5.3f} V\n"
        )


        # Darstellung der Matrix im Textfeld


        matrix_display.config(state=tk.NORMAL)
        matrix_display.delete(1.0, tk.END)
        matrix_display.insert(tk.END, matrix_str)
        matrix_display.config(state=tk.DISABLED)

    except ValueError as e:
        messagebox.showerror("Fehler", f"Bitte geben Sie gültige Zahlen ein")
def display_matrix_schaltung3():

        try:
            # Werte aus den Eingabefeldern holen und in float umwandeln
            R1 = float(entry_r1.get().strip())
            R2 = float(entry_r2.get().strip())
            R3 = float(entry_r3.get().strip())
            R4 = float(entry_r4.get().strip())
            R5 = float(entry_r5.get().strip())
            R6 = float(entry_r6.get().strip())
            V1 = float(entry_voltage1.get())

            # Koeffizientenmatrix A
            A = np.array([[R1+R2+R3, -R2,-R3],
                          [-R2, R2+R4+R5,-R4],
                          [-R3,-R4,R6+R3+R4]])

            print(A)
            # Rechte Seite b
            b = np.array([V1, 0,0])
            print(b)
            # Lösung des Gleichungssystems A * x = b
            x = np.linalg.solve(A, b)
            print(x)
            # Formatierte Darstellung mit festen Spaltenbreiten
            IM1=x[0]
            IM2=x[1]
            IM3=x[2]
            IR1=IM1
            IR2=IM1-IM2
            IR3=IM1-IM3
            IR4=IM2-IM3
            IR5=IM2
            IR6=IM3
            VR2=(x[0]-x[1])*R2
            K69=V1-(x[1]*R5)
            matrix_str = (
                "Matrix-Gleichung des Maschenstromverfahrens:\n\n"
                f"[{R1 :<8.2f} + {R2:<8.2f} + {R3:<8.2f}, {-R2:<8.2f},{-R3:<8.2f}]  * [I1]   =   [{V1:<5.2f}]\n"
                f"[{-R2:<8.2f}, {R2:<8.2f} + {R4:<8.2f} + {R5:<8.2f},{-R4:<8.2f}]    [I2]       [0]\n"
                f"[{-R3:<8.2f}, {-R4:<8.2f},{R6:<8.2f} + {R4:<8.2f} + {R3:<8.2f}]    [I3]       [0]\n\n"
                "Maschenströme:\n"
                f"I1={x[0]:.3f} A\n"
                f"I2={x[1]:.3f} A\n"
                f"I3={x[2]:.3f} A\n\n"

                f"Knotenpotenziale:{'':<16.2} Ströme durch die Widerstände:\n"
                f"K1=0 V          {'':16.2} IR1={IR1:<8.3f} A\n"
                f"K2={V1:<5.3f} V      {'':16.2} IR2={IR2:<8.3f} A\n"
                f"K3={V1:<5.3f} V      {'':16.2} IR3={IR3:<8.3f} A\n"
                f"K4={(x[0]*R1):<5.3f} V      {'':16.2} IR4={IR4:<8.3f} A\n"
                f"K5={V1-VR2:<5.3f} V      {'':16.2} IR5={IR5:<8.3f} A\n"
                f"K6={K69:<5.3f} V      {'':16.2} IR6={IR6:<8.3f} A\n"
                f"K7={V1 :<5.3f} V\n"
                f"K8={K69-(x[2]*R6):<5.3f} V\n"
                f"K9={K69:<5.3f} V\n"
            )

            # Darstellung der Matrix im Textfeld

            matrix_display.config(state=tk.NORMAL)
            matrix_display.delete(1.0, tk.END)
            matrix_display.insert(tk.END, matrix_str)
            matrix_display.config(state=tk.DISABLED)



        except np.linalg.LinAlgError:
            messagebox.showerror("Fehler", "Matrix ist singulär und kann nicht gelöst werden.")
        except ValueError as e:
            messagebox.showerror("Fehler", f"Bitte geben Sie gültige Zahlen ein.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")
def display_matrix_schaltung2():
    try:
        # Werte aus den Eingabefeldern holen und in float umwandeln
        R1 = float(entry_r1.get().strip())
        R2 = float(entry_r2.get().strip())
        R3 = float(entry_r3.get().strip())
        R4 = float(entry_r4.get().strip())
        R5 = float(entry_r5.get().strip())
        V1 = float(entry_voltage1.get())

        # Koeffizientenmatrix A
        A = np.array([[R1 + R4, -R4, -R1],
                      [-R4, R3 + R4 + R5, -R5],
                      [-R1, -R5,R2 + R1 + R5]])

        print(A)
        # Rechte Seite b
        b = np.array([V1, 0, 0])
        print(b)
        # Lösung des Gleichungssystems A * x = b
        x = np.linalg.solve(A, b)
        print(x)
        # Formatierte Darstellung mit festen Spaltenbreiten
        IM1=x[0]
        IM2=x[1]
        IM3=x[2]
        IR1=IM1-IM3
        IR2=IM3
        IR3=IM2
        IR4=IM1-IM2
        IR5=IM3-IM2
        VR1=IR1*R1
        matrix_str = (
            "Matrix-Gleichung des Maschenstromverfahrens:\n\n"
            f"[{R1 :<8.2f} + {R4:<16.4f}, {-R4:<8.2f},{-R5:<8.2f}]     * [I1]   =   [{V1:<5.2f}]\n"
            f"[{-R4:<8.2f}, {R3:<8.2f} + {R4:<8.2f} + {R5:<8.2f},{-R1:<8.2f}]    [I2]       [0]\n"
            f"[{-R5:<8.2f}, {-R1:<8.2f},{R5:<8.2f} + {R2:<8.2f} + {R1:<8.2f}]    [I3]       [0]\n\n"
            "Maschenströme:\n"
            f"I1={x[0]:.3f} A\n"
            f"I2={x[1]:.3f} A\n"
            f"I3={x[2]:.3f} A\n\n"

            f"Knotenpotenziale:{'':<16.2} Ströme durch die Widerstände:\n"
            f"K1=0 V          {'':16.2} IR1={IR1:<8.3f} A\n"
            f"K2=0 V          {'':16.2} IR2={IR2:<8.3f} A\n"
            f"K3={VR1:<5.3f} V      {'':16.2} IR3={IR3:<8.3f} A\n"
            f"K4={(x[2]*R2):<5.3f} V      {'':16.2} IR4={IR4:<8.3f} A\n"
            f"K5={V1:<5.3f} V     {'':16.2} IR5={IR5:<8.3f} A\n"
            f"K6={V1:<5.3f} V\n"

        )

        # Darstellung der Matrix im Textfeld

        matrix_display.config(state=tk.NORMAL)
        matrix_display.delete(1.0, tk.END)
        matrix_display.insert(tk.END, matrix_str)
        matrix_display.config(state=tk.DISABLED)



    except np.linalg.LinAlgError:
        messagebox.showerror("Fehler", "Matrix ist singulär und kann nicht gelöst werden.")
    except ValueError as e:
        messagebox.showerror("Fehler", f"Bitte geben Sie gültige Zahlen ein. Fehler: {str(e)}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")

# Funktion zum Zeichnen der Schaltung 1 auf dem Canvas
def draw_circuit_schaltung1(canvas):
    set_current_circuit(1)
    # Canvas zurücksetzen
    canvas.delete("all")
    entry_r2.place(x=135, y=380)
    entry_r1.place(x=24, y=380)
    entry_r3.place(x=244, y=380)


    ohm1.place(x=26, y=360)
    ohm2.place(x=137, y=360)
    ohm3.place(x=246, y=360)

    Spannungsquelle1.place(x=24, y=480)
    Spannungsquelle2.place_forget()
    entry_voltage1.place(x=24, y=500)
    entry_voltage2.place_forget()


    entry_r5.place_forget()
    entry_r4.place_forget()
    entry_r6.place_forget()
    ohm4.place_forget()
    ohm5.place_forget()
    ohm6.place_forget()

    # Knoten zeichnen (gelbe Punkte)
    canvas.create_oval(45, 45, 55, 55, fill="yellow")  # Knoten 1
    canvas.create_oval(45, 245, 55, 255, fill="yellow")  # Knoten 2
    canvas.create_oval(195, 45, 205, 55, fill="yellow")  # Knoten 3
    canvas.create_oval(195, 245, 205, 255, fill="yellow")  # Knoten 4
    canvas.create_oval(345, 45, 355, 55, fill="yellow")  # Knoten 5
    canvas.create_oval(345, 245, 355, 255, fill="yellow")  # Knoten 6

    # Knotenbeschriftungen
    canvas.create_text(68, 40, text="1", fill="yellow")
    canvas.create_text(70, 260, text="2", fill="yellow")
    canvas.create_text(215, 40, text="3", fill="yellow")
    canvas.create_text(215, 260, text="4", fill="yellow")
    canvas.create_text(365, 45, text="5", fill="yellow")
    canvas.create_text(365, 255, text="6", fill="yellow")

    # Spannungsquelle (rote Linien, Minus oben und Plus unten)
    canvas.create_line(50, 55, 50, 245, fill="red", width=3)
    canvas.create_line(50, 80, 60, 80, fill="red", width=3)
    canvas.create_line(50, 220, 60, 220, fill="red", width=3)
    canvas.create_text(35, 70, text="(-)", fill="red")
    canvas.create_text(35, 230, text="(+)", fill="red")

    # Verbindungslinien (blau)
    canvas.create_line(55, 50, 95, 50, fill="blue", width=3)  # knoten 1 zu
    canvas.create_line(155, 50, 195, 50, fill="blue", width=3)  # knoten 3

    canvas.create_line(205, 250, 345, 250, fill="blue", width=3)  # knoten 4 zu 6

    canvas.create_line(55, 250, 195, 250, fill="blue", width=3)  # knoten 2 zu 4

    canvas.create_line(205, 50, 245, 50, fill="blue", width=3)  # knoten 5 zu
    canvas.create_line(305, 50, 345, 50, fill="blue", width=3)  # knoten 3

    canvas.create_line(350, 55, 350, 245, fill="blue", width=3)  # 5zu6


    canvas.create_line(200, 55, 200, 120, fill="blue", width=3)  # knoten 3 zu
    canvas.create_line(200, 180, 200, 245, fill="blue", width=3)  # knoten 4

    canvas.create_line(200, 200, 200, 245, fill="blue", width=3)
    canvas.create_line(330, 50, 345, 50, fill="blue", width=3)

    height = 60
    width = 20

    draw_rect_between(canvas, 50, 50, 200, 50, width, height)  # zwiswchen 1und 3
    draw_rect_between(canvas, 200, 50, 200, 250, width, height)  # zwischen 3 und 4
    draw_rect_between(canvas, 200, 50, 345, 50, width, height)  # zwischen 3 und 5

    # Text für Widerstände
    canvas.create_text(130, 30, text=f"R1 = {entry_r1.get()} Ohm", fill="blue")
    canvas.create_text(270, 30, text=f"R2 = {entry_r2.get()} Ohm", fill="blue")
    canvas.create_text(260, 150, text=f"R3 = {entry_r3.get()} Ohm", fill="blue")
    canvas.create_text(80, 140, text=f"U1 = {entry_voltage1.get()} V", fill="red")  # Spannungen




# Funktion zum Zeichnen der Schaltung 2 auf dem Canvas (angepasst nach deinem Bild)
def draw_circuit_schaltung2(canvas):
    # Canvas zurücksetzen und das Zeichenfeld vergrößern
    shift_x=-75
    shift_y=-130
    canvas.delete("all")

    set_current_circuit(2)

    entry_r2.place(x=135, y=380)
    entry_r1.place(x=24, y=380)
    entry_r3.place(x=244, y=380)
    entry_r5.place(x=24, y=440)
    entry_r4.place(x=352, y=380)
    entry_r6.place_forget()

    Spannungsquelle1.place(x=24, y=480)
    Spannungsquelle2.place_forget()
    entry_voltage1.place(x=24, y=500)
    entry_voltage2.place_forget()


    ohm1.place(x=26, y=360)
    ohm2.place(x=137, y=360)
    ohm3.place(x=246, y=360)
    ohm4.place(x=354, y=360)
    ohm5.place(x=26, y=420)
    ohm6.place_forget()


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
    canvas.create_text(200 + shift_x, 350 + shift_y, text=f"R1 = {entry_r1.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 2 und 3
    canvas.create_text(170 + shift_x, 180 + shift_y, text=f"R2 = {entry_r2.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 2 und 4
    canvas.create_text(370 + shift_x, 180 + shift_y, text=f"R3 = {entry_r3.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 4 und 5
    canvas.create_text(370 + shift_x, 350 + shift_y, text=f"R4 = {entry_r4.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 5 und 3
    canvas.create_text(220 + shift_x, 250 + shift_y, text=f"R5 = {entry_r5.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 3 und 4

    canvas.create_text(270+shift_x, 390+shift_y, text=f"U1 = {entry_voltage1.get()} V", fill="red")  # Spannungen

def draw_circuit_schaltung3(canvas):
    set_current_circuit(3)
    canvas.delete("all")  # Zurücksetzen des Canvas

    shift_x = -30  # Horizontaler Versatz
    shift_y = -160 # Vertikaler Versatz

    entry_r2.place(x=135, y=380)
    entry_r1.place(x=24, y=380)
    entry_r3.place(x=244, y=380)
    entry_r5.place(x=24, y=440)
    entry_r4.place(x=352, y=380)
    entry_r6.place(x=135, y=440)

    ohm1.place(x=26, y=360)
    ohm2.place(x=137, y=360)
    ohm3.place(x=246, y=360)
    ohm4.place(x=354, y=360)
    ohm5.place(x=26, y=420)
    ohm6.place(x=137, y=420)

    Spannungsquelle1.place(x=24, y=480)
    Spannungsquelle2.place_forget()
    entry_voltage1.place(x=24, y=500)
    entry_voltage2.place_forget()


    # Knoten zeichnen (gelbe Punkte)
    canvas.create_oval(100 + shift_x, 400 + shift_y, 110 + shift_x, 410 + shift_y, fill="yellow")  # Knoten 1
    canvas.create_oval(200 + shift_x, 400 + shift_y, 210 + shift_x, 410 + shift_y, fill="yellow")  # Knoten 2
    canvas.create_oval(400 + shift_x, 400 + shift_y, 410 + shift_x, 410 + shift_y, fill="yellow")  # Knoten 3
    canvas.create_oval(100 + shift_x, 300 + shift_y, 110 + shift_x, 310 + shift_y, fill="yellow")  # Knoten 4
    canvas.create_oval(200 + shift_x, 300 + shift_y, 210 + shift_x, 310 + shift_y, fill="yellow")  # Knoten 5
    canvas.create_oval(300 + shift_x, 300 + shift_y, 310 + shift_x, 310 + shift_y, fill="yellow")  # Knoten 6
    canvas.create_oval(400 + shift_x, 300 + shift_y, 410 + shift_x, 310 + shift_y, fill="yellow")  # Knoten 7
    canvas.create_oval(100 + shift_x, 200 + shift_y, 110 + shift_x, 210 + shift_y, fill="yellow")  # Knoten 8
    canvas.create_oval(300 + shift_x, 200 + shift_y, 310 + shift_x, 210 + shift_y, fill="yellow")  # Knoten 9

    # Knotenbeschriftungen
    canvas.create_text(90 + shift_x, 405 + shift_y, text="1", fill="yellow")
    canvas.create_text(220 + shift_x, 415 + shift_y, text="2", fill="yellow")
    canvas.create_text(390 + shift_x, 415 + shift_y, text="3", fill="yellow")
    canvas.create_text(90 + shift_x, 305 + shift_y, text="4", fill="yellow")
    canvas.create_text(190 + shift_x, 315 + shift_y, text="5", fill="yellow")
    canvas.create_text(290 + shift_x, 315 + shift_y, text="6", fill="yellow")
    canvas.create_text(390 + shift_x, 300 + shift_y, text="7", fill="yellow")
    canvas.create_text(90 + shift_x, 200 + shift_y, text="8", fill="yellow")
    canvas.create_text(290 + shift_x, 195 + shift_y, text="9", fill="yellow")

    # Funktion zum Zeichnen eines Rechtecks zwischen zwei Knoten (diesmal so gedreht, dass die kurze Seite auf die Knoten zeigt)


    # Zeichne Rechtecke zwischen den Knoten
    rect_width = 15
    rect_height = 40  # Doppelt so lang wie breit

    # Rechtecke zeichnen
    draw_rect_between(canvas, 100 + shift_x, 205 + shift_y, 300 + shift_x, 205 + shift_y, rect_width,
                      rect_height)  # Knoten 8 und 9
    draw_rect_between(canvas, 200 + shift_x, 305 + shift_y, 300 + shift_x, 305 + shift_y, rect_width,
                      rect_height)  # Knoten 5 und 6
    draw_rect_between(canvas, 300 + shift_x, 305 + shift_y, 400 + shift_x, 305 + shift_y, rect_width,
                      rect_height)  # Knoten 6 und 7
    draw_rect_between(canvas, 205 + shift_x, 400 + shift_y, 205 + shift_x, 300 + shift_y, rect_width,
                      rect_height)  # Knoten 5 und 2
    draw_rect_between(canvas, 105 + shift_x, 400 + shift_y, 105 + shift_x, 300 + shift_y, rect_width,
                      rect_height)  # Knoten 4 und 1
    draw_rect_between(canvas, 100 + shift_x, 305 + shift_y, 200 + shift_x, 305 + shift_y, rect_width,
                      rect_height)  # Knoten 4 und 5

    canvas.create_line(210 + shift_x, 405 + shift_y, 400 + shift_x, 405 + shift_y, fill="blue",width=3)  # Knoten 2 und 3
    canvas.create_line(405 + shift_x, 400 + shift_y, 405 + shift_x, 310 + shift_y, fill="blue", width=3)  # Knoten 3 und 7

    canvas.create_line(400 + shift_x, 305 + shift_y, 370 + shift_x, 305 + shift_y, fill="blue", width=3)  # Knoten 7 zu
    canvas.create_line(330 + shift_x, 305 + shift_y, 310 + shift_x, 305 + shift_y, fill="blue", width=3)  # knoten 6

    canvas.create_line(305 + shift_x, 300 + shift_y, 305 + shift_x, 210 + shift_y, fill="blue", width=3)  # Knoten 6 zu 9

    canvas.create_line(300 + shift_x, 205 + shift_y, 220 + shift_x, 205 + shift_y, fill="blue", width=3)  # Knoten 9 zu
    canvas.create_line(180 + shift_x, 205 + shift_y, 110 + shift_x, 205 + shift_y, fill="blue", width=3)  # Knoten  8

    canvas.create_line(105 + shift_x, 210 + shift_y, 105 + shift_x, 300 + shift_y, fill="blue", width=3)  # Knoten 8 zu 4

    canvas.create_line(105 + shift_x, 310 + shift_y, 105 + shift_x, 330 + shift_y, fill="blue", width=3)  # knoten 4 zu
    canvas.create_line(105 + shift_x, 370 + shift_y, 105 + shift_x, 400 + shift_y, fill="blue", width=3)  # knoten 1

    canvas.create_line(110 + shift_x, 305 + shift_y, 130 + shift_x, 305 + shift_y, fill="blue", width=3)  # knoten 4 zu
    canvas.create_line(170 + shift_x, 305 + shift_y, 200 + shift_x, 305 + shift_y, fill="blue", width=3)  # knoten 5

    canvas.create_line(205 + shift_x, 310 + shift_y, 205 + shift_x, 330 + shift_y, fill="blue", width=3)  # knoten 5 zu
    canvas.create_line(205 + shift_x, 370 + shift_y, 205 + shift_x, 400 + shift_y, fill="blue", width=3)  # knoten 2

    canvas.create_line(210 + shift_x, 305 + shift_y, 230 + shift_x, 305 + shift_y, fill="blue", width=3)  # knoten 5 zu
    canvas.create_line(270 + shift_x, 305 + shift_y, 300 + shift_x, 305 + shift_y, fill="blue", width=3)  # knoten 6

    canvas.create_line(110 + shift_x, 405 + shift_y, 200 + shift_x, 405 + shift_y, fill="red", width=3)  # spannungsline
    canvas.create_line(130 + shift_x, 405 + shift_y, 130 + shift_x, 395 + shift_y, fill="red", width=3)  # pluspol
    canvas.create_line(180 + shift_x, 405 + shift_y, 180 + shift_x, 395 + shift_y, fill="red", width=3)  # minuspol

    canvas.create_text(130 + shift_x, 413 + shift_y, text="(-)", fill="red")
    canvas.create_text(180 + shift_x, 413 + shift_y, text="(+)", fill="red")

    canvas.create_text(155 + shift_x, 355 + shift_y, text=f"R1 = {entry_r1.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 1 und 4
    canvas.create_text(255 + shift_x, 355 + shift_y, text=f"R2 = {entry_r2.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 2 und 5
    canvas.create_text(155 + shift_x, 285 + shift_y, text=f"R3 = {entry_r3.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 4 und 5
    canvas.create_text(240 + shift_x, 285 + shift_y, text=f"R4 = {entry_r4.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 5 und 6
    canvas.create_text(360 + shift_x, 285 + shift_y, text=f"R5 = {entry_r5.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 6 und 7
    canvas.create_text(195 + shift_x, 225 + shift_y, text=f"R6 = {entry_r6.get()} Ohm",
                       fill="blue")  # Widerstand zwischen 8 und 9

    canvas.create_text(140+shift_x, 435+shift_y, text=f"U1 = {entry_voltage1.get()} V", fill="red")  # Spannungen


def draw_circuit_schaltung4(canvas):
    # Canvas zurücksetzen
    set_current_circuit(4)
    canvas.delete("all")
    entry_r2.place(x=135, y=380)
    entry_r1.place(x=24, y=380)
    entry_r3.place(x=244, y=380)

    ohm1.place(x=26, y=360)
    ohm2.place(x=137, y=360)
    ohm3.place(x=246, y=360)

    Spannungsquelle1.place(x=24, y=480)
    Spannungsquelle2.place(x=246, y=480)
    entry_voltage1.place(x=24, y=500)
    entry_voltage2.place(x=246, y=500)


    entry_r5.place_forget()
    entry_r4.place_forget()
    entry_r6.place_forget()
    ohm4.place_forget()
    ohm5.place_forget()
    ohm6.place_forget()

    # Knoten zeichnen (gelbe Punkte)
    canvas.create_oval(45, 45, 55, 55, fill="yellow")  # Knoten 1
    canvas.create_oval(45, 245, 55, 255, fill="yellow")  # Knoten 2
    canvas.create_oval(195, 45, 205, 55, fill="yellow")  # Knoten 3
    canvas.create_oval(195, 245, 205, 255, fill="yellow")  # Knoten 4
    canvas.create_oval(345, 45, 355, 55, fill="yellow")  # Knoten 5
    canvas.create_oval(345, 245, 355, 255, fill="yellow")  # Knoten 6

    # Knotenbeschriftungen
    canvas.create_text(68, 40, text="1", fill="yellow")
    canvas.create_text(70, 260, text="2", fill="yellow")
    canvas.create_text(215, 40, text="3", fill="yellow")
    canvas.create_text(215, 260, text="4", fill="yellow")
    canvas.create_text(365, 45, text="5", fill="yellow")
    canvas.create_text(365, 255, text="6", fill="yellow")

    # Spannungsquelle (rote Linien, Minus oben und Plus unten)
    canvas.create_line(50, 55, 50, 245, fill="red", width=3)
    canvas.create_line(50, 80, 60, 80, fill="red", width=3)
    canvas.create_line(50, 220, 60, 220, fill="red", width=3)
    canvas.create_text(35, 70, text="(+)", fill="red")
    canvas.create_text(35, 230, text="(-)", fill="red")

    # Verbindungslinien (blau)
    canvas.create_line(55, 50, 95, 50, fill="blue", width=3)#knoten 1 zu
    canvas.create_line(155, 50, 195, 50, fill="blue", width=3)#knoten 3

    canvas.create_line(205, 50, 345, 50, fill="blue", width=3)#knoten 3 zu 5

    canvas.create_line(55, 250, 195, 250, fill="blue", width=3)#knoten 2 zu 4

    canvas.create_line(205, 250, 245, 250, fill="blue", width=3)#knoten 4 zu
    canvas.create_line(305, 250, 345, 250, fill="blue", width=3)#knoten 6

    canvas.create_line(350, 55, 350, 245, fill="red", width=3)#spannungsline
    canvas.create_line(350, 80, 340, 80, fill="red", width=3)
    canvas.create_line(350, 220, 340, 220, fill="red", width=3)
    canvas.create_text(365, 70, text="(+)", fill="red")
    canvas.create_text(365, 230, text="(-)", fill="red")

    canvas.create_line(200, 55, 200, 120, fill="blue", width=3)#knoten 3 zu
    canvas.create_line(200, 180, 200, 245, fill="blue", width=3)#knoten 4

    canvas.create_line(200, 200, 200, 245, fill="blue", width=3)
    canvas.create_line(205, 50, 270, 50, fill="blue", width=3)
    canvas.create_line(330, 50, 345, 50, fill="blue", width=3)

    height = 60
    width = 20

    draw_rect_between(canvas,50,50,200,50,width,height)#zwiswchen 1und 3
    draw_rect_between(canvas,200,50,200,250,width,height)#zwischen 3 und 4
    draw_rect_between(canvas,200,250,350,250,width,height)#zwischen 4 und 6

    # Text für Widerstände
    canvas.create_text(120, 30, text=f"R1 = {entry_r1.get()} Ohm", fill="blue")
    canvas.create_text(255, 150, text=f"R2 = {entry_r2.get()} Ohm", fill="blue")
    canvas.create_text(275, 225, text=f"R3 = {entry_r3.get()} Ohm", fill="blue")

    canvas.create_text(90,150, text=f"U1 = {entry_voltage1.get()} V", fill="red")#Spannungen
    canvas.create_text(300, 80, text=f"U2 = {entry_voltage2.get()} V", fill="red")






# Hauptfenster und die restliche Logik bleibt unverändert
root = tk.Tk()
root.title("Schaltungssimulation mit visueller Darstellung und Matrixberechnung")
root.geometry("1070x550")

# Canvas für die Schaltung (größerer Canvas)
canvas = tk.Canvas(root, width=400, height=300, bg="gray")
canvas.place(x=24,y=0)

# Button zum Zeichnen der Schaltungen
btn_draw_s1 = tk.Button(root, text="Schaltung 1", command=lambda: draw_circuit_schaltung1(canvas))
btn_draw_s1.place(x=24, y=305)

btn_draw_s2 = tk.Button(root, text="Schaltung 2", command=lambda: draw_circuit_schaltung2(canvas))
btn_draw_s2.place(x=135, y=305)

btn_draw_s3=tk.Button(root, text="Schaltung 3", command=lambda: draw_circuit_schaltung3(canvas))
btn_draw_s3.place(x=244, y=305)

btn_draw_s4=tk.Button(root, text="Schaltung 4", command=lambda: draw_circuit_schaltung4(canvas))
btn_draw_s4.place(x=352, y=305)


# Eingabefelder für Widerstände und Spannungsquellen
ohm1=tk.Label(root, text="R1 (Ohm):")
entry_r1 = tk.Entry(root,width=11)


ohm2=tk.Label(root, text="R2 (Ohm):")
entry_r2 = tk.Entry(root,width=11)


ohm3=tk.Label(root, text="R3 (Ohm):")
entry_r3 = tk.Entry(root,width=11)




ohm4=tk.Label(root, text="R4 (Ohm):")
entry_r4 = tk.Entry(root,width=11)




ohm5=tk.Label(root, text="R5 (Ohm):")
entry_r5 = tk.Entry(root,width=11)

ohm6=tk.Label(root, text="R6 (Ohm):")
entry_r6 = tk.Entry(root,width=11)






Spannungsquelle1=tk.Label(root, text="Spannungsquelle 1 (V):")
entry_voltage1 = tk.Entry(root)

Spannungsquelle2=tk.Label(root, text="Spannungsquelle 2 (V):")
entry_voltage2 = tk.Entry(root)



# Button zum Berechnen der Matrix
btn_berechnen = tk.Button(root, text="Berechnen", command=berechnen,width=71,height=5)
btn_berechnen.place(x=460, y=420)



# Textfeld zur Anzeige der Matrix
matrix_display = tk.Text(root, height=24, width=74)
matrix_display.place(x=460, y=0)

# Starte das Hauptfenster
root.mainloop()
