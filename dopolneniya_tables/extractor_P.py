import pandas as pd
from pprint import pprint  # Импортируем для красивой печати


def get_reduction_data(variant: int, pretty_print: bool = True):
    """
    Извлекает данные о снижении норм расходов для указанного варианта задания из CSV файла 'dop_P.csv'.

    Args:
        variant (int): Номер варианта задания (1-10).
        pretty_print (bool): Если True, печатает данные красиво. Если False, возвращает словарь.

    Returns:
        dict: Словарь с данными для вариантов проекта 1 и 2 (если pretty_print=False).
    """
    # Читаем CSV файл
    df = pd.read_csv('../dopolneniya_tables/dop_P.csv', sep=';')  # Указываем разделитель ';', так как в данных используются ';'

    # Фильтруем по варианту задания
    variant_df = df[df['Вариант задания'] == variant]

    # Проверяем наличие данных
    if len(variant_df) != 2:
        raise ValueError(f"Для варианта задания {variant} не найдено ровно 2 записи (варианты проекта 1 и 2).")

    # Извлекаем данные для вариантов проекта 1 и 2
    row_1 = variant_df[variant_df['Вариант проекта развития предприятия'] == 1].iloc[0]
    row_2 = variant_df[variant_df['Вариант проекта развития предприятия'] == 2].iloc[0]

    # Словарь с данными
    reduction_data = {
        "project_1": {
            "steel_rolling": row_1['Снижение норм расходов стального проката, %'] / 100,
            "steel_pipes": row_1['Снижение норм расходов стальных труб, %'] / 100,
            "castings_black_colored": row_1['Снижение норм расходов отливок черных и цветных металлов, %'] / 100,
            "other_materials": row_1['Снижение расходов и стоимости других материалов и комплектующих, %'] / 100,
            "labor_intensity": row_1['Снижение трудоемкости, %'] / 100
        },
        "project_2": {
            "steel_rolling": row_2['Снижение норм расходов стального проката, %'] / 100,
            "steel_pipes": row_2['Снижение норм расходов стальных труб, %'] / 100,
            "castings_black_colored": row_2['Снижение норм расходов отливок черных и цветных металлов, %'] / 100,
            "other_materials": row_2['Снижение расходов и стоимости других материалов и комплектующих, %'] / 100,
            "labor_intensity": row_2['Снижение трудоемкости, %'] / 100
        }
    }

    if pretty_print:
        print(f"Данные для варианта задания {variant}:")
        pprint(reduction_data, indent=2, sort_dicts=False)
        return None  # Не возвращаем, если печатаем
    else:
        return reduction_data


# Пример использования с красивой печатью (по умолчанию):
get_reduction_data(2)

# Если хочешь просто вернуть словарь (без печати):
# reduction_data = get_reduction_data(2, pretty_print=False)