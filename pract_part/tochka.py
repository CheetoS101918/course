import matplotlib.pyplot as plt
import numpy as np
from math import ceil

# # Данные
# fixed_costs = 49078.02   # Постоянные затраты (CF)
# price_per_unit = 411.55  # Цена единицы продукции (P)
# var_cost_per_unit = 114.515  # Переменные издержки на единицу (V)
# break_even_qty = 287  # Точка безубыточности (Qкр)
# project_qty = 477

# КОСТЯ
# fixed_costs = 88532.68   # Постоянные затраты (CF)
# price_per_unit = 479.38  # Цена единицы продукции (P)
# var_cost_per_unit = 108206.63  # Переменные издержки на единицу (V)
# break_even_qty = 350  # Точка безубыточности (Qкр)
# project_qty = 479

# Исходные данные
# CF = 49078.02  # постоянные расходы, тыс. руб.
# cv_total = 114515.41  # общие переменные расходы, тыс. руб.
# price = 411.55  # цена единицы продукции, тыс. руб.
# Q_max = 477  # годовой объем производства, шт.


CF = 88532.68  # постоянные расходы, тыс. руб.
cv_total = 108206.63  # общие переменные расходы, тыс. руб.
price = 479.38  # цена единицы продукции, тыс. руб.
Q_max = 479  # годовой объем производства, шт.



# Расчет переменных расходов на единицу продукции
cv_unit = cv_total / Q_max

# Расчет точки безубыточности
Q_be = ceil(CF / (price - cv_unit))

# Создание массива объемов производства
Q = np.linspace(0, Q_max * 1.2, 100)

# Расчет финансовых показателей
revenue = price * Q  # выручка
variable_costs = cv_unit * Q  # переменные затраты
fixed_costs_line = np.ones_like(Q) * CF  # постоянные затраты
total_costs = CF + variable_costs  # общие затраты

# Создание графика
plt.figure(figsize=(12, 8), facecolor='white')

# Построение основных линий с различными стилями для Ч/Б печати
plt.plot(Q, revenue, 'k-', linewidth=2.5)  # Выручка - сплошная линия
plt.plot(Q, total_costs, 'k--', linewidth=2.5)  # Общие затраты - пунктир
plt.plot(Q, variable_costs, 'k-.', linewidth=2)  # Переменные затраты - штрих-пунктир
plt.plot(Q, fixed_costs_line, 'k:', linewidth=2)  # Постоянные затраты - точечная линия

# Вертикальная линия в точке безубыточности
plt.axvline(x=Q_be, color='k', linestyle='-', linewidth=1.5)

# Точка безубыточности
plt.plot(Q_be, price * Q_be, 'ko', markersize=8)
plt.plot(Q_be, CF + cv_unit * Q_be, 'ko', markersize=8)

fontsize = 9

# Подписи на линиях
plt.text(Q_max * 0.7, price * Q_max * 0.8, f'Выручка', fontsize=fontsize,
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
plt.text(Q_max * 0.7, (CF + cv_unit * Q_max * 0.9) * 0.8, f'Общие затраты',
         fontsize=fontsize, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
plt.text(Q_max * 0.9, cv_unit * Q_max * 0.9, f'Переменные затраты',
         fontsize=fontsize, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
plt.text(Q_max * 0.1, CF * 1.05, f'Постоянные затраты',
         fontsize=fontsize, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# Подпись точки безубыточности
plt.text(Q_be + 5, price * Q_be + 2000, f'Точка безубыточности\n({Q_be:.1f} шт.; {(price * Q_be):.1f} тыс. руб.)',
         fontsize=fontsize, bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))

# Подпись для линии себестоимости (общих затрат)
plt.text(Q_max * 0.3, CF + cv_unit * Q_max * 0.28, f'Себестоимость',
         fontsize=fontsize, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# Отметка годового объема производства
plt.axvline(x=Q_max, color='k', linestyle='-', linewidth=1, alpha=0.7)
plt.text(Q_max + 5, 5000, f'Годовой объем\nпроизводства\n({Q_max} шт.)',
         fontsize=fontsize, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# Дополнительный расчет прибыли при максимальном объеме
profit_at_max = price * Q_max - (CF + cv_unit * Q_max)
plt.text(Q_max - 40, price * Q_max - 10000, f'Прибыль при Q={Q_max} шт.:\n{profit_at_max:.2f} тыс. руб.',
         fontsize=fontsize, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# Настройка графика
plt.title('График безубыточности производства', fontsize=16, pad=20)
plt.xlabel('Объем производства, шт.', fontsize=14, labelpad=10)
plt.ylabel('Денежные средства, тыс. руб.', fontsize=14, labelpad=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', alpha=0.4)

# Установка пределов осей
plt.xlim(0, Q_max * 1.2)
plt.ylim(0, max(revenue[-1], total_costs[-1]) * 1.1)

# Форматирование осей
plt.xticks(np.arange(0, Q_max * 1.3, 50))
plt.yticks(np.arange(0, max(revenue[-1], total_costs[-1]) * 1.2, 20000))

# Убираем легенду согласно требованию
plt.legend().set_visible(False)

# Финальная настройка
plt.tight_layout()

# Отображение графика
plt.show()