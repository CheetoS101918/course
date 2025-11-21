import pandas as pd


def get_variant_data(file_path, variant_number):
    """
    Считывает данные из CSV для указанного варианта.
    """
    # Считываем CSV, указывая разделитель "точка с запятой"
    try:
        df = pd.read_csv(file_path, sep=';')
    except FileNotFoundError:
        return "Файл не найден. Проверьте путь."

    # Формируем имя колонки (например, "Вариант 2")
    col_name = f'Вариант {variant_number}'

    # Проверяем, есть ли такой вариант в таблице
    if col_name not in df.columns:
        return f"Вариант {variant_number} не найден в таблице."

    # Извлекаем данные по строкам (индексация начинается с 0)
    # Строка 0: Стоимость (преобразуем в целое число)
    stoimost_rmo_nachalo = int(df[col_name].iloc[0])

    # Строка 1: Группа ввода (строка)
    gruppa_vvod = str(df[col_name].iloc[1]).strip()

    # Строка 2: Группа вывода (строка)
    gruppa_vyvod = str(df[col_name].iloc[2]).strip()

    # Строка 3: Процент ввода (заменяем запятую на точку для float)
    procent_vvoda = float(str(df[col_name].iloc[3]).replace(',', '.'))

    # Строка 4: Процент вывода (заменяем запятую на точку для float)
    procent_vyvoda = float(str(df[col_name].iloc[4]).replace(',', '.'))

    # Строка 5: Месяц ввода (целое число)
    mes_vvoda = int(df[col_name].iloc[5])

    # Строка 6: Месяц вывода (целое число)
    mes_vyvoda = int(df[col_name].iloc[6])

    # Возвращаем словарь для удобства
    return {
        'stoimost_rmo_nachalo': stoimost_rmo_nachalo,
        'gruppa_vvod': gruppa_vvod,
        'gruppa_vyvod': gruppa_vyvod,
        'procent_vvoda': procent_vvoda,
        'procent_vyvoda': procent_vyvoda,
        'mes_vvoda': mes_vvoda,
        'mes_vyvoda': mes_vyvoda
    }