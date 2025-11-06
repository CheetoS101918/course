import csv
import io

def calculate_material_costs(norma_rasxoda, norma_otxoda, price_mat, price_otxod, Ktr=1.0):
    """
    Расчет затрат на один вид основного материала или покупного полуфабриката
    для одного изделия по формуле: Сi = (Нmi * Цmi * Kтр - Н0i * Ц0i).

    Args:
        norma_rasxoda (float): Норма расхода материала (в тоннах).
        norma_otxoda (float): Норма отходов (в тоннах).
        price_mat (float): Цена материала (руб/т).
        price_otxod (float): Цена отходов (руб/т).
        Ktr (float): Коэффициент транспортно-заготовительных расходов.

    Returns:
        float: Затраты на материал/полуфабрикат для одного изделия, руб.
    """
    cost = (norma_rasxoda * price_mat * Ktr - norma_otxoda * price_otxod)
    return cost

def calculate_total_material_costs(components_data, prices, Ktr=1.0, item='A'):
    """
    Расчет общей суммы затрат на все основные материалы и покупные полуфабрикаты
    (включая комплектующие) для одного изделия.

    Args:
        components_data (dict): Словарь с нормами расхода/отходов и фикс. стоимостями.
                                Пример:
                                {
                                    'стальной прокат': {'type': 'material', 'A': {'rasxod': 0.62, 'otxod': 0.1116}, 'B': {...}},
                                    'трубы стальные': {'type': 'material', 'A': {'rasxod': 0.06, 'otxod': 0.0042}, 'B': {...}},
                                    'электромоторы': {'type': 'fixed', 'A': 36000, 'B': 5000},
                                    ...
                                }
        prices (dict): Словарь с ценами на материалы и отходы.
                       Пример:
                       {
                           'стальной прокат_материал': 12800,
                           'стальной прокат_отходы': 7500,
                           ...
                       }
        Ktr (float): Коэффициент транспортно-заготовительных расходов.
        item (str): 'A' или 'B', для какого изделия рассчитываются затраты.

    Returns:
        float: Общие затраты на материалы и полуфабрикаты для одного изделия, руб.
    """
    total_cost = 0.0
    for component_name, component_info in components_data.items():
        comp_type = component_info.get("type", "fixed")
        if comp_type == "material":
            norma_rasxoda = component_info[item]['rasxod']
            norma_otxoda = component_info[item]['otxod']
            price_mat = prices.get(f"{component_name}_материал")
            price_otxod = prices.get(f"{component_name}_отходы")

            if price_mat is None or price_otxod is None:
                print(f"Предупреждение: Цены для '{component_name}' не найдены в 'prices'.")
                continue

            cost = calculate_material_costs(norma_rasxoda, norma_otxoda, price_mat, price_otxod, Ktr)
            total_cost += cost
        else: # comp_type == "fixed"
            fixed_cost = component_info.get(item)
            if fixed_cost is not None:
                total_cost += fixed_cost
            else:
                print(f"Предупреждение: Фиксированная стоимость для '{component_name}' и изделия '{item}' не найдена.")

    return total_cost

def calculate_fuel_energy_costs(total_material_costs_item, fuel_energy_percentage):
    """
    Расчет затрат на топливо и энергию для одного изделия как процент от СУММЫ материальных расходов.
    Формула: Впер = ((Вом + Впф + Вком) * βпер) / (100 - βпер)

    Args:
        total_material_costs_item (float): Общие затраты на все материалы/ПФ/Комплектующие для одного изделия, руб.
        fuel_energy_percentage (float): Процент топлива и энергии от общей суммы материальных расходов.

    Returns:
        float: Затраты на топливо и энергию для одного изделия, руб.
    """
    # Применяем формулу (1.4) из методички
    fuel_energy_cost = (total_material_costs_item * fuel_energy_percentage) / (100 - fuel_energy_percentage)
    return fuel_energy_cost

def calculate_basic_wage(labor_hours, hourly_rate):
    """
    Расчет основной заработной платы для одного изделия по формуле Сосн = t * Т.

    Args:
        labor_hours (float): Суммарная трудоемкость (t), нормо-часов.
        hourly_rate (float): Часовая тарифная ставка (Т), руб/час.

    Returns:
        float: Основная заработная плата для одного изделия, руб.
    """
    wage = labor_hours * hourly_rate
    return wage

def calculate_additional_wage(basic_wage, additional_wage_percentage):
    """
    Расчет дополнительной заработной платы как процент от основной.

    Args:
        basic_wage (float): Основная заработная плата, руб.
        additional_wage_percentage (float): Процент дополнительной зарплаты.

    Returns:
        float: Дополнительная заработная плата, руб.
    """
    additional_wage = basic_wage * (additional_wage_percentage / 100)
    return additional_wage

