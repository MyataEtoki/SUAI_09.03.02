clc; clear; close all;

% Данные
x = [-2.0 -1.2 -0.4 0.4 1.2 2.0 2.8 3.6 4.4 5.2 6.0 6.8 7.6];
y = [-1.72 -1.03 -0.61 -0.35 0.36 0.54 1.28 1.69 2.07 2.52 2.93 3.59 4.04];

% Массив для интерполированной функции
x_interp = linspace(min(x), max(x), 200);
y_interp = zeros(size(x_interp));

% Для каждого интервала ищем a_i и b_i
for i = 2:length(x)
    a(i) = (y(i) - y(i-1)) / (x(i) - x(i-1));
    b(i) = y(i-1) - a(i) * x(i-1);
end

for j = 1:length(x_interp)
    % ищем, в какой интервал попадает x_interp(j)
    for i = 2:length(x)
        if x_interp(j) >= x(i-1) && x_interp(j) <= x(i)
            y_interp(j) = a(i) * x_interp(j) + b(i);
            break
        end
    end
end
writematrix([x_interp' y_interp'], 'interpolation_data.xlsx', 'Sheet', 1, 'Range', 'A1');

% Аппроксимация


n = length(x);

% Суммы степеней
S0 = n;
S1 = sum(x);
S2 = sum(x.^2);
S3 = sum(x.^3);
S4 = sum(x.^4);
S5 = sum(x.^5);
S6 = sum(x.^6);

T0 = sum(y);
T1 = sum(x .* y);
T2 = sum(x.^2 .* y);
T3 = sum(x.^3 .* y);

% Матрица и правая часть
M = [S0 S1 S2 S3;
     S1 S2 S3 S4;
     S2 S3 S4 S5;
     S3 S4 S5 S6];

R = [T0; T1; T2; T3];

% Решение системы 
P = M\R;  % [A; B; C; D]

A = P(4); B = P(3); C = P(2); D = P(1);

% Построение аппроксимирующей кривой
y_approx = A*x.^3 + B*x.^2 + C*x + D;

% Ошибка аппроксимации
E = sqrt(sum((y_approx - y).^2) / (n + 1));
E_rel = E / mean(abs(y));

% Графики 
figure;
plot(x, y, 'go', 'MarkerFaceColor', 'g', 'DisplayName', 'Исходные данные'); hold on;
plot(x_interp, y_interp, 'b--', 'LineWidth', 1.5, 'DisplayName', 'Интерполяция');
plot(x, y_approx, 'r-', 'LineWidth', 2, 'DisplayName', 'Аппроксимация (3 степень)');
legend('Location','best');
xlabel('x'); ylabel('y');
title(sprintf('Интерполяция и аппроксимация. Ошибка E = %.4f', E_rel));
grid on;
