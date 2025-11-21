import pandas as pd
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
import sys


def create_custom_style(doc):
    """Создает изолированный стиль для таблицы без отступов"""
    styles = doc.styles
    # Создаем новый стиль абзаца
    style_name = 'CsvTableText'

    try:
        custom_style = styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
        custom_style.base_style = styles['Normal']
    except:
        custom_style = styles[style_name]  # Если вдруг уже есть

    # Настраиваем стиль жестко
    p_fmt = custom_style.paragraph_format
    p_fmt.first_line_indent = Pt(0)
    p_fmt.left_indent = Pt(0)
    p_fmt.space_before = Pt(0)
    p_fmt.space_after = Pt(0)

    # Можно добавить шрифт, чтобы он тоже не слетал
    font = custom_style.font
    font.name = 'Times New Roman'  # Или какой вам нужен
    font.size = Pt(14)

    return style_name

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

    table_style_name = create_custom_style(doc)

    # Шаг 4: Добавляем таблицу
    table = doc.add_table(rows=len(df) + 1, cols=len(df.columns))
    table.style = 'Table Grid'  # Рамки

    # Шаг 5: Заполняем заголовки
    for j, column in enumerate(df.columns):
        cell = table.cell(0, j)
        cell.text = str(column)
        # !!! 2. Применяем стиль
        cell.paragraphs[0].style = doc.styles[table_style_name]
        cell.paragraphs[0].runs[0].bold = True

    # Шаг 6: Заполняем данные (NaN -> пустая ячейка)
    for i, row in df.iterrows():
        for j, value in enumerate(row):
            cell = table.cell(i + 1, j)
            clean_value = str(value).strip() if pd.notna(value) else ""
            cell.text = clean_value
            # !!! 2. Применяем стиль к каждой ячейке
            cell.paragraphs[0].style = doc.styles[table_style_name]

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