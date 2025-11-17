import pandas as pd
from pprint import pprint  # Для красивой печати, если нужно


def extract_purchased_sums(variant: int, pretty_print: bool = True):
    """
    Извлекает суммы стоимостей покупных комплектующих изделий для указанного варианта из CSV файла 'доп В.csv'.

    Args:
        variant (int): Номер варианта (1-10).
        pretty_print (bool): Если True, печатает данные красиво. Если False, возвращает словарь.

    Returns:
        dict: Словарь {"A": sum_A, "B": sum_B} (если pretty_print=False).
    """
    # Читаем CSV файл
    df = pd.read_csv('dop_V.csv')

    # Проверяем наличие столбца для варианта
    variant_col = str(variant)
    if variant_col not in df.columns:
        raise ValueError(f"Вариант {variant} не найден в данных.")

    # Суммируем по изделию
    sum_a = df[df['Изделие'] == 'А'][variant_col].sum()
    sum_b = df[df['Изделие'] == 'Б'][variant_col].sum()

    result = {"A": sum_a, "B": sum_b}

    if pretty_print:
        print(f"Суммы стоимостей покупных комплектующих для варианта {variant}:")
        pprint(result, indent=2, sort_dicts=False)
        return None  # Не возвращаем, если печатаем
    else:
        return result


# Пример использования с красивой печатью (по умолчанию):
extract_purchased_sums(8)

# Если хочешь просто вернуть словарь (без печати):
# sums_data = extract_purchased_sums(1, pretty_print=False)
# print(sums_data)  # {'A': 139000, 'B': 39800}