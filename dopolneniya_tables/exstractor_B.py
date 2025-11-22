import pandas as pd
from pprint import pprint  # Импортируем для красивой печати


def extract_materials_data(variant: int, pretty_print: bool = True):
    """
    Извлекает данные материалов для указанного варианта из CSV файла 'доп Б.csv'.

    Args:
        variant (int): Номер варианта (1-10).
        pretty_print (bool): Если True, печатает данные красиво. Если False, возвращает словари.

    Returns:
        tuple: Кортеж из двух словарей - materials_main и materials_purchased (если pretty_print=False).
    """
    # Читаем CSV файл
    df = pd.read_csv('dop_B.csv')

    # Фильтруем по варианту
    variant_df = df[df['Вариант'] == variant]

    # Проверяем наличие данных
    if len(variant_df) != 2:
        raise ValueError(f"Для варианта {variant} не найдено ровно 2 записи (А и Б).")

    # Извлекаем данные для А и Б
    row_a = variant_df[variant_df['Изделие'] == 'А'].iloc[0]
    row_b = variant_df[variant_df['Изделие'] == 'Б'].iloc[0]

    # Основные материалы
    materials_main = {
        "стальной прокат": {
            "type": "material",
            "A": {
                "rasxod": row_a['Стальной_прокат_кг'] / 1000,
                "otxod": (row_a['Стальной_прокат_%'] / 100) * (row_a['Стальной_прокат_кг'] / 1000)
            },
            "B": {
                "rasxod": row_b['Стальной_прокат_кг'] / 1000,
                "otxod": (row_b['Стальной_прокат_%'] / 100) * (row_b['Стальной_прокат_кг'] / 1000)
            }
        },
        "трубы стальные": {
            "type": "material",
            "A": {
                "rasxod": row_a['Трубы_стальные_кг'] / 1000,
                "otxod": (row_a['Трубы_стальные_%'] / 100) * (row_a['Трубы_стальные_кг'] / 1000)
            },
            "B": {
                "rasxod": row_b['Трубы_стальные_кг'] / 1000,
                "otxod": (row_b['Трубы_стальные_%'] / 100) * (row_b['Трубы_стальные_кг'] / 1000)
            }
        },
        "прокат цветных металлов": {
            "type": "fixed",
            "A": row_a['Прокат_цветных_руб'],
            "B": row_b['Прокат_цветных_руб']
        },
        "другие материалы": {
            "type": "fixed",
            "A": row_a['Другие_материалы_руб'],
            "B": row_b['Другие_материалы_руб']
        }
    }

    # Покупные полуфабрикаты
    materials_purchased = {
        "отливки черных металлов": {
            "type": "material",
            "A": {
                "rasxod": row_a['Отливки_черных_кг'] / 1000,
                "otxod": (row_a['Отливки_черных_%'] / 100) * (row_a['Отливки_черных_кг'] / 1000)
            },
            "B": {
                "rasxod": row_b['Отливки_черных_кг'] / 1000,
                "otxod": (row_b['Отливки_черных_%'] / 100) * (row_b['Отливки_черных_кг'] / 1000)
            }
        },
        "отливки цветных металлов": {
            "type": "material",
            "A": {
                "rasxod": row_a['Отливки_цветных_кг'] / 1000,
                "otxod": (row_a['Отливки_цветных_%'] / 100) * (row_a['Отливки_цветных_кг'] / 1000)
            },
            "B": {
                "rasxod": row_b['Отливки_цветных_кг'] / 1000,
                "otxod": (row_b['Отливки_цветных_%'] / 100) * (row_b['Отливки_цветных_кг'] / 1000)
            }
        }
    }

    if pretty_print:
        print(f"Данные для варианта {variant}:")
        print("\nОсновные материалы:")
        pprint(materials_main, indent=2, sort_dicts=False)
        print("\nПокупные полуфабрикаты:")
        pprint(materials_purchased, indent=2, sort_dicts=False)
        return None  # Не возвращаем, если печатаем
    else:
        return materials_main, materials_purchased


# Пример использования с красивой печатью (по умолчанию):
extract_materials_data(1)

# Если хочешь просто вернуть словари (без печати):
# materials_main, materials_purchased = extract_materials_data(2, pretty_print=False)