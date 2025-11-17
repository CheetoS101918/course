import csv
import io
import json
from typing import List, Dict, Any


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
    return round(fuel_energy_cost, 2)

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
    return round(wage, 2)

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
    return round(additional_wage, 2)

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
    return round(social_contributions, 2)

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
    return round(overhead_cost, 2)

def calculate_production_cost(material_costs, fuel_energy, purchased_comp_cost, basic_wage, additional_wage, social_contributions, rsuo_costs, opr_costs, oxr_costs):
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
    production_cost = (material_costs + purchased_comp_cost + fuel_energy + basic_wage + additional_wage +
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
    total_material_costs_unit = round(total_main_mat_cost_unit + total_purchased_comp_cost_unit, 2)
    fuel_energy_unit = calculate_fuel_energy_costs(total_material_costs_unit, fuel_energy_percentage)
    fuel_energy_annual = fuel_energy_unit * Q_corrected

    output += "3. Топливо и энергия на технологические потребности\n"
    output += f"На единицу:\n"
    # Выводим формулу с подстановкой значений
    output += f"Стэ = (Сом + Спф+Ском) * ({fuel_energy_percentage}/(100-{fuel_energy_percentage})) = ({format_cost(total_main_mat_cost_unit)} + {format_cost(total_purchased_comp_cost_unit)}) * {fuel_energy_percentage}/(100-{fuel_energy_percentage}) = {format_cost(fuel_energy_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Стэ = {format_cost(fuel_energy_unit)} * {Q_corrected} = {format_cost_annual(fuel_energy_annual)}\n\n"

    # --- 4. Основная заработная плата ---
    labor_hours = data_labor['labor_hours'][item_name]
    hourly_rate = data_labor['hourly_rate'][item_name]
    basic_wage_unit = calculate_basic_wage(labor_hours, hourly_rate)
    basic_wage_annual = basic_wage_unit * Q_corrected

    output += "4. Основная заработная плата производственных рабочих\n"
    output += f"На единицу:\n"
    output += f"Сосн = t * Т = {labor_hours} * {hourly_rate} = {format_cost(basic_wage_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Сосн = {format_cost(basic_wage_unit)} * {Q_corrected} = {format_cost_annual(basic_wage_annual)}\n\n"

    # --- 5. Дополнительная заработная плата ---
    additional_wage_percentage = data_rates["доп_зарплата"]
    additional_wage_unit = calculate_additional_wage(basic_wage_unit, additional_wage_percentage)
    additional_wage_annual = additional_wage_unit * Q_corrected

    output += "5. Дополнительная заработная плата производственных рабочих\n"
    output += f"На единицу:\n"
    output += f"Сдоп = Сосн * ({additional_wage_percentage}/100) = {format_cost(basic_wage_unit)} * {additional_wage_percentage/100} = {format_cost(additional_wage_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Сдоп = {format_cost(additional_wage_unit)} * {Q_corrected} = {format_cost_annual(additional_wage_annual)}\n\n"

    # --- 6. Отчисления в фонды социальных мероприятий ---
    social_percentage = data_rates["отчисления"]
    social_contributions_unit = calculate_social_contributions(basic_wage_unit, additional_wage_unit, social_percentage)
    social_contributions_annual = social_contributions_unit * Q_corrected

    output += "6. Отчисление в фонды социальных мероприятий\n"
    output += f"На единицу:\n"
    output += f"Ссоц = (Сосн + Сдоп) * ({social_percentage}/100) = ({format_cost(basic_wage_unit, '')} + {format_cost(additional_wage_unit, '')}) * {social_percentage/100} = {format_cost(social_contributions_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Ссоц = {format_cost(social_contributions_unit)} * {Q_corrected} = {format_cost_annual(social_contributions_annual)}\n\n"

    # --- 7. РСЭО ---
    rsuo_percentage = data_rates["РСЭО"]
    rsuo_unit = calculate_overhead_costs(basic_wage_unit, rsuo_percentage)
    rsuo_annual = rsuo_unit * Q_corrected

    output += "7. Расходы на содержание и эксплуатацию оборудования\n"
    output += f"На единицу:\n"
    output += f"Рсэо = Сосн * ({rsuo_percentage}/100) = {format_cost(basic_wage_unit)} * {rsuo_percentage/100} = {format_cost(rsuo_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Рсэо = {format_cost(rsuo_unit)} * {Q_corrected} = {format_cost_annual(rsuo_annual)}\n\n"

    # --- 8. ОПР ---
    opr_percentage = data_rates["ОПР"]
    opr_unit = calculate_overhead_costs(basic_wage_unit, opr_percentage)
    opr_annual = opr_unit * Q_corrected

    output += "8. Общепроизводственные расходы\n"
    output += f"На единицу:\n"
    output += f"Роп = Сосн * ({opr_percentage}/100) = {format_cost(basic_wage_unit)} * {opr_percentage/100} = {format_cost(opr_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Роп = {format_cost(opr_unit)} * {Q_corrected} = {format_cost_annual(opr_annual)}\n\n"

    # --- 9. ОХР ---
    oxr_percentage = data_rates["ОХР"]
    oxr_unit = calculate_overhead_costs(basic_wage_unit, oxr_percentage)
    oxr_annual = oxr_unit * Q_corrected

    output += "9. Общехозяйственные расходы\n"
    output += f"На единицу:\n"
    output += f"Рох = Сосн * ({oxr_percentage}/100) = {format_cost(basic_wage_unit)} * {oxr_percentage/100} = {format_cost(oxr_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Рох = {format_cost(oxr_unit)} * {Q_corrected} = {format_cost_annual(oxr_annual)}\n\n"

    # --- Производственная себестоимость ---
    production_cost_unit = calculate_production_cost(
        total_material_costs_unit,  total_purchased_comp_cost_unit, fuel_energy_unit, basic_wage_unit,
        additional_wage_unit, social_contributions_unit, rsuo_unit, opr_unit, oxr_unit
    )
    production_cost_annual = production_cost_unit * Q_corrected

    output += "ВСЕГО производственная себестоимость\n"
    output += f"На единицу:\n"
    output += f"Спр = Сом + (Спф+Ском) + Впер + Сосн + Сдоп + Ссоц + Рсэо + Роп + Рох = {format_cost(total_material_costs_unit)} + {fuel_energy_unit:.2f} + {basic_wage_unit:.2f} + {additional_wage_unit:.2f} + {social_contributions_unit:.2f} + {rsuo_unit:.2f} + {opr_unit:.2f} + {oxr_unit:.2f} = {format_cost(production_cost_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Спр = {format_cost(production_cost_unit)} * {Q_corrected} = {format_cost_annual(production_cost_annual)}\n\n"

    # --- 10. Внепроизводственные расходы ---
    selling_percentage = data_rates["ВПР"]
    selling_cost_unit = calculate_selling_cost(production_cost_unit, selling_percentage)
    selling_cost_annual = selling_cost_unit * Q_corrected

    output += "10. Внепроизводственные расходы\n"
    output += f"На единицу:\n"
    output += f"Свп = Спр * ({selling_percentage}/100) = {format_cost(production_cost_unit)} * {selling_percentage/100} = {format_cost(selling_cost_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Свп = {format_cost(selling_cost_unit)} * {Q_corrected} = {format_cost_annual(selling_cost_annual)}\n\n"

    # --- Полная себестоимость ---
    full_cost_unit = calculate_full_cost(production_cost_unit, selling_cost_unit)
    full_cost_annual = full_cost_unit * Q_corrected

    output += "ВСЕГО полная (коммерческая) себестоимость\n"
    output += f"На единицу:\n"
    output += f"Сп = Спр + Свп = {production_cost_unit:.2f} + {selling_cost_unit:.2f} = {format_cost(full_cost_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"Сп = {format_cost(full_cost_unit)} * {Q_corrected} = {format_cost_annual(full_cost_annual)}\n\n"

    # --- 11. Прибыль ---
    profitability_percentage = data_rates["рентабельность"]
    profit_unit = calculate_profit(full_cost_unit, profitability_percentage)
    profit_annual = profit_unit * Q_corrected

    output += f"11. Прибыль\n"
    output += f"На единицу:\n"
    output += f"П = Сп * ({profitability_percentage}/100) = {format_cost(full_cost_unit)} * {profitability_percentage / 100} = {format_cost(profit_unit)}\n"
    output += f"На годовой выпуск:\n"
    output += f"П = {format_cost(profit_unit)} * {Q_corrected} = {format_cost_annual(profit_annual)}\n\n"

    # --- 12. Оптовая цена ---
    opt_price = calculate_opt_price(full_cost_unit, profit_unit)

    output += f"12. Оптовая (отпускная) цена\n"
    output += f"Цопт = Сп + П = {format_cost(full_cost_unit)} + {format_cost(profit_unit)} = {format_cost(opt_price)}\n\n"


    # --- Структура себестоимости (для таблицы) ---
    structure_data = {
        "Наименование": item_name,
        "Единица_Сом": total_main_mat_cost_unit, "Годовой_Сом": total_main_mat_cost_annual,
        "Единица_Спф_Ском": total_purchased_comp_cost_unit, "Годовой_Спф_Ском": total_purchased_comp_cost_annual,
        "Единица_Стэ": fuel_energy_unit, "Годовой_Стэ": fuel_energy_annual,
        "Единица_Сосн": basic_wage_unit, "Годовой_Сосн": basic_wage_annual,
        "Единица_Сдоп": additional_wage_unit, "Годовой_Сдоп": additional_wage_annual,
        "Единица_Ссоц": social_contributions_unit, "Годовой_Ссоц": social_contributions_annual,
        "Единица_Рсэо": rsuo_unit, "Годовой_Рсэо": rsuo_annual,
        "Единица_Роп": opr_unit, "Годовой_Роп": opr_annual,
        "Единица_Рох": oxr_unit, "Годовой_Рох": oxr_annual,
        "Единица_Спр": production_cost_unit, "Годовой_Спр": production_cost_annual,
        "Единица_Свп": selling_cost_unit, "Годовой_Свп": selling_cost_annual,
        "Единица_Сп": full_cost_unit, "Годовой_Сп": full_cost_annual,
        "Единица_Прибыль": profit_unit, "Годовой_Прибыль": profit_annual,  # Добавляем прибыль
        "Оптовая_цена": opt_price,
        "Q": Q_corrected
    }

    return output, structure_data

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
        ("11. Прибыль", "Единица_Прибыль", "Годовой_Прибыль"), # Добавляем строку "Прибыль"
        ("12. Оптовая (отпускная) цена", "Оптовая_цена", None) # Для оптовой цены нет годового выпуска
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

def prepare_data_with_coefficients(data_materials, data_labor, data_volume_base, Ka, Kj):
    """
    Подготавливает данные, применяя коэффициенты Kj и Ka.
    Kj применяется к нормам расхода/отходов и трудоемкости.
    Ka применяется к базовому объему.
    """
    import copy
    prepared_materials = copy.deepcopy(data_materials)
    prepared_labor = copy.deepcopy(data_labor)
    prepared_volume = {k: v * Ka for k, v in data_volume_base.items()} # Только Ka к объему

    # Применяем Kj к нормам расхода и отходов
    # for comp_name, comp_info in prepared_materials.items():
    #     if isinstance(comp_info, dict) and 'rasxod' in comp_info:
    #         for item in ['A', 'B']:
    #             if item in comp_info:
    #                 comp_info[item]['rasxod'] *= Kj
    #                 comp_info[item]['otxod'] *= Kj

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
    #     output += generate_structure_table_csv(structure_data_A, structure_data_B)

    return output


def calculate_profit(full_cost, profitability_percentage):
    """
    Расчет прибыли как процент от полной себестоимости.

    Args:
        full_cost (float): Полная себестоимость единицы изделия, руб.
        profitability_percentage (float): Норматив рентабельности, %.

    Returns:
        float: Прибыль на единицу изделия, руб.
    """
    profit = full_cost * (profitability_percentage / 100)
    return profit


def calculate_opt_price(full_cost, profit):
    """
    Расчет оптовой (отпускной) цены как сумма полной себестоимости и прибыли.

    Args:
        full_cost (float): Полная себестоимость единицы изделия, руб.
        profit (float): Прибыль на единицу изделия, руб.

    Returns:
        float: Оптовая цена, руб.
    """
    opt_price = full_cost + profit
    return opt_price


def calculate_product_volumes(structure_data_A, structure_data_B):
    """
    Рассчитывает объем товарной и реализованной продукции.
    Использует данные из structure_data_A и structure_data_B.
    """
    # Годовые объемы выпуска
    Q_A = structure_data_A["Q"]
    Q_B = structure_data_B["Q"]

    # Оптовые цены
    price_A = structure_data_A["Оптовая_цена"]
    price_B = structure_data_B["Оптовая_цена"]

    # Объем товарной продукции (Qт)
    Q_t = (Q_A * price_A + Q_B * price_B) / 1000 # в тыс.руб

    # Объем реализованной продукции (Qр)
    # Qн = 2% от Qт
    # Qк = 1.5% от Qт
    Q_n = Q_t * 0.02
    Q_k = Q_t * 0.015
    Q_p = Q_n + Q_t - Q_k

    return Q_t, Q_p, Q_A, Q_B, price_A, price_B


def generate_input_table_csv(materials_main, materials_purchased, prices, fuel_energy, labor, rates, volume_base, Ka, Kj, Ktr):
    """
    Генерирует CSV строку для Таблицы 1 (Исходные данные)
    """
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    # Заголовок таблицы
    writer.writerow(["№", "Показатели", "Номер дополнения", "Ед. измерения", "Изделие А", "Изделие Б"])

    # --- Структура данных для сопоставления ---
    # Сопоставляем названия из ваших словарей с описанием из таблицы методички
    # Формат: ("Описание из таблицы", "Ед. изм.", "Номер дополнения", "Ключ для A", "Ключ для B")
    # Для материалов с типом "material", ключ - это кортеж (значение_расхода, значение_отходов)
    # Для материалов с типом "fixed", ключ - это просто значение
    # Цены, топливо/энергия, трудоемкость, ставки, проценты, объемы - отдельно

    # 1. Основные материалы
    writer.writerow(["1", "Основные материалы", "2", "", "", ""])
    writer.writerow(["1.1", "Стальной прокат:", "", "", "", ""])
    steel_data = materials_main.get("стальной прокат", {})
    writer.writerow(["", "- расходы", "", "т", steel_data.get("A", {}).get("rasxod", ""), steel_data.get("B", {}).get("rasxod", "")])
    writer.writerow(["", "- отходы", "", "т", steel_data.get("A", {}).get("otxod", ""), steel_data.get("B", {}).get("otxod", "")])

    writer.writerow(["1.2", "Трубы стальные:", "", "", "", ""])
    pipes_data = materials_main.get("трубы стальные", {})
    writer.writerow(["", "- расходы", "", "т", pipes_data.get("A", {}).get("rasxod", ""), pipes_data.get("B", {}).get("rasxod", "")])
    writer.writerow(["", "- отходы", "", "т", pipes_data.get("A", {}).get("otxod", ""), pipes_data.get("B", {}).get("otxod", "")])

    writer.writerow(["1.3", "Прокат цветных металлов", "", "руб", materials_main.get("прокат цветных металлов", {}).get("A"), materials_main.get("прокат цветных металлов", {}).get("B")])
    writer.writerow(["1.4", "Другие материалы", "", "руб", materials_main.get("другие материалы", {}).get("A"), materials_main.get("другие материалы", {}).get("B")])

    # 2. Покупные полуфабрикаты (отливки)
    writer.writerow(["2", "Покупные полуфабрикаты (отливки):", "2", "", "", ""])
    writer.writerow(["2.1", "черных металлов", "", "", "", ""])
    cast_iron_data = materials_purchased.get("отливки черных металлов", {})
    writer.writerow(["", "- расходы", "", "т", cast_iron_data.get("A", {}).get("rasxod", ""), cast_iron_data.get("B", {}).get("rasxod", "")])
    writer.writerow(["", "- отходы", "", "т", cast_iron_data.get("A", {}).get("otxod", ""), cast_iron_data.get("B", {}).get("otxod", "")])

    writer.writerow(["2.2", "цветных металлов", "", "", "", ""])
    cast_alloy_data = materials_purchased.get("отливки цветных металлов", {})
    writer.writerow(["", "- расходы", "", "т", cast_alloy_data.get("A", {}).get("rasxod", ""), cast_alloy_data.get("B", {}).get("rasxod", "")])
    writer.writerow(["", "- отходы", "", "т", cast_alloy_data.get("A", {}).get("otxod", ""), cast_alloy_data.get("B", {}).get("otxod", "")])

    # 3. Покупные комплектующие изделия
    writer.writerow(["3", "покупные комплектующие изделия", "3", "руб", materials_purchased.get("покупные комплектующие изделия", {}).get("A"), materials_purchased.get("покупные комплектующие изделия", {}).get("B")])

    # 4. Цены
    writer.writerow(["4", "Цена стального проката", "4", "руб /т", prices.get("стальной прокат_материал"), prices.get("стальной прокат_материал")])
    writer.writerow(["5", "Цена стальных труб", "4", "руб /т", prices.get("трубы стальные_материал"), prices.get("трубы стальные_материал")])
    writer.writerow(["6", "Цена отливок:", "4", "", "", ""])
    writer.writerow(["", "-черных металлов", "", "руб /т", prices.get("отливки черных металлов_материал"), prices.get("отливки черных металлов_материал")])
    writer.writerow(["", "-цветных металлов", "", "руб /т", prices.get("отливки цветных металлов_материал"), prices.get("отливки цветных металлов_материал")])

    # 7. Цены отходов
    writer.writerow(["7", "Цена отходов:", "4", "", "", ""])
    writer.writerow(["", "-стального проката", "", "руб /т", prices.get("стальной прокат_отходы"), prices.get("стальной прокат_отходы")])
    writer.writerow(["", "-труб стальных", "", "руб /т", prices.get("трубы стальные_отходы"), prices.get("трубы стальные_отходы")])
    writer.writerow(["", "-отливок черных металлов", "", "руб /т", prices.get("отливки черных металлов_отходы"), prices.get("отливки черных металлов_отходы")])
    writer.writerow(["", "-отливок цветных металлов", "", "руб /т", prices.get("отливки цветных металлов_отходы"), prices.get("отливки цветных металлов_отходы")])

    # 8. Топливо и энергия
    writer.writerow(["8", "Топливо и энергия на технологические потребности", "5", "%", fuel_energy.get("A"), fuel_energy.get("B")])

    # 9. Суммарная трудоемкость
    writer.writerow(["9", "Суммарная трудоемкость изделия", "6", "н-час", int(labor.get("labor_hours", {}).get("A") * Kj), int(labor.get("labor_hours", {}).get("B") * Kj)])

    # 10. Часовая тарифная ставка
    writer.writerow(["10", "Часовая тарифная ставка", "6", "руб", labor.get("hourly_rate", {}).get("A"), labor.get("hourly_rate", {}).get("B")])

    # 11. Дополнительная зарплата
    writer.writerow(["11", "Дополнительная зарплата", "7", "%", rates.get("доп_зарплата"), rates.get("доп_зарплата")])

    # 12. Отчисление на социальное страхование
    writer.writerow(["12", "Отчисление на социальное страхование", "7", "%", rates.get("отчисления"), rates.get("отчисления")])

    # 13. РСЭО
    writer.writerow(["13", "Расходы на содержание и эксплуатацию оборудования", "7", "%", rates.get("РСЭО"), rates.get("РСЭО")])

    # 14. ОПР
    writer.writerow(["14", "Общепроизводственные расходы", "7", "%", rates.get("ОПР"), rates.get("ОПР")])

    # 15. ОХР
    writer.writerow(["15", "Общехозяйственные расходы", "7", "%", rates.get("ОХР"), rates.get("ОХР")])

    # 16. ВПР
    writer.writerow(["16", "Внепроизводственные расходы", "7", "%", rates.get("ВПР"), rates.get("ВПР")])

    # 17. Норматив рентабельности
    writer.writerow(["17", "Норматив рентабельности к себестоимости", "7", "%", rates.get("рентабельность"), rates.get("рентабельность")])

    # 18. Годовой объем производства (базовый)
    writer.writerow(["18", "Годовой объем производства", "1", "шт", int(volume_base.get("A") * Ka), int(volume_base.get("B") * Ka)])

    csv_content = output.getvalue()
    output.close()
    return csv_content


def save_structure_table_to_json(structure_data_A, structure_data_B, filename="sebestoimost_structure.json"):
    """
    Сохраняет итоговую таблицу структуры себестоимости в формате JSON.

    Args:
        structure_data_A (dict): Словарь с данными для изделия А (из generate_output_for_item).
        structure_data_B (dict): Словарь с данными для изделия Б (из generate_output_for_item).
        filename (str): Имя файла для сохранения JSON (по умолчанию "sebestoimost_structure.json").
    """
    # Общая годовая себестоимость для расчета структуры
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
        ("11. Прибыль", "Единица_Прибыль", "Годовой_Прибыль"),
        ("12. Оптовая (отпускная) цена", "Оптовая_цена", None) # Для оптовой цены нет годового выпуска
    ]

    # Список для хранения данных JSON
    json_data = []

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
            # Используем вашу функцию calculate_structure_percentage
            perc_combined = calculate_structure_percentage(combined_annual_val, total_combined_annual) # combined_annual_val уже в тыс.руб
        elif annual_key is None: # Для строки "Оптовая цена" структура не рассчитывается
             perc_combined = None # или оставить пустым

        # Формируем словарь данных JSON
        row_data_json = {
            "Наименование статей расходов": row_name,
            "Изделие А на единицу, руб": round(a_unit_val, 2),
            "Изделие А на годовой выпуск, тыс.руб.": round(a_annual_val, 2) if a_annual_val is not None else None,
            "Изделие Б на единицу, руб": round(b_unit_val, 2),
            "Изделие Б на годовой выпуск, тыс.руб.": round(b_annual_val, 2) if b_annual_val is not None else None,
            "Себестоимость годового выпуска продукции, тыс.руб.": round(combined_annual_val, 2) if combined_annual_val is not None else None,
            "Структура расходов,%": round(perc_combined, 2) if isinstance(perc_combined, (int, float)) else None
        }
        json_data.append(row_data_json)

    # Сохранение JSON
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(json_data, jsonfile, indent=4, ensure_ascii=False) # indent для красивого форматирования, ensure_ascii=False для кириллицы

    print(f"\nJSON таблица структуры себестоимости сохранена в файл: {filename}")


