import pandas as pd
from docx import Document
from docx.shared import Inches
import sys


def create_docx_from_csv(csv_file, output_file=None):
    """
    Создаёт DOCX-документ с таблицей из CSV-файла.

    Args:
        csv_file (str): Путь к CSV-файлу (с разделителем ';').
        output_file (str, optional): Путь к выходному DOCX. Если None,
                                     генерирует имя на основе CSV.

    Returns:
        str: Путь к сохранённому файлу.
    """
    # Шаг 1: Читаем CSV
    df = pd.read_csv(csv_file, sep=';')

    # Шаг 2: Генерируем имя выходного файла, если не указано
    if output_file is None:
        output_file = csv_file.replace('.csv', '_table.docx')

    # Шаг 3: Создаём DOCX
    doc = Document()

    # Шаг 4: Добавляем таблицу
    table = doc.add_table(rows=len(df) + 1, cols=len(df.columns))
    table.style = 'Table Grid'  # Рамки

    # Шаг 5: Заполняем заголовки
    for j, column in enumerate(df.columns):
        cell = table.cell(0, j)
        cell.text = str(column)

    # Шаг 6: Заполняем данные (NaN -> пустая ячейка)
    for i, row in df.iterrows():
        for j, value in enumerate(row):
            cell = table.cell(i + 1, j)
            if pd.notna(value):
                cell.text = str(value)

    # Шаг 7: Настраиваем ширину столбцов
    table.columns[0].width = Inches(2.5)  # Шире для названий
    for j in range(1, len(table.columns)):
        table.columns[j].width = Inches(1.2)

    # Шаг 8: Сохраняем
    doc.save(output_file)
    print(f"Таблица сохранена в {output_file}")
    return output_file


if __name__ == "__main__":
    # Парсим аргументы из командной строки
    if len(sys.argv) != 2:
        print("Использование: python csv_to_docx.py <путь_к_csv_файлу>")
        print("Пример: python csv_to_docx.py sebestoimost_structure.csv")
        sys.exit(1)

    csv_file = sys.argv[1]
    create_docx_from_csv(csv_file)