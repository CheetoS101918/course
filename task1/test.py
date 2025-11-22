from funcs import *
import pandas as pd
import numpy as np

# Пример исходных данных для Варианта 3
materials_main_example = { 'стальной прокат': { 'type': 'material',
                       'A': { 'rasxod': np.float64(0.45),
                              'otxod': np.float64(0.0675)},
                       'B': { 'rasxod': np.float64(0.05),
                              'otxod': np.float64(0.005)}},
  'трубы стальные': { 'type': 'material',
                      'A': { 'rasxod': np.float64(0.04),
                             'otxod': np.float64(0.0028)},
                      'B': { 'rasxod': np.float64(0.005),
                             'otxod': np.float64(0.0003)}},
  'прокат цветных металлов': { 'type': 'fixed',
                               'A': np.int64(2900),
                               'B': np.int64(3000)},
  'другие материалы': { 'type': 'fixed',
                        'A': np.int64(1800),
                        'B': np.int64(1700)}}


materials_purchased_example = {
    "отливки черных металлов": {"type": "material", "A": {"rasxod": 4.5, "otxod": 0.675}, "B": {"rasxod": 2.2, "otxod": 0.484}},
    "отливки цветных металлов": {"type": "material", "A": {"rasxod": 0.3, "otxod": 0.075}, "B": {"rasxod": 0.25, "otxod": 0.05}},
    "покупные комплектующие изделия": {"type": "fixed", "A": 142800, "B": 75800}
}


# !!!!!!!!!!  ^^^   "покупные комплектующие изделия": {"type": "fixed", "A": 142800, "B": 75800}    !!!!!!!!!!!!  ^^^


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

fuel_energy_example = {"A": 1, "B": 0.9}
labor_example = {
    "labor_hours": {"A": 1000, "B": 171},
    "hourly_rate": {"A": 41.50, "B": 35.60}
}
rates_example = {
    "доп_зарплата": 40,
    "отчисления": 22,
    "РСЭО": 87,
    "ОПР": 85,
    "ОХР": 98,
    "ВПР": 5,
    "рентабельность": 20
}
volume_base_example = {"A": 195, "B": 60}

# --- Входные коэффициенты ---
Ka_input = 1.06 # Коэффициент для корректировки объема
Kj_input = 0.92 # Пример
Ktr_input = 1.15

# --- Сохранение CSV ---
csv_table_input = generate_input_table_csv(
    materials_main_example, materials_purchased_example,
    prices_example, fuel_energy_example, labor_example, rates_example,
    volume_base_example, Ka_input, Kj_input, Ktr_input
)
csv_input_filename = "input_data_table.csv"
with open(csv_input_filename, 'w', encoding='utf-8', newline='') as csvfile:
    csvfile.write(csv_table_input)

to_js = csv_to_json_structure(csv_input_filename)
with open("input_data_table.json", "w", encoding="utf-8") as f:
    json.dump(to_js, f, ensure_ascii=False, indent=4)


# --- Выполнение основной логики ---
# print("Исходные данные:")
# print(f"Ka = {Ka_input}, Kj = {Kj_input}, Ktr = {Ktr_input}")
# print(f"Базовый объем (из Дополнения 1, Вар. 3): {volume_base_example}")
# Q_A_calc = int(volume_base_example["A"] * Ka_input)
# Q_B_calc = int(volume_base_example["B"] * Ka_input)
# print(f"Рассчитанные объемы (Q_base * Ka, округленные до меньшего целого): A = {Q_A_calc}, B = {Q_B_calc}")
# print(f"Основные материалы: {materials_main_example}")
# print(f"Покупные ПФ+Комплектующие: {materials_purchased_example}")
# print(f"Цены: {prices_example}")
# print(f"Топливо и энергия: {fuel_energy_example}")
# print(f"Трудоемкость и ставка: {labor_example}")
# print(f"Процентные ставки: {rates_example}")
print("\n" + "="*50 + "\n")

# Генерация вывода для изделий А и Б
output_result, structure_data_A, structure_data_B, details_A, details_B = generate_full_output(  # Изменено: принимаем пять значений
    volume_base_example, Ka_input, Kj_input, Ktr_input,
    materials_main_example, materials_purchased_example,
    prices_example, fuel_energy_example, labor_example, rates_example
)

print("Расчет по статьям:")
print(output_result)

# Теперь используем generate_output_by_punkt для нового формата вывода
new_format_output = generate_output_by_punkt(structure_data_A, structure_data_B, details_A, details_B, rates_example)

print("\n" + "="*80 + "\n")
print("РАСЧЕТ В НОВОМ ФОРМАТЕ (по пунктам):")
print(new_format_output)

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
    # _, item_structure = generate_output_for_item(
    #     item, Q_item, 1, Ktr_input,
    #     combined_materials, prices_example, fuel_energy_example, prepared_labor, rates_example
    # )
    # if item == 'A':
    #     structure_data_A = item_structure
    # else:
    #     structure_data_B = item_structure

    _, item_structure, item_details = generate_output_for_item(
        item, Q_item, Ka_input, Ktr_input,
        combined_materials, prices_example, fuel_energy_example, prepared_labor, rates_example
    )

    if item == 'A':
        structure_data_A = item_structure
        details_A = item_details
    else:
        structure_data_B = item_structure
        details_B = item_details

output_result = generate_output_by_punkt(structure_data_A, structure_data_B, details_A, details_B, rates_example)

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

volumes_output += f"Годовой объем товарной продукции  A: {(price_A * Q_A) / 1000:.2f} тыс. руб. \n"
volumes_output += f"Годовой объем товарной продукции  Б: {(price_B * Q_B) / 1000:.2f} тыс. руб. \n \n"

volumes_output += "Объем реализованной продукции (Qр):\n"
volumes_output += f"Qр = Qн + Qт – Qк (1.7)\n"
volumes_output += "где:\n"
volumes_output += "Qн – остатки готовой продукции на складе на начало года, тыс.руб. (2% от объема товарной продукции);\n"
volumes_output += "Qк – остатки готовой продукции на конец года, тыс.руб. (принимается 1,5% от объема товарной продукции).\n"
volumes_output += f"Qр = {Q_t:.2f} * 0,02 + {Q_t:.2f} - {Q_t:.2f} * 0,015 = {Q_p:.2f} тыс. руб.\n"

print(volumes_output)
save_structure_table_to_json(structure_data_A, structure_data_B)


individual_volumes_data = {
    "Изделие": "А",
    "Годовой_объем_выпуска": Q_A,
    "Оптовая_цена_за_единицу": round(price_A, 2),
    "Объем_товарной_продукции_по_изделию тыс руб": round(Q_A * price_A / 1000, 2) # в тыс.руб
}
individual_volumes_data_B = {
    "Изделие": "Б",
    "Годовой_объем_выпуска": Q_B,
    "Оптовая_цена_за_единицу": round(price_B, 2),
    "Объем_товарной_продукции_по_изделию тыс руб": round(Q_B * price_B / 1000, 2) # в тыс.руб
}
other = {
    'Qt': Q_t,
    'Qr': Q_p
}

# Сохраняем в JSON файл (например, список из двух словарей)
individual_volumes_json_filename = "individual_product_volumes.json"
with open(individual_volumes_json_filename, 'w', encoding='utf-8') as jsonfile:
    # Записываем оба изделия в один файл как список
    json.dump([individual_volumes_data, individual_volumes_data_B, other], jsonfile, indent=4, ensure_ascii=False)

print(f"\nJSON с отдельными объемами товарной продукции сохранен в файл: {individual_volumes_json_filename}")
