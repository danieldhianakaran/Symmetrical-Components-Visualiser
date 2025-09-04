import math
import matplotlib.pyplot as plt
import numpy as np

a = complex(math.cos(math.radians(120)), math.sin(math.radians(120)))

# Function to convert polar form to rectangular form
def polar_to_rect(mag, angle_deg):
    angle_rad = math.radians(angle_deg)
    real = mag * math.cos(angle_rad)
    imag = mag * math.sin(angle_rad)
    return complex(real, imag)

# Function to compute symmetrical components
def compute_symmetrical_components(V_a, V_b, V_c):
    #a = complex(math.cos(math.radians(120)), math.sin(math.radians(120)))
    V_0 = (V_a + V_b + V_c) / 3
    V_1 = (V_a + a * V_b + a**2 * V_c) / 3
    V_2 = (V_a + a**2 * V_b + a * V_c) / 3
    return V_0, V_1, V_2

# Function to plot vectors
def plot_vectors(vectors, start_points, color, label):
    for i, (vec, start) in enumerate(zip(vectors, start_points)):
        plt.arrow(start[0], start[1], vec.real, vec.imag, head_width=0.2, head_length=0.2, color=color[i], label=f"{label} {i+1}")

# Main function
def main():
    # Input vectors
    V_a_mag = float(input("Enter magnitude of V_a: "))
    V_a_angle = float(input("Enter angle of V_a (degrees): "))
    V_b_mag = float(input("Enter magnitude of V_b: "))
    V_b_angle = float(input("Enter angle of V_b (degrees): "))
    V_c_mag = float(input("Enter magnitude of V_c: "))
    V_c_angle = float(input("Enter angle of V_c (degrees): "))

    # Convert input vectors to rectangular form
    V_a = polar_to_rect(V_a_mag, V_a_angle)
    V_b = polar_to_rect(V_b_mag, V_b_angle)
    V_c = polar_to_rect(V_c_mag, V_c_angle)

    # Compute symmetrical components
    V_0, V_1, V_2 = compute_symmetrical_components(V_a, V_b, V_c)

    # Plotting
    plt.figure(figsize=(10, 10))
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    # Plot input vectors
    plot_vectors([V_a, V_b, V_c], [(0, 0), (0, 0), (0, 0)], ['grey', 'grey', 'grey'], "Input")

    # Plot positive sequence vectors
    plot_vectors([V_1, V_1 * a, V_1 * a**2], [(0, 0), (0, 0), (0, 0)], ['blue', 'blue', 'blue'], "Positive")

    # Plot negative sequence vectors
    start_neg1 = (V_1.real, V_1.imag)
    start_neg2 = ((V_1 * a).real, (V_1 * a).imag)
    start_neg3 = ((V_1 * a**2).real, (V_1 * a**2).imag)
    plot_vectors([V_2, V_2 * a**2, V_2 * a], [start_neg1, start_neg2, start_neg3], ['green', 'green', 'green'], "Negative")

    # Plot zero sequence vectors
    start_zero1 = (V_1.real + V_2.real, V_1.imag + V_2.imag)
    start_zero2 = ((V_1 * a).real + (V_2 * a**2).real, (V_1 * a).imag + (V_2 * a**2).imag)
    start_zero3 = ((V_1 * a**2).real + (V_2 * a).real, (V_1 * a**2).imag + (V_2 * a).imag)
    plot_vectors([V_0, V_0, V_0], [start_zero1, start_zero2, start_zero3], ['red', 'red', 'red'], "Zero")

    plt.legend()
    plt.grid()
    plt.title("Symmetrical Components Breakdown")
    plt.xlabel("Real Axis")
    plt.ylabel("Imaginary Axis")
    plt.show()

if __name__ == "__main__":
    main()
