import pandas as pd
from pprint import pprint

# Словарь разрядов -> ставки
GRADE_TO_RATE = {3: 30.25, 4: 35.60, 5: 41.50}


def extract_labor_data(variant: int, pretty_print: bool = True):
    """
    Извлекает данные о трудоёмкости и ставках для указанного варианта из CSV файлов 'доп Ж_hours.csv' и 'доп Ж_grades.csv'.

    Args:
        variant (int): Номер варианта (1-10).
        k_zh (float): Коэффициент Кж (по умолчанию 1.0).
        pretty_print (bool): Если True, печатает данные красиво. Если False, возвращает словарь.

    Returns:
        dict: Словарь как в примере (если pretty_print=False).
    """
    # Читаем CSV для часов
    df_hours = pd.read_csv('../dopolneniya_tables/dop_J_hours.csv')
    # Читаем CSV для разрядов
    df_grades = pd.read_csv('../dopolneniya_tables/dop_J_grades.csv')

    # Проверяем наличие столбца для варианта
    variant_col = str(variant)
    if variant_col not in df_hours.columns or variant_col not in df_grades.columns:
        raise ValueError(f"Вариант {variant} не найден в данных.")

    # Суммируем часы по всем видам работ для А и Б
    sum_a_hours = df_hours[df_hours['Изделие'] == 'А'][variant_col].sum()
    sum_b_hours = df_hours[df_hours['Изделие'] == 'Б'][variant_col].sum()

    # Получаем разряды
    grade_a = df_grades[df_grades['Изделие'] == 'А'][variant_col].iloc[0]
    grade_b = df_grades[df_grades['Изделие'] == 'Б'][variant_col].iloc[0]

    # Мапим на ставки
    rate_a = GRADE_TO_RATE.get(int(grade_a), 0)
    rate_b = GRADE_TO_RATE.get(int(grade_b), 0)

    result = {
        "labor_hours": {"A": sum_a_hours, "B": sum_b_hours},
        "hourly_rate": {"A": rate_a, "B": rate_b}
    }

    if pretty_print:
        print(f"Данные о трудоёмкости и ставках для варианта {variant}:")
        pprint(result, indent=2, sort_dicts=False)
        return None
    else:
        return result


# Пример использования с красивой печатью (по умолчанию):
extract_labor_data(1)

# С Кж=1.2, например:
# extract_labor_data(1, k_zh=1.2)

# Просто вернуть словарь:
# labor_data = extract_labor_data(1, pretty_print=False)