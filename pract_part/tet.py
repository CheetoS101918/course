import pandas as pd
from pprint import pprint  # Импортируем для красивой печати


def apply_reductions(variant: int, pretty_print: bool = True):
    """
    Извлекает данные из 'dop_B.csv' и 'dop_P.csv' для указанного варианта,
    применяет проценты снижения норм расходов для проектов 1 и 2,
    пересчитывает расходы, отходы и фиксированные стоимости.

    Args:
        variant (int): Номер варианта (1-10).
        pretty_print (bool): Если True, печатает данные красиво. Если False, возвращает словарь.

    Returns:
        dict: Словарь с обновленными данными для проектов 1 и 2 (если pretty_print=False).
    """
    # Читаем CSV файл dop_B
    df_b = pd.read_csv('../dopolneniya_tables/dop_B.csv')

    # Фильтруем по варианту для dop_B
    variant_df_b = df_b[df_b['Вариант'] == variant]

    if len(variant_df_b) != 2:
        raise ValueError(f"Для варианта {variant} в dop_B не найдено ровно 2 записи (А и Б).")

    # Извлекаем данные для А и Б из dop_B
    row_a = variant_df_b[variant_df_b['Изделие'] == 'А'].iloc[0]
    row_b = variant_df_b[variant_df_b['Изделие'] == 'Б'].iloc[0]

    # Основные материалы (исходные)
    materials_main = {
        "стальной прокат": {
            "type": "material",
            "A": {
                "rasxod": row_a['Стальной_прокат_кг'] / 1000,
                "otxod_percent": row_a['Стальной_прокат_%'],
                "otxod": (row_a['Стальной_прокат_%'] / 100) * (row_a['Стальной_прокат_кг'] / 1000)
            },
            "B": {
                "rasxod": row_b['Стальной_прокат_кг'] / 1000,
                "otxod_percent": row_b['Стальной_прокат_%'],
                "otxod": (row_b['Стальной_прокат_%'] / 100) * (row_b['Стальной_прокат_кг'] / 1000)
            }
        },
        "трубы стальные": {
            "type": "material",
            "A": {
                "rasxod": row_a['Трубы_стальные_кг'] / 1000,
                "otxod_percent": row_a['Трубы_стальные_%'],
                "otxod": (row_a['Трубы_стальные_%'] / 100) * (row_a['Трубы_стальные_кг'] / 1000)
            },
            "B": {
                "rasxod": row_b['Трубы_стальные_кг'] / 1000,
                "otxod_percent": row_b['Трубы_стальные_%'],
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

    # Покупные полуфабрикаты (исходные)
    materials_purchased = {
        "отливки черных металлов": {
            "type": "material",
            "A": {
                "rasxod": row_a['Отливки_черных_кг'] / 1000,
                "otxod_percent": row_a['Отливки_черных_%'],
                "otxod": (row_a['Отливки_черных_%'] / 100) * (row_a['Отливки_черных_кг'] / 1000)
            },
            "B": {
                "rasxod": row_b['Отливки_черных_кг'] / 1000,
                "otxod_percent": row_b['Отливки_черных_%'],
                "otxod": (row_b['Отливки_черных_%'] / 100) * (row_b['Отливки_черных_кг'] / 1000)
            }
        },
        "отливки цветных металлов": {
            "type": "material",
            "A": {
                "rasxod": row_a['Отливки_цветных_кг'] / 1000,
                "otxod_percent": row_a['Отливки_цветных_%'],
                "otxod": (row_a['Отливки_цветных_%'] / 100) * (row_a['Отливки_цветных_кг'] / 1000)
            },
            "B": {
                "rasxod": row_b['Отливки_цветных_кг'] / 1000,
                "otxod_percent": row_b['Отливки_цветных_%'],
                "otxod": (row_b['Отливки_цветных_%'] / 100) * (row_b['Отливки_цветных_кг'] / 1000)
            }
        }
    }

    # Читаем CSV файл dop_P
    df_p = pd.read_csv('../dopolneniya_tables/dop_P.csv', sep=';')

    # Фильтруем по варианту для dop_P
    variant_df_p = df_p[df_p['Вариант задания'] == variant]

    if len(variant_df_p) != 2:
        raise ValueError(f"Для варианта {variant} в dop_P не найдено ровно 2 записи (проекты 1 и 2).")

    # Извлекаем данные для проектов 1 и 2
    row_p1 = variant_df_p[variant_df_p['Вариант проекта развития предприятия'] == 1].iloc[0]
    row_p2 = variant_df_p[variant_df_p['Вариант проекта развития предприятия'] == 2].iloc[0]

    # Проценты снижения (в дробях)
    reductions = {
        "project_1": {
            "steel_rolling": row_p1['Снижение норм расходов стального проката, %'] / 100,
            "steel_pipes": row_p1['Снижение норм расходов стальных труб, %'] / 100,
            "castings": row_p1['Снижение норм расходов отливок черных и цветных металлов, %'] / 100,
            "other_materials": row_p1['Снижение расходов и стоимости других материалов и комплектующих, %'] / 100,
            # labor_intensity игнорируем
        },
        "project_2": {
            "steel_rolling": row_p2['Снижение норм расходов стального проката, %'] / 100,
            "steel_pipes": row_p2['Снижение норм расходов стальных труб, %'] / 100,
            "castings": row_p2['Снижение норм расходов отливок черных и цветных металлов, %'] / 100,
            "other_materials": row_p2['Снижение расходов и стоимости других материалов и комплектующих, %'] / 100,
            # labor_intensity игнорируем
        }
    }

    # Функция для применения снижений к материалам
    def apply_reduction_to_materials(project_reductions, main_mats, purch_mats):
        new_main = {}
        for key, val in main_mats.items():
            new_val = val.copy()
            if key == "стальной прокат":
                red = project_reductions["steel_rolling"]
                for item in ["A", "B"]:
                    old_rasxod = val[item]["rasxod"]
                    new_rasxod = old_rasxod * (1 - red)
                    new_otxod = (val[item]["otxod_percent"] / 100) * new_rasxod
                    new_val[item]["rasxod"] = new_rasxod
                    new_val[item]["otxod"] = new_otxod
            elif key == "трубы стальные":
                red = project_reductions["steel_pipes"]
                for item in ["A", "B"]:
                    old_rasxod = val[item]["rasxod"]
                    new_rasxod = old_rasxod * (1 - red)
                    new_otxod = (val[item]["otxod_percent"] / 100) * new_rasxod
                    new_val[item]["rasxod"] = new_rasxod
                    new_val[item]["otxod"] = new_otxod
            elif key in ["прокат цветных металлов", "другие материалы"]:
                red = project_reductions["other_materials"]
                for item in ["A", "B"]:
                    new_val[item] = val[item] * (1 - red)
            new_main[key] = new_val

        new_purch = {}
        for key, val in purch_mats.items():
            red = project_reductions["castings"]
            new_val = val.copy()
            for item in ["A", "B"]:
                old_rasxod = val[item]["rasxod"]
                new_rasxod = old_rasxod * (1 - red)
                new_otxod = (val[item]["otxod_percent"] / 100) * new_rasxod
                new_val[item]["rasxod"] = new_rasxod
                new_val[item]["otxod"] = new_otxod
            new_purch[key] = new_val

        return new_main, new_purch

    # Применяем для project_1
    new_main_1, new_purch_1 = apply_reduction_to_materials(reductions["project_1"], materials_main, materials_purchased)

    # Применяем для project_2
    new_main_2, new_purch_2 = apply_reduction_to_materials(reductions["project_2"], materials_main, materials_purchased)

    # Собираем результат
    result = {
        "project_1": {
            "materials_main": new_main_1,
            "materials_purchased": new_purch_1
        },
        "project_2": {
            "materials_main": new_main_2,
            "materials_purchased": new_purch_2
        }
    }

    if pretty_print:
        print(f"Обновленные данные для варианта {variant}:")
        print("\nПроект 1:")
        print("Основные материалы:")
        pprint(result["project_1"]["materials_main"], indent=2, sort_dicts=False)
        print("Покупные полуфабрикаты:")
        pprint(result["project_1"]["materials_purchased"], indent=2, sort_dicts=False)
        print("\nПроект 2:")
        print("Основные материалы:")
        pprint(result["project_2"]["materials_main"], indent=2, sort_dicts=False)
        print("Покупные полуфабрикаты:")
        pprint(result["project_2"]["materials_purchased"], indent=2, sort_dicts=False)
        return None
    else:
        return result


# Пример использования с красивой печатью (по умолчанию):
apply_reductions(3)

# Если хочешь просто вернуть словарь (без печати):
# data = apply_reductions(2, pretty_print=False)