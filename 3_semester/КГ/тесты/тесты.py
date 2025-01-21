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