import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math  # Импортируем math для вычисления факториалов

N = 42  # Количество точек (4+17)
Z = 10  # Количество точек после запятой для ошибки восстановления
x_range = np.linspace(0, 1.5, 500)  # Диапазон значений x для построения графиков


def f(x):
    return 1 - np.exp(-x ** 5)


def calculate_error(true_vals, approx_vals):
    return np.mean(np.abs(true_vals - approx_vals))  # Среднее абсолютное отклонение


# Функция для кубической кривой Безье
def bezier_curve(control_points, num_points=100):
    n = len(control_points) - 1
    t_values = np.linspace(0, 1, num_points)
    bezier_points = np.zeros((num_points, 2))

    for i in range(n + 1):
        binomial_coefficient = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
        bezier_points[:, 0] += binomial_coefficient * ((1 - t_values) ** (n - i)) * (t_values ** i) * control_points[
            i, 0]
        bezier_points[:, 1] += binomial_coefficient * ((1 - t_values) ** (n - i)) * (t_values ** i) * control_points[
            i, 1]

    return bezier_points[:, 0], bezier_points[:, 1]


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


# Функция для построения кривой Безье
def plot_bezier_curve(points_count):
    fig.clear()
    x_points = np.linspace(0, 1.5, points_count)
    y_points = f(x_points)
    control_points = np.vstack((x_points, y_points)).T
    bezier_x, bezier_y = bezier_curve(control_points)

    y_true = f(bezier_x)
    error = calculate_error(y_true, bezier_y)

    ax = fig.add_subplot(111)

    # Рисуем прямые между контрольными точками
    ax.plot(control_points[:, 0], control_points[:, 1], 'k--', lw=1, label="Прямые между контрольными точками")

    ax.plot(bezier_x, bezier_y, label="Кривая Безье на основе функции", color='orange', linestyle='--')
    ax.scatter(x_points, y_points, color='blue')
    ax.legend()
    ax.set_title(f"Кривая Безье на основе функции\nОшибка восстановления: {error:.{Z}f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    canvas.draw()


# Функция для построения кривой Безье на основе полинома
def plot_bezier_curve_polynomial(points_count):
    fig.clear()
    x_points = np.linspace(0, 1.5, points_count)
    coefficients = np.polyfit(x_points, f(x_points), points_count - 1)
    polynomial = np.poly1d(coefficients)
    y_points = polynomial(x_points)
    control_points = np.vstack((x_points, y_points)).T
    bezier_x, bezier_y = bezier_curve(control_points)

    y_true = f(bezier_x)
    error = calculate_error(y_true, bezier_y)

    ax = fig.add_subplot(111)

    # Рисуем прямые между контрольными точками
    ax.plot(control_points[:, 0], control_points[:, 1], 'k--', lw=1, label="Прямые между контрольными точками")

    ax.plot(bezier_x, bezier_y, label="Кривая Безье на основе полинома", color='green', linestyle='--')
    ax.scatter(x_points, y_points, color='violet')
    ax.legend()
    ax.set_title(f"Кривая Безье на основе полинома\nОшибка восстановления: {error:.{Z}f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    canvas.draw()


# Создание интерфейса
root = tk.Tk()
root.title("Интерполяционная кривая Безье")
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
    plot_bezier_curve(points_count=N)


def button3_action():
    plot_bezier_curve_polynomial(points_count=N)


# Панель с кнопками
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

# Кнопки
btn1 = tk.Button(button_frame, text="1 - e^(-x^5)", command=button1_action)
btn1.pack(side=tk.LEFT, padx=(0, 5))

btn2 = tk.Button(button_frame, text="Кривая Безье на основе функции", command=button2_action)
btn2.pack(side=tk.LEFT, padx=(0, 5))

btn3 = tk.Button(button_frame, text="Кривая Безье на основе полинома", command=button3_action)
btn3.pack(side=tk.LEFT)

# Запуск интерфейса
root.mainloop()
