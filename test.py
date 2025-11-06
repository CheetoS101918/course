from funcs import *

# --- 4. Основная логика скрипта ---

# Пример исходных данных для Варианта 3
materials_main_example = {
    "стальной прокат": {"type": "material", "A": {"rasxod": 0.62, "otxod": 0.1116}, "B": {"rasxod": 0.07, "otxod": 0.007}},
    "трубы стальные": {"type": "material", "A": {"rasxod": 0.06, "otxod": 0.0042}, "B": {"rasxod": 0.05, "otxod": 0.004}},
    "прокат цветных металлов": {"type": "fixed", "A": 2500, "B": 3200},
    "другие материалы": {"type": "fixed", "A": 800, "B": 950}
}

materials_purchased_example = {
    "отливки черных металлов": {"type": "material", "A": {"rasxod": 2.6, "otxod": 0.468}, "B": {"rasxod": 2.9, "otxod": 0.464}},
    "отливки цветных металлов": {"type": "material", "A": {"rasxod": 0.32, "otxod": 0.0736}, "B": {"rasxod": 0.28, "otxod": 0.0504}},
    "покупные комплектующие изделия": {"type": "fixed", "A": 136800, "B": 118300}
}

prices_example = {
    "стальной прокат_материал": 12800,
    "стальной прокат_отходы": 7500,
    "трубы стальные_материал": 18500,
    "трубы стальные_отходы": 6300,
    "отливки черных металлов_материал": 10500,
    "отливки черных металлов_отходы": 7200,
    "отливки цветных металлов_материал": 22600,
    "отливки цветных металлов_отходы": 16900,
}

fuel_energy_example = {"A": 1.6, "B": 1.2}
labor_example = {
    "labor_hours": {"A": 893.0, "B": 177.65},
    "hourly_rate": {"A": 41.50, "B": 35.60}
}
rates_example = {
    "доп_зарплата": 40,
    "отчисления": 22,
    "РСЭО": 80,
    "ОПР": 90,
    "ОХР": 110,
    "ВПР": 3,
    "рентабельность": 22
}
volume_base_example = {"A": 98, "B": 65}

# --- Входные коэффициенты ---
Ka_input = 1.04 # Коэффициент для корректировки объема
Kj_input = 0.95 # Пример
Ktr_input = 1.15 # Пример из расчета

# --- Сохранение CSV ---
csv_table_input = generate_input_table_csv(
    materials_main_example, materials_purchased_example,
    prices_example, fuel_energy_example, labor_example, rates_example,
    volume_base_example, Ka_input, Kj_input, Ktr_input
)
csv_input_filename = "input_data_table.csv"
with open(csv_input_filename, 'w', encoding='utf-8', newline='') as csvfile:
    csvfile.write(csv_table_input)

print(f"CSV таблица исходных данных сохранена в файл: {csv_input_filename}")

# --- Выполнение основной логики ---
print("Исходные данные:")
print(f"Ka = {Ka_input}, Kj = {Kj_input}, Ktr = {Ktr_input}")
print(f"Базовый объем (из Дополнения 1, Вар. 3): {volume_base_example}")
Q_A_calc = int(volume_base_example["A"] * Ka_input)
Q_B_calc = int(volume_base_example["B"] * Ka_input)
print(f"Рассчитанные объемы (Q_base * Ka, округленные до меньшего целого): A = {Q_A_calc}, B = {Q_B_calc}")
print(f"Основные материалы: {materials_main_example}")
print(f"Покупные ПФ+Комплектующие: {materials_purchased_example}")
print(f"Цены: {prices_example}")
print(f"Топливо и энергия: {fuel_energy_example}")
print(f"Трудоемкость и ставка: {labor_example}")
print(f"Процентные ставки: {rates_example}")
print("\n" + "="*50 + "\n")

# Генерация вывода для изделий А и Б
output_result = generate_full_output(
    volume_base_example, Ka_input, Kj_input, Ktr_input,
    materials_main_example, materials_purchased_example,
    prices_example, fuel_energy_example, labor_example, rates_example
)

print("Расчет по статьям:")
print(output_result)

# --- Новый код для получения данных структуры ---
prepared_materials_main, prepared_labor, prepared_volume = prepare_data_with_coefficients(
    materials_main_example, labor_example, volume_base_example, Ka_input, Kj_input
)
prepared_materials_purchased, _, _ = prepare_data_with_coefficients(
    materials_purchased_example, {"labor_hours": {"A": 1, "B": 1}}, {"A": 1, "B": 1}, 1, Kj_input
)
combined_materials = {**prepared_materials_main, **prepared_materials_purchased}

structure_data_A = {}
structure_data_B = {}
for item in ['A', 'B']:
    Q_item = prepared_volume[item]
    _, item_structure = generate_output_for_item(
        item, Q_item, 1, Ktr_input,
        combined_materials, prices_example, fuel_energy_example, prepared_labor, rates_example
    )
    if item == 'A':
        structure_data_A = item_structure
    else:
        structure_data_B = item_structure

# --- Конец нового кода ---

# Генерация CSV и сохранение в файл
csv_table_content = generate_structure_table_csv(structure_data_A, structure_data_B)

# Сохранение CSV в файл
csv_filename = "sebestoimost_structure.csv"
with open(csv_filename, 'w', encoding='utf-8', newline='') as csvfile:
    csvfile.write(csv_table_content)

print(f"\nCSV таблица сохранена в файл: {csv_filename}")


Q_t, Q_p, Q_A, Q_B, price_A, price_B = calculate_product_volumes(structure_data_A, structure_data_B)

# Формируем и выводим расчет для объемов продукции
volumes_output = "\n--- Расчет объемов продукции ---\n"

volumes_output += "Объем товарной продукции (Qт):\n"
volumes_output += f"QT = QA * ЦА + QБ * ЦБ (1.6)\n"
volumes_output += "где:\n"
volumes_output += "QA и QБ – годовой объем производства изделий А и Б, шт.;\n"
volumes_output += "ЦА и ЦБ – оптовая цена предприятия изделий А и Б.\n"
volumes_output += f"QT = ({price_A:.2f} * {Q_A} + {price_B:.2f} * {Q_B}) / 1000 = {Q_t:.2f} тыс.руб.\n\n"

volumes_output += "Объем реализованной продукции (Qр):\n"
volumes_output += f"Qр = Qн + Qт – Qк (1.7)\n"
volumes_output += "где:\n"
volumes_output += "Qн – остатки готовой продукции на складе на начало года, тыс.руб. (2% от объема товарной продукции);\n"
volumes_output += "Qк – остатки готовой продукции на конец года, тыс.руб. (принимается 1,5% от объема товарной продукции).\n"
volumes_output += f"Qр = {Q_t:.2f} * 0,02 + {Q_t:.2f} - {Q_t:.2f} * 0,015 = {Q_p:.2f} тыс. руб.\n"

print(volumes_output)
