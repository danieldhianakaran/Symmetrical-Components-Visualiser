#!/usr/bin/env python3
"""
Symmetrical-components visualiser
Tkinter GUI – square grid – non-numeric blocking
"""

import math
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# 120° operator ----------------------------------------------------------
a = complex(math.cos(math.radians(120)), math.sin(math.radians(120)))

# ------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------
def polar_to_rect(mag: float, ang: float) -> complex:
    """mag∠ang°  ->  complex"""
    rad = math.radians(ang)
    return complex(mag * math.cos(rad), mag * math.sin(rad))

def compute_symmetrical(Va, Vb, Vc):
    """Fortescue transform"""
    V0 = (Va + Vb + Vc) / 3
    V1 = (Va + a * Vb + a ** 2 * Vc) / 3
    V2 = (Va + a ** 2 * Vb + a * Vc) / 3
    return V0, V1, V2

def cpolar(z):
    return abs(z), math.degrees(math.atan2(z.imag, z.real))

# ------------------------------------------------------------------------
# Input validation
# ------------------------------------------------------------------------
def validate_float(char):
    """Allow only digits, minus, dot and control chars"""
    return char == "" or char in "-.0123456789" or char.isascii() and char.isdigit()

def fetch_float(entry, name):
    """Return float or raise ValueError with friendly message"""
    val = entry.get().strip()
    if not val:
        raise ValueError(f"{name} is empty")
    try:
        return float(val)
    except ValueError:
        raise ValueError(f"{name} must be a real number")

# ------------------------------------------------------------------------
# Plotting
# ------------------------------------------------------------------------
def draw_plot():
    """Read entries → compute → draw square-axis plot"""
    try:
        Va = polar_to_rect(fetch_float(mag_a, "Va magnitude"),
                           fetch_float(ang_a, "Va angle"))
        Vb = polar_to_rect(fetch_float(mag_b, "Vb magnitude"),
                           fetch_float(ang_b, "Vb angle"))
        Vc = polar_to_rect(fetch_float(mag_c, "Vc magnitude"),
                           fetch_float(ang_c, "Vc angle"))
    except ValueError as e:
        messagebox.showerror("Input error", str(e))
        return

    V0, V1, V2 = compute_symmetrical(Va, Vb, Vc)
    
    mag0, ang0 = cpolar(V0)
    mag1, ang1 = cpolar(V1)
    mag2, ang2 = cpolar(V2)

    lbl_zero.config(text=f"Zero  : {mag0:.3f} ∠ {ang0:.2f}°")
    lbl_pos .config(text=f"Pos   : {mag1:.3f} ∠ {ang1:.2f}°")
    lbl_neg .config(text=f"Neg   : {mag2:.3f} ∠ {ang2:.2f}°")

    # --- clear previous drawing -----------------------------------------
    ax.clear()
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color="grey", lw=0.5)
    ax.axvline(0, color="grey", lw=0.5)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_title("Symmetrical-components breakdown")
    ax.set_xlabel("Real")
    ax.set_ylabel("Imaginary")

    # --- helper to plot --------------------------------------------------
    def arrow(comp, start, colour, lbl):
        ax.arrow(start[0], start[1], comp.real, comp.imag,
                 head_width=0.2, head_length=0.2, fc=colour, ec=colour,
                 label=lbl, length_includes_head=True)

    # 1) original phasors
    arrow(Va, (0, 0), "black", "Va")
    arrow(Vb, (0, 0), "black", "Vb")
    arrow(Vc, (0, 0), "black", "Vc")

    # 2) positive sequence (from origin)
    V1a, V1b, V1c = V1, V1 * a, V1 * a ** 2
    arrow(V1a, (0, 0), "blue", "V1a")
    arrow(V1b, (0, 0), "blue", "V1b")
    arrow(V1c, (0, 0), "blue", "V1c")

    # 3) negative sequence (tail on tip of respective positive)
    V2a, V2b, V2c = V2, V2 * a ** 2, V2 * a
    arrow(V2a, (V1a.real, V1a.imag), "green", "V2a")
    arrow(V2b, (V1b.real, V1b.imag), "green", "V2b")
    arrow(V2c, (V1c.real, V1c.imag), "green", "V2c")

    # 4) zero sequence (tail on tip of negative)
    arrow(V0, (V1a.real + V2a.real, V1a.imag + V2a.imag), "red", "V0a")
    arrow(V0, (V1b.real + V2b.real, V1b.imag + V2b.imag), "red", "V0b")
    arrow(V0, (V1c.real + V2c.real, V1c.imag + V2c.imag), "red", "V0c")

    # --- tidy legend ------------------------------------------------------
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc="best")
    
    canvas.draw()

# ------------------------------------------------------------------------
# GUI construction
# ------------------------------------------------------------------------
root = tk.Tk()
root.title("Symmetrical Components Visualiser")
root.resizable(False, False)

# --- register validation command -----------------------------------------
vcmd = (root.register(validate_float), "%S")

# --- left frame for controls ---------------------------------------------
left = ttk.Frame(root, padding=10)
left.grid(row=0, column=0, sticky="nw")

labels = ("Va magnitude", "Va angle°", "Vb magnitude", "Vb angle°",
          "Vc magnitude", "Vc angle°")
entries = []
for idx, text in enumerate(labels):
    ttk.Label(left, text=text).grid(row=idx, column=0, sticky="w", pady=2)
    e = ttk.Entry(left, width=10, validate="key", validatecommand=vcmd)
    e.grid(row=idx, column=1, padx=5, pady=2)
    entries.append(e)

mag_a, ang_a, mag_b, ang_b, mag_c, ang_c = entries

ttk.Button(left, text="Plot", command=draw_plot).grid(
    row=len(labels), column=0, columnspan=2, pady=10)
    
# --------- result area ---------
res_frame = ttk.LabelFrame(left, text="Sequence results (polar)", padding=5)
res_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=10, sticky="ew")
    
lbl_zero  = ttk.Label(res_frame, text="Zero  :  – ∠ – °")
lbl_pos   = ttk.Label(res_frame, text="Pos   :  – ∠ – °")
lbl_neg   = ttk.Label(res_frame, text="Neg   :  – ∠ – °")
lbl_zero.grid(row=0, column=0, sticky="w")
lbl_pos .grid(row=1, column=0, sticky="w")
lbl_neg .grid(row=2, column=0, sticky="w")

# --- right frame for matplotlib ------------------------------------------
right = ttk.Frame(root)
right.grid(row=0, column=1, sticky="nsew")

fig = Figure(figsize=(6, 6), dpi=100)  # square canvas
ax = fig.add_subplot(111)
ax.set_aspect("equal", adjustable="box")
canvas = FigureCanvasTkAgg(fig, master=right)
canvas.get_tk_widget().pack(fill="both", expand=True)

# ------------------------------------------------------------------------
root.mainloop()