def calculate_social_contributions(basic_wage, additional_wage, social_percentage):
    """
    Расчет отчислений в фонды социальных мероприятий как процент от (основной + дополнительной) з/п.

    Args:
        basic_wage (float): Основная заработная плата, руб.
        additional_wage (float): Дополнительная заработная плата, руб.
        social_percentage (float): Процент отчислений.

    Returns:
        float: Отчисления в фонды социальных мероприятий, руб.
    """
    social_contributions = (basic_wage + additional_wage) * (social_percentage / 100)
    return social_contributions

def calculate_overhead_costs(base_wage, overhead_percentage):
    """
    Расчет РСЭО, ОПР или ОХР как процент от базы (обычно основной з/п).

    Args:
        base_wage (float): База для расчета (например, основная з/п), руб.
        overhead_percentage (float): Процент расходов (РСЭО, ОПР, ОХР).

    Returns:
        float: Сумма расходов (РСЭО, ОПР или ОХР), руб.
    """
    overhead_cost = base_wage * (overhead_percentage / 100)
    return overhead_cost

def calculate_production_cost(material_costs, fuel_energy, basic_wage, additional_wage, social_contributions, rsuo_costs, opr_costs, oxr_costs):
    """
    Расчет полной производственной себестоимости единицы изделия.

    Args:
        material_costs (float): Затраты на *все* материалы/ПФ/Комплектующие, руб.
        fuel_energy (float): Затраты на топливо и энергию, руб.
        basic_wage (float): Основная з/п, руб.
        additional_wage (float): Дополнительная з/п, руб.
        social_contributions (float): Отчисления, руб.
        rsuo_costs (float): РСЭО, руб.
        opr_costs (float): ОПР, руб.
        oxr_costs (float): ОХР, руб.

    Returns:
        float: Производственная себестоимость единицы изделия, руб.
    """
    production_cost = (material_costs + fuel_energy + basic_wage + additional_wage +
                       social_contributions + rsuo_costs + opr_costs + oxr_costs)
    return production_cost

def calculate_selling_cost(production_cost, selling_percentage):
    """
    Расчет внепроизводственных расходов как процент от производственной себестоимости.

    Args:
        production_cost (float): Производственная себестоимость, руб.
        selling_percentage (float): Процент внепроизводственных расходов.

    Returns:
        float: Внепроизводственные расходы, руб.
    """
    selling_cost = production_cost * (selling_percentage / 100)
    return selling_cost

def calculate_full_cost(production_cost, selling_cost):
    """
    Расчет полной (коммерческой) себестоимости единицы изделия.

    Args:
        production_cost (float): Производственная себестоимость, руб.
        selling_cost (float): Внепроизводственные расходы, руб.

    Returns:
        float: Полная себестоимость единицы изделия, руб.
    """
    full_cost = production_cost + selling_cost
    return full_cost

def calculate_opt_price(full_cost, profitability_percentage):
    """
    Расчет оптовой (отпускной) цены на основе полной себестоимости и рентабельности.

    Args:
        full_cost (float): Полная себестоимость, руб.
        profitability_percentage (float): Норматив рентабельности, %.

    Returns:
        float: Оптовая цена, руб.
    """
    opt_price = full_cost * (1 + profitability_percentage / 100)
    return opt_price

def calculate_structure_percentage(item_cost, total_cost):
    """
    Расчет удельного веса (в %) статьи в общей себестоимости.

    Args:
        item_cost (float): Значение статьи (например, на годовой выпуск), тыс. руб.
        total_cost (float): Общая себестоимость (на годовой выпуск), тыс. руб.

    Returns:
        float: Удельный вес статьи, %.
    """
    if total_cost == 0:
        return 0 # Избегаем деления на ноль
    percentage = (item_cost / total_cost) * 100
    return percentage


# --- 3. Создание шаблона вывода ---
# (См. пункт 3 плана)

def format_cost(value, unit="руб."):
    """Форматирует числовое значение стоимости для вывода."""
    return f"{value:.2f} {unit}"

def format_cost_annual(value):
    """Форматирует числовое значение годовой стоимости для вывода (в руб. и тыс.руб.)."""
    value_thousands = value / 1000
    return f"{value:.2f} руб. = {value_thousands:.2f} тыс.руб."

def format_percentage(value):
    """Форматирует числовое значение процента для вывода."""
    return f"{value:.2f}%"