def csv_to_json_structure(csv_path: str) -> List[Dict[str, Any]]:
    """
    Преобразует CSV-файл с иерархической таблицей в список словарей.
    Каждая строка с данными → словарь с иерархическими ключами.
    """
    result = []
    context = {}  # main, sub

    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')

        for row in reader:
            # Пропускаем полностью пустые строки
            if not any(cell.strip() for cell in row):
                continue

            # Заполняем недостающие поля
            row += [''] * (6 - len(row))
            num, indicator, addition_num, unit, item_a, item_b = [cell.strip() for cell in row]

            # Пропускаем пустые значения
            if not indicator and not item_a and not item_b:
                continue

            # --- Определяем тип строки ---
            if indicator.startswith('- '):
                # Подпункт: расходы / отходы
                if 'main' not in context or 'sub' not in context:
                    continue  # защита от ошибок
                sub_type = indicator[2:].strip()
                entry = {
                    "№": num,
                    "Показатель": context['main'],
                    "Подкатегория": context['sub'],
                    "Тип": sub_type,
                    "Дополнение": addition_num,
                    "Ед. измерения": unit or None,
                    "Изделие А": item_a or None,
                    "Изделие Б": item_b or None
                }
                if item_a or item_b:
                    result.append(entry)

            elif '.' in num and num.strip().endswith('.'):
                # Подраздел: 1.1, 1.2 и т.д.
                context['sub'] = indicator
            elif num.isdigit() or (num and not indicator.startswith('-')) and not num.endswith('.'):
                # Основной раздел: 1, 2, 3...
                if indicator:
                    context['main'] = indicator
                    context.pop('sub', None)
                # Для строк верхнего уровня (например, покупные изделия)
                if item_a or item_b:
                    entry = {
                        "№": num,
                        "Показатель": indicator,
                        "Дополнение": addition_num,
                        "Ед. измерения": unit or None,
                        "Изделие А": item_a or None,
                        "Изделие Б": item_b or None
                    }
                    result.append(entry)
            # Иначе — заголовок или пусто, пропускаем

    return result

# --- Пример вызова функции в конце вашего основного скрипта ---
# (Предполагается, что structure_data_A и structure_data_B уже получены)
# structure_data_A = ...
# structure_data_B = ...
# save_structure_table_to_json(structure_data_A, structure_data_B)
