import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

N = 42  # Количество точек (4+17)
Z = 10 # Количество точек после запятой для ошибки восстановления
x_range = np.linspace(0, 1.5, 500)  # Диапазон значений x для построения графиков

def f(x):
    return 1 - np.exp(-x ** 5)

def calculate_error(true_vals, approx_vals):
    return np.mean(np.abs(true_vals - approx_vals))  # Среднее абсолютное отклонение

# Функция для замкнутого Catmull-Rom сплайна
def catmull_rom_spline(x_points, y_points):
    x_points = np.concatenate(([x_points[0]], x_points, [x_points[-1]]))
    y_points = np.concatenate(([y_points[0]], y_points, [y_points[-1]]))
    spline_x = []
    spline_y = []
    for i in range(1, len(x_points) - 2):
        P0, P1, P2, P3 = x_points[i - 1], x_points[i], x_points[i + 1], x_points[i + 2]
        Q0, Q1, Q2, Q3 = y_points[i - 1], y_points[i], y_points[i + 1], y_points[i + 2]

        t_values = np.linspace(0, 1, 100)
        for t in t_values:
            xt = 0.5 * ((2 * P1) + (-P0 + P2) * t + (2 * P0 - 5 * P1 + 4 * P2 - P3) * t ** 2 + (-P0 + 3 * P1 - 3 * P2 + P3) * t ** 3)
            yt = 0.5 * ((2 * Q1) + (-Q0 + Q2) * t + (2 * Q0 - 5 * Q1 + 4 * Q2 - Q3) * t ** 2 + (-Q0 + 3 * Q1 - 3 * Q2 + Q3) * t ** 3)
            spline_x.append(xt)
            spline_y.append(yt)
    return np.array(spline_x), np.array(spline_y)

# Функция для построения графика гармонических колебаний
def plot_f(points_count):
    fig.clear()
    x_points = np.linspace(0, 1.5, points_count)
    y_points = f(x_points)
    y_true = f(x_range)
    ax = fig.add_subplot(111)
    ax.plot(x_range, y_true, label="Гармонические колебания", color='cyan', linewidth=1.5)
    ax.scatter(x_points, y_points, color='red')
    ax.legend()
    ax.set_title("Гармонические колебания")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    for i in table.get_children():
        table.delete(i)
    for x, y in zip(x_points, y_points):
        table.insert("", "end", values=(f"{x:.3f}", f"{y:.3f}"))
    canvas.draw()

# Функции для построения Catmull-Rom сплайна
def plot_catmull_rom_spline(points_count):
    fig.clear()
    x_points = np.linspace(0, 1.5, points_count)
    y_points = f(x_points)
    spline_x, spline_y = catmull_rom_spline(x_points, y_points)
    y_true = f(spline_x)
    error = calculate_error(y_true, spline_y)
    ax = fig.add_subplot(111)
    ax.plot(spline_x, spline_y, label="Catmull-Rom на основе функции", color = 'orange', linestyle='--')
    ax.scatter(x_points, y_points, color='blue')
    ax.legend()
    ax.set_title(f"Catmull-Rom на основе функции\nОшибка восстановления: {error:.{Z}f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    canvas.draw()

def plot_catmull_rom_spline_polynomial(points_count):
    fig.clear()
    x_points = np.linspace(0, 1.5, points_count)
    coefficients = np.polyfit(x_points, f(x_points), points_count - 1)
    polynomial = np.poly1d(coefficients)
    y_points = polynomial(x_points)
    spline = PchipInterpolator(x_points, y_points)
    y_spline = spline(x_range)
    y_true = f(x_range)
    error = calculate_error(y_true, y_spline)
    ax = fig.add_subplot(111)
    ax.plot(x_range, y_spline, label="Catmull-Rom на основе полинома",color = 'green', linestyle='--')
    ax.scatter(x_points, y_points, color='violet')
    ax.legend()
    ax.set_title(f"Catmull-Rom на основе полинома\nОшибка восстановления: {error:.{Z}f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    canvas.draw()

# Создание интерфейса
root = tk.Tk()
root.title("Интерполяционная кривая Catmull-Rom")
root.geometry("800x800")

# График
fig = plt.Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=(0, 5))

# Таблица
table_frame = tk.Frame(root)
table_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=(0, 10))

table = ttk.Treeview(table_frame, columns=("X", "Y"), show='headings')
table.heading("X", text="X")
table.heading("Y", text="Y")
table.pack()

def button1_action():
    plot_f(points_count=N)

def button2_action():
    plot_catmull_rom_spline(points_count=N)

def button3_action():
    plot_catmull_rom_spline_polynomial(points_count=N)

# Панель с кнопками
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

# Кнопки
btn1 = tk.Button(button_frame, text="1 - e^(-x^5)", command=button1_action)
btn1.pack(side=tk.LEFT, padx=(0, 5))

btn2 = tk.Button(button_frame, text="Catmull-Rom на основе функции", command=button2_action)
btn2.pack(side=tk.LEFT, padx=(0, 5))

btn3 = tk.Button(button_frame, text="Catmull-Rom на основе полинома", command=button3_action)
btn3.pack(side=tk.LEFT)

# Запуск интерфейса
root.mainloop()