def calculate_costs_split(data_dict, prices_dict, ktr, item):
    """Вспомогательная функция для разделения расчетов материалов."""
    total_cost = 0.0
    breakdown_parts = []
    for comp_name, comp_info in data_dict.items():
        comp_type = comp_info.get("type", "fixed")
        if comp_type == "material":
             norma_rasxoda = comp_info[item]['rasxod']
             norma_otxoda = comp_info[item]['otxod']
             price_mat = prices_dict.get(f"{comp_name}_материал")
             price_otxod = prices_dict.get(f"{comp_name}_отходы")
             if price_mat is not None and price_otxod is not None:
                 cost_part_val = (norma_rasxoda * price_mat * ktr - norma_otxoda * price_otxod)
                 total_cost += cost_part_val
                 breakdown_parts.append(f"({norma_rasxoda}*{price_mat}*{ktr}-{norma_otxoda}*{price_otxod})")
             else:
                 print(f"Предупреждение: Цены для '{comp_name}' не найдены в 'prices'.")
        else: # comp_type == "fixed"
             fixed_cost = comp_info.get(item)
             if fixed_cost is not None:
                 total_cost += fixed_cost
                 breakdown_parts.append(f"{fixed_cost}")
             else:
                 print(f"Предупреждение: Фиксированная стоимость для '{comp_name}' и изделия '{item}' не найдена.")
    breakdown_str = " + ".join(breakdown_parts)
    return total_cost, breakdown_str

def generate_output_for_item(item_name, Q_base, Ka, Ktr, data_materials, data_prices, data_fuel_energy, data_labor, data_rates):
    """
    Генерирует форматированный текстовый вывод для одного изделия (А или Б)
    по структуре из "Курсовая часть 1.docx".
    """
    output = f"Изделие {item_name}\n"
    Q_corrected = int(Q_base * Ka)

    # --- 1. Основные материалы ---
    output += "1. Основные материалы за вычетом обортных отходов\n"
    output += "Сом = ( Нмi * Цмi * Ктр - Н0i*Ц0i) (1.1)\n"
    output += "где Цмi - цена i -го вида материала, руб / т;\n"
    output += "Ктр - коэффициент, который учитывает транспортно-заготовительные расходы (принимается в интервале значений 1,1 - 1,15);\n"
    output += "Ноi - норма отходов, т;\n"
    output += "Цоi - цена отходов, руб /т;\n"
    output += "m - число наименований материалов.\n"

    # Определяем, что входит в "Основные материалы" (п.1)
    main_materials_names = ["стальной прокат", "трубы стальные", "прокат цветных металлов", "другие материалы"]
    materials_for_main = {k: v for k, v in data_materials.items() if k in main_materials_names}

    # Рассчитываем стоимость основных материалов для единицы
    total_main_mat_cost_unit, breakdown_main = calculate_costs_split(materials_for_main, data_prices, Ktr, item_name)
    total_main_mat_cost_annual = total_main_mat_cost_unit * Q_corrected

    output += f"На единицу:\n"
    output += f"Сом i = {breakdown_main} = {format_cost(total_main_mat_cost_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Сом = Сом i * Q = {format_cost(total_main_mat_cost_unit)} * {Q_corrected} = {format_cost_annual(total_main_mat_cost_annual)}\n\n"

    # --- 2. Покупные полуфабрикаты и комплектующие ---
    output += "2. Расходы на покупные полуфабрикаты (СПФ) и комплектующие изделия ( Ском ).\n"
    output += "Расходы на покупные полуфабрикаты рассчитываются по вышеприведенной формуле . Стоимость комплектующих изделий определяется суммированием расходов на приобретение составных частей для производства продукции согласно данным дополнения 3.\n"
    output += "С пф = Σ ( Нмi * Цмi * Ктр - Н0iЦ0i) (1.3)\n"

    # Определяем, что входит в "Покупные ПФ+Комплектующие" (п.2)
    materials_for_purchased = {k: v for k, v in data_materials.items() if k not in main_materials_names}

    # Рассчитываем стоимость ПФ+Комплектующих для единицы
    total_purchased_comp_cost_unit, breakdown_purchased = calculate_costs_split(materials_for_purchased, data_prices, Ktr, item_name)
    total_purchased_comp_cost_annual = total_purchased_comp_cost_unit * Q_corrected

    output += f"На единицу:\n"
    output += f"СПФ+Ском = {breakdown_purchased} = {format_cost(total_purchased_comp_cost_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"( СПФ+Ском ) * Q = {format_cost(total_purchased_comp_cost_unit)} * {Q_corrected} = {format_cost_annual(total_purchased_comp_cost_annual)}\n\n"

    # --- 3. Топливо и энергия ---
    fuel_energy_percentage = data_fuel_energy[item_name]
    # !!! ИСПРАВЛЕНИЕ: Передаем СУММУ всех материальных расходов (основных + ПФ+Комплектующих)
    total_material_costs_unit = total_main_mat_cost_unit + total_purchased_comp_cost_unit
    fuel_energy_unit = calculate_fuel_energy_costs(total_material_costs_unit, fuel_energy_percentage)
    fuel_energy_annual = fuel_energy_unit * Q_corrected

    output += "3. Топливо и энергия на технологические потребности\n"
    output += f"На единицу:\n"
    # Выводим формулу с подстановкой значений
    output += f"Стэ = (Сом + Спф+Ском) * ({fuel_energy_percentage}/(100-{fuel_energy_percentage})) = ({format_cost(total_main_mat_cost_unit)} + {format_cost(total_purchased_comp_cost_unit)}) * {fuel_energy_percentage}/(100-{fuel_energy_percentage}) = {format_cost(fuel_energy_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Стэ = {format_cost(fuel_energy_unit)} * {Q_corrected} = {format_cost_annual(fuel_energy_annual)}\n\n"

