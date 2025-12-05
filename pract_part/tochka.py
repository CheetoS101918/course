import matplotlib.pyplot as plt
import numpy as np

# Данные из документа (в тыс. руб.)
fixed_costs = 42360.13  # Постоянные затраты (CF)
price_per_unit = 405.646  # Цена единицы продукции (P)
var_cost_per_unit = 216.123  # Переменные издержки на единицу (V)
break_even_qty = 223  # Точка безубыточности (Qкр)
project_qty = 364  # Проектный объем производства (предполагается на основе расчетов)

# Диапазон для оси X (объем производства, от 0 до 500 для лучшей визуализации)
q = np.linspace(0, 500, 501)

# Расчеты
revenue = price_per_unit * q  # Выручка от реализации
var_costs = var_cost_per_unit * q  # Переменные затраты
total_costs = fixed_costs + var_costs  # Себестоимость (общие затраты)

# Построение графика
plt.figure(figsize=(10, 6))

# Линия выручки
plt.plot(q, revenue, label='Выручка от реализации', color='green')

# Линия переменных затрат
plt.plot(q, var_costs, label='Переменные затраты', color='blue')

# Линия постоянных затрат (горизонтальная)
plt.axhline(fixed_costs, label='Постоянные затраты', color='orange', linestyle='--')

# Линия общих затрат
plt.plot(q, total_costs, label='Себестоимость', color='red')

# Точка безубыточности
break_even_revenue = price_per_unit * break_even_qty
plt.plot(break_even_qty, break_even_revenue, 'ro', label='Точка безубыточности')

# Точки для проектного объема
project_revenue = price_per_unit * project_qty
project_var_costs = var_cost_per_unit * project_qty
plt.plot(project_qty, project_revenue, 'go', label='Выручка при проектном объеме')
plt.plot(project_qty, project_var_costs, 'bo', label='Переменные затраты при проектном объеме')

# Оси и заголовок
plt.xlabel('Объем производства (Q, шт)')
plt.ylabel('Тыс. руб.')
plt.title('График безубыточности')
plt.legend()
plt.grid(True)

# Сохранение в PNG
plt.savefig('break_even.png')
plt.close()  # Закрыть фигуру, чтобы не отображалась в выводе, если запускается в интерактивной среде

print("График сохранен в файл 'tochka.png'")