def generate_structure_table(structure_data_A, structure_data_B):
    """Генерирует итоговую таблицу структуры себестоимости."""
    output = "\n--- Итоговая таблица ---\n"
    output += "| Наименование статей расходов | Изделие А | | Изделие Б | | Себестоимость годового выпуска продукции, тыс.руб. | Структура расходов,% |\n"
    output += "| | на единицу, руб | на годовой выпуск, тыс.руб. | на едину, руб | на годовой выпуск, тыс.руб. | | |\n"
    output += "| --- | --- | --- | --- | --- | --- | --- |\n"

    total_A_annual = structure_data_A["Годовой_Сп"] / 1000 # в тыс.руб
    total_B_annual = structure_data_B["Годовой_Сп"] / 1000 # в тыс.руб
    total_combined_annual = total_A_annual + total_B_annual

    # 1. Основные материалы
    output += f"| 1. Основные материалы за вычетом возвратных отходов | {structure_data_A['Единица_Сом']:.2f} | {structure_data_A['Годовой_Сом'] / 1000:.2f} | {structure_data_B['Единица_Сом']:.2f} | {structure_data_B['Годовой_Сом'] / 1000:.2f} | | |\n"
    # 2. Покупные ПФ и комплектующие
    output += f"| 2. Покупные полуфабрикаты и комплектующие изделия | {structure_data_A['Единица_Спф_Ском']:.2f} | {structure_data_A['Годовой_Спф_Ском'] / 1000:.2f} | {structure_data_B['Единица_Спф_Ском']:.2f} | {structure_data_B['Годовой_Спф_Ском'] / 1000:.2f} | | |\n"
    # 3. Топливо и энергия
    output += f"| 3. Топливо и энергия на технологические потребности | {structure_data_A['Единица_Стэ']:.2f} | {structure_data_A['Годовой_Стэ'] / 1000:.2f} | {structure_data_B['Единица_Стэ']:.2f} | {structure_data_B['Годовой_Стэ'] / 1000:.2f} | | |\n"
    # 4. Основная з/п
    output += f"| 4. Основная заработная плата производственных рабочих | {structure_data_A['Единица_Сосн']:.2f} | {structure_data_A['Годовой_Сосн'] / 1000:.2f} | {structure_data_B['Единица_Сосн']:.2f} | {structure_data_B['Годовой_Сосн'] / 1000:.2f} | | |\n"
    # 5. Доп. з/п
    output += f"| 5. Дополнительная заработная плата производственных рабочих | {structure_data_A['Единица_Сдоп']:.2f} | {structure_data_A['Годовой_Сдоп'] / 1000:.2f} | {structure_data_B['Единица_Сдоп']:.2f} | {structure_data_B['Годовой_Сдоп'] / 1000:.2f} | | |\n"
    # 6. Отчисления
    output += f"| 6. Отчисление в фонды социальных мероприятий | {structure_data_A['Единица_Ссоц']:.2f} | {structure_data_A['Годовой_Ссоц'] / 1000:.2f} | {structure_data_B['Единица_Ссоц']:.2f} | {structure_data_B['Годовой_Ссоц'] / 1000:.2f} | | |\n"
    # 7. РСЭО
    output += f"| 7. Расходы по содержанию и эксплуатации оборудования | {structure_data_A['Единица_Рсэо']:.2f} | {structure_data_A['Годовой_Рсэо'] / 1000:.2f} | {structure_data_B['Единица_Рсэо']:.2f} | {structure_data_B['Годовой_Рсэо'] / 1000:.2f} | | |\n"
    # 8. ОПР
    output += f"| 8. Общепроизводственные расходы | {structure_data_A['Единица_Роп']:.2f} | {structure_data_A['Годовой_Роп'] / 1000:.2f} | {structure_data_B['Единица_Роп']:.2f} | {structure_data_B['Годовой_Роп'] / 1000:.2f} | | |\n"
    # 9. ОХР
    output += f"| 9. Общехозяйственные расходы | {structure_data_A['Единица_Рох']:.2f} | {structure_data_A['Годовой_Рох'] / 1000:.2f} | {structure_data_B['Единица_Рох']:.2f} | {structure_data_B['Годовой_Рох'] / 1000:.2f} | | |\n"
    # Всего производственная
    output += f"| ВСЕГО производственная себестоимость | {structure_data_A['Единица_Спр']:.2f} | {structure_data_A['Годовой_Спр'] / 1000:.2f} | {structure_data_B['Единица_Спр']:.2f} | {structure_data_B['Годовой_Спр'] / 1000:.2f} | | |\n"
    # 10. Внепроизводственные
    output += f"| 10. Внепроизводственные расходы | {structure_data_A['Единица_Свп']:.2f} | {structure_data_A['Годовой_Свп'] / 1000:.2f} | {structure_data_B['Единица_Свп']:.2f} | {structure_data_B['Годовой_Свп'] / 1000:.2f} | | |\n"
    # Всего полная
    output += f"| ВСЕГО полная (коммерческая) себестоимость | {structure_data_A['Единица_Сп']:.2f} | {total_A_annual:.2f} | {structure_data_B['Единица_Сп']:.2f} | {total_B_annual:.2f} | {total_combined_annual:.2f} | | \n"
    # Оптовая цена
    output += f"| Оптовая (отпускная) цена | {structure_data_A['Оптовая_цена']:.2f} | | {structure_data_B['Оптовая_цена']:.2f} | | | | \n\n"

    # Структура расходов (%)
    output += "--- Структура расходов (в % от общей годовой себестоимости) ---\n"
    output += "| Наименование статей расходов | Изделие А | Изделие Б |\n"
    output += "| --- | --- | --- |\n"
    # 1. Основные материалы
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Сом'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Сом'] / 1000, total_combined_annual)
    output += f"| 1. Основные материалы за вычетом возвратных отходов | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # 2. Покупные ПФ и комплектующие
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Спф_Ском'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Спф_Ском'] / 1000, total_combined_annual)
    output += f"| 2. Покупные полуфабрикаты и комплектующие изделия | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # 3. Топливо и энергия
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Стэ'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Стэ'] / 1000, total_combined_annual)
    output += f"| 3. Топливо и энергия на технологические потребности | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # 4. Основная з/п
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Сосн'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Сосн'] / 1000, total_combined_annual)
    output += f"| 4. Основная заработная плата производственных рабочих | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # 5. Доп. з/п
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Сдоп'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Сдоп'] / 1000, total_combined_annual)
    output += f"| 5. Дополнительная заработная плата производственных рабочих | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # 6. Отчисления
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Ссоц'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Ссоц'] / 1000, total_combined_annual)
    output += f"| 6. Отчисление в фонды социальных мероприятий | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # 7. РСЭО
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Рсэо'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Рсэо'] / 1000, total_combined_annual)
    output += f"| 7. Расходы по содержанию и эксплуатации оборудования | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # 8. ОПР
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Роп'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Роп'] / 1000, total_combined_annual)
    output += f"| 8. Общепроизводственные расходы | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # 9. ОХР
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Рох'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Рох'] / 1000, total_combined_annual)
    output += f"| 9. Общехозяйственные расходы | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # Всего производственная
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Спр'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Спр'] / 1000, total_combined_annual)
    output += f"| ВСЕГО производственная себестоимость | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # 10. Внепроизводственные
    perc_A = calculate_structure_percentage(structure_data_A['Годовой_Свп'] / 1000, total_combined_annual)
    perc_B = calculate_structure_percentage(structure_data_B['Годовой_Свп'] / 1000, total_combined_annual)
    output += f"| 10. Внепроизводственные расходы | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"
    # Всего полная (должна быть 100%)
    perc_A = calculate_structure_percentage(total_A_annual, total_combined_annual)
    perc_B = calculate_structure_percentage(total_B_annual, total_combined_annual)
    output += f"| ВСЕГО полная (коммерческая) себестоимость | {format_percentage(perc_A)} | {format_percentage(perc_B)} |\n"

    return output


def generate_structure_table(structure_data_A, structure_data_B):
    """Генерирует итоговую таблицу структуры себестоимости в читаемом формате."""
    output = "\n--- Итоговая таблица ---\n"

    # Определяем заголовки и их ширину
    headers = [
        ("Наименование статей расходов", 45),
        ("Изделие А на единицу, руб", 20),
        ("Изделие А на годовой выпуск, тыс.руб.", 25),
        ("Изделие Б на единицу, руб", 20),
        ("Изделие Б на годовой выпуск, тыс.руб.", 25),
        ("Себестоимость годового выпуска продукции, тыс.руб.", 35),
        ("Структура расходов,%", 20)
    ]

    # Формируем строку заголовков
    header_row = "|"
    for header_text, width in headers:
        header_row += f" {header_text:<{width}} |"
    output += header_row + "\n"

    # Формируем разделительную линию
    separator_row = "|"
    for _, width in headers:
        separator_row += f"{'-' * (width + 2)}|"
    output += separator_row + "\n"

    total_A_annual = structure_data_A["Годовой_Сп"] / 1000 # в тыс.руб
    total_B_annual = structure_data_B["Годовой_Сп"] / 1000 # в тыс.руб
    total_combined_annual = total_A_annual + total_B_annual

    # Данные для строк таблицы
    rows = [
        ("1. Основные материалы за вычетом возвратных отходов", "Единица_Сом", "Годовой_Сом"),
        ("2. Покупные полуфабрикаты и комплектующие изделия", "Единица_Спф_Ском", "Годовой_Спф_Ском"),
        ("3. Топливо и энергия на технологические потребности", "Единица_Стэ", "Годовой_Стэ"),
        ("4. Основная заработная плата производственных рабочих", "Единица_Сосн", "Годовой_Сосн"),
        ("5. Дополнительная заработная плата производственных рабочих", "Единица_Сдоп", "Годовой_Сдоп"),
        ("6. Отчисление в фонды социальных мероприятий", "Единица_Ссоц", "Годовой_Ссоц"),
        ("7. Расходы по содержанию и эксплуатации оборудования", "Единица_Рсэо", "Годовой_Рсэо"),
        ("8. Общепроизводственные расходы", "Единица_Роп", "Годовой_Роп"),
        ("9. Общехозяйственные расходы", "Единица_Рох", "Годовой_Рох"),
        ("ВСЕГО производственная себестоимость", "Единица_Спр", "Годовой_Спр"),
        ("10. Внепроизводственные расходы", "Единица_Свп", "Годовой_Свп"),
        ("ВСЕГО полная (коммерческая) себестоимость", "Единица_Сп", "Годовой_Сп"),
        ("Оптовая (отпускная) цена", "Оптовая_цена", None) # Для оптовой цены нет годового выпуска
    ]

    for row_name, unit_key, annual_key in rows:
        # Значения для изделия А
        a_unit_val = structure_data_A[unit_key]
        if annual_key is not None:
            a_annual_val = structure_data_A[annual_key] / 1000 # в тыс.руб
        else:
            a_annual_val = None

        # Значения для изделия Б
        b_unit_val = structure_data_B[unit_key]
        if annual_key is not None:
            b_annual_val = structure_data_B[annual_key] / 1000 # в тыс.руб
        else:
            b_annual_val = None

        # Сумма годового выпуска (для строк, где есть annual_key)
        combined_annual_val = None
        if annual_key is not None:
            combined_annual_val = (structure_data_A[annual_key] + structure_data_B[annual_key]) / 1000 # в тыс.руб

        # Удельный вес (структура расходов)
        perc_A = 0
        perc_B = 0
        if annual_key is not None and total_combined_annual > 0:
            perc_A = calculate_structure_percentage(structure_data_A[annual_key] / 1000, total_combined_annual)
            perc_B = calculate_structure_percentage(structure_data_B[annual_key] / 1000, total_combined_annual)

        # Формируем строку данных
        data_row = "|"
        data_row += f" {row_name:<45} |"
        data_row += f" {a_unit_val:>18.2f} |"
        if a_annual_val is not None:
            data_row += f" {a_annual_val:>23.2f} |"
        else:
            data_row += f" {'':>23} |"
        data_row += f" {b_unit_val:>18.2f} |"
        if b_annual_val is not None:
            data_row += f" {b_annual_val:>23.2f} |"
        else:
            data_row += f" {'':>23} |"
        if combined_annual_val is not None:
            data_row += f" {combined_annual_val:>33.2f} |"
        else:
            data_row += f" {'':>33} |"
        if annual_key is not None:
            data_row += f" {perc_A:>17.2f}% | {perc_B:>17.2f}% |"
        else:
            data_row += f" {'':>17} | {'':>17} |"

        output += data_row + "\n"

    return output

def prepare_data_with_coefficients(data_materials, data_labor, data_volume_base, Ka, Kj):
    """
    Подготавливает данные, применяя коэффициенты Kj и Ka.
    Kj применяется к нормам расхода/отходов и трудоемкости.
    Ka применяется к базовому объему.
    """
    import copy
    prepared_materials = copy.deepcopy(data_materials)
    prepared_labor = copy.deepcopy(data_labor)
    prepared_volume = {k: v * Ka for k, v in data_volume_base.items()}

    # Применяем Kj к нормам расхода и отходов
    for comp_name, comp_info in prepared_materials.items():
        if isinstance(comp_info, dict) and 'rasxod' in comp_info:
            for item in ['A', 'B']:
                if item in comp_info:
                    comp_info[item]['rasxod'] *= Kj
                    comp_info[item]['otxod'] *= Kj

    # Применяем Kj к трудоемкости
    for item in ['A', 'B']:
        if item in prepared_labor['labor_hours']:
            prepared_labor['labor_hours'][item] *= Kj

    return prepared_materials, prepared_labor, prepared_volume

def generate_full_output(Q_base_data, Ka, Kj, Ktr, materials_main, materials_purchased, prices, fuel_energy, labor, rates):
    """
    Основная функция для генерации полного вывода расчета для изделий А и Б.
    """
    # Подготовка данных с учетом Kj (и Ka для объема)
    prepared_materials_main, prepared_labor, prepared_volume = prepare_data_with_coefficients(
        materials_main, labor, Q_base_data, Ka, Kj
    )
    prepared_materials_purchased, _, _ = prepare_data_with_coefficients(
        materials_purchased, {"labor_hours": {"A": 1, "B": 1}}, {"A": 1, "B": 1}, 1, Kj
    )
    # Объединяем подготовленные материалы
    combined_materials = {**prepared_materials_main, **prepared_materials_purchased}

    output = "1.1 Расчет себестоимости и цены изделий\n\n"
    structure_data_A = None
    structure_data_B = None

    for item in ['A', 'B']:
        Q_item = prepared_volume[item] # Используем подготовленный объем
        item_output, item_structure = generate_output_for_item(
            item, Q_item, 1, Ktr, # Ka=1, потому что объем Q_item уже скорректирован
            combined_materials, prices, fuel_energy, prepared_labor, rates
        )
        output += item_output
        if item == 'A':
            structure_data_A = item_structure
        else:
            structure_data_B = item_structure

    # Генерация таблицы структуры
    # if structure_data_A and structure_data_B:
    #     output += generate_structure_table(structure_data_A, structure_data_B)

    return output


def generate_structure_table_csv(structure_data_A, structure_data_B):
    """Генерирует итоговую таблицу структуры себестоимости в формате CSV."""
    output = io.StringIO() # Используем StringIO как "файл в памяти"
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    # Определяем заголовки
    headers = [
        "Наименование статей расходов",
        "Изделие А на единицу, руб",
        "Изделие А на годовой выпуск, тыс.руб.",
        "Изделие Б на единицу, руб",
        "Изделие Б на годовой выпуск, тыс.руб.",
        "Себестоимость годового выпуска продукции, тыс.руб.",
        "Структура расходов,%"
    ]

    writer.writerow(headers)

    # Общая годовая себестоимость для расчета структуры
    total_A_annual = structure_data_A["Годовой_Сп"] / 1000 # в тыс.руб
    total_B_annual = structure_data_B["Годовой_Сп"] / 1000 # в тыс.руб
    total_combined_annual = total_A_annual + total_B_annual

    # Данные для строк таблицы
    # Ключи в словарях structure_data_A и structure_data_B
    # соответствуют статьям: "Единица_Сом", "Годовой_Сом", "Единица_Спф_Ском", "Годовой_Спф_Ском", ...
    # Нам нужно сопоставить наименование строки с ключом.
    # Повторим логику из generate_output_for_item для сопоставления
    # Основные материалы (только для п.1) - это сумма "стальной прокат", "трубы", "прокат цв.м.", "другие м." из п.1
    # Покупные ПФ+Комплектующие (для п.2) - это "отливки", "комплектующие" из п.2
    # Остальные статьи берутся напрямую из расчетов, например, "Единица_Стэ", "Годовой_Стэ" и т.д.

    # Мы можем использовать ключи из structure_data_A/B, но сопоставим их с наименованиями строк
    # или создать список сопоставлений.
    # Лучше создать список кортежей (наименование, ключ_единица, ключ_годовой)
    # где ключ_годовой может быть None, если строки нет (например, для оптовой цены)
    # Но в structure_data уже есть "Единица_Сом" и "Годовой_Сом", где "Сом" - это сумма *всех* основных материалов.
    # "Единица_Спф_Ском", "Годовой_Спф_Ском" - сумма *всех* покупных ПФ и комплектующих.
    # Поэтому сопоставление будет таким:
    rows = [
        ("1. Основные материалы за вычетом возвратных отходов", "Единица_Сом", "Годовой_Сом"),
        ("2. Покупные полуфабрикаты и комплектующие изделия", "Единица_Спф_Ском", "Годовой_Спф_Ском"),
        ("3. Топливо и энергия на технологические потребности", "Единица_Стэ", "Годовой_Стэ"),
        ("4. Основная заработная плата производственных рабочих", "Единица_Сосн", "Годовой_Сосн"),
        ("5. Дополнительная заработная плата производственных рабочих", "Единица_Сдоп", "Годовой_Сдоп"),
        ("6. Отчисление в фонды социальных мероприятий", "Единица_Ссоц", "Годовой_Ссоц"),
        ("7. Расходы по содержанию и эксплуатации оборудования", "Единица_Рсэо", "Годовой_Рсэо"),
        ("8. Общепроизводственные расходы", "Единица_Роп", "Годовой_Роп"),
        ("9. Общехозяйственные расходы", "Единица_Рох", "Годовой_Рох"),
        ("ВСЕГО производственная себестоимость", "Единица_Спр", "Годовой_Спр"),
        ("10. Внепроизводственные расходы", "Единица_Свп", "Годовой_Свп"),
        ("ВСЕГО полная (коммерческая) себестоимость", "Единица_Сп", "Годовой_Сп"),
        ("Оптовая (отпускная) цена", "Оптовая_цена", None) # Для оптовой цены нет годового выпуска
    ]

    for row_name, unit_key, annual_key in rows:
        # Значения для изделия А
        a_unit_val = structure_data_A[unit_key]
        if annual_key is not None:
            a_annual_val = structure_data_A[annual_key] / 1000 # в тыс.руб
        else:
            a_annual_val = None

        # Значения для изделия Б
        b_unit_val = structure_data_B[unit_key]
        if annual_key is not None:
            b_annual_val = structure_data_B[annual_key] / 1000 # в тыс.руб
        else:
            b_annual_val = None

        # Сумма годового выпуска для этой строки (А + Б)
        combined_annual_val = None
        if annual_key is not None:
            combined_annual_val = (structure_data_A[annual_key] + structure_data_B[annual_key]) / 1000 # в тыс.руб

        # Удельный вес (структура расходов) - рассчитывается от общей себестоимости ВСЕЙ НОМЕНКЛАТУРЫ
        perc_combined = 0
        if annual_key is not None and total_combined_annual > 0: # Только для статей с годовым значением и если общая себестоимость > 0
            perc_combined = calculate_structure_percentage(combined_annual_val, total_combined_annual) # combined_annual_val уже в тыс.руб
        elif annual_key is None: # Для строки "Оптовая цена" структура не рассчитывается
             perc_combined = "" # или оставить пустым

        # Формируем строку данных
        row_data = [
            row_name,
            f"{a_unit_val:.2f}",
            f"{a_annual_val:.2f}" if a_annual_val is not None else "",
            f"{b_unit_val:.2f}",
            f"{b_annual_val:.2f}" if b_annual_val is not None else "",
            f"{combined_annual_val:.2f}" if combined_annual_val is not None else "",
            f"{perc_combined:.2f}%" if isinstance(perc_combined, (int, float)) else perc_combined # Форматируем процент, если это число
        ]

        writer.writerow(row_data)

    csv_content = output.getvalue()
    output.close()
    return csv_content

# --- 4. Основная логика скрипта ---
# (См. пункт 4 плана)

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
# Используем Ka = 1.04, как в описании к файлу "Курсовая часть 1.docx" и для получения объемов 102 и 68
Ka_input = 1.04 # Коэффициент для корректировки объема
Kj_input = 0.95 # Пример
Ktr_input = 1.15 # Пример из расчета

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

print("Расчет по статьям (как в файле 'Курсовая часть 1.docx'):")
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

# --- Конец скрипта ---