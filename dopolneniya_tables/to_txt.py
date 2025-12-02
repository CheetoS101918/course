# merge_files_to_txt.py
import os
import sys
import argparse
from pathlib import Path


def is_text_file(filepath, sample_size=1024):
    """Простая проверка, является ли файл текстовым (не бинарным)"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read(sample_size)
            return True
    except UnicodeDecodeError:
        return False
    except Exception:
        return False


def merge_directory_to_txt(source_dir: str, output_file: str, recursive=True):
    source_path = Path(source_dir)
    if not source_path.is_dir():
        print(f"Ошибка: {source_dir} не является каталогом или не существует!")
        return

    output_path = Path(output_file)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(f"=== Содержимое каталога: {source_path.resolve()} ===\n")
        outfile.write(f"=== Объединено: {os.path.getmtime(source_dir)} ===\n\n")

        files_processed = 0
        files_skipped = 0

        # Обходим все файлы (рекурсивно или только в текущем каталоге)
        for file_path in source_path.rglob('*') if recursive else source_path.glob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(source_path)

                if not is_text_file(file_path):
                    files_skipped += 1
                    print(f"Пропущен (бинарный/нечитаемый): {rel_path}")
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()

                    outfile.write(f"{'=' * 20} ФАЙЛ: {rel_path} {'=' * 20}\n")
                    outfile.write(content)
                    if not content.endswith('\n'):
                        outfile.write('\n')
                    outfile.write(f"\n{'-' * 60}\n\n")

                    files_processed += 1
                    print(f"Добавлен: {rel_path}")

                except Exception as e:
                    print(f"Ошибка при чтении {rel_path}: {e}")
                    files_skipped += 1

        outfile.write(f"\n=== ГОТОВО ===\n")
        outfile.write(f"Обработано файлов: {files_processed}\n")
        outfile.write(f"Пропущено файлов: {files_skipped}\n")

    print(f"\nГотово! Результат записан в: {output_path.resolve()}")


def main():
    parser = argparse.ArgumentParser(description="Объединить все текстовые файлы из каталога в один .txt")
    parser.add_argument("directory", nargs="?", help="Путь к каталогу с файлами")
    parser.add_argument("-o", "--output", default="merged_output.txt",
                        help="Имя выходного файла (по умолчанию: merged_output.txt)")
    parser.add_argument("--no-recursive", action="store_true", help="Не заходить в подкаталоги")

    args = parser.parse_args()

    if not args.directory:
        directory = input("Введите путь к каталогу: ").strip('"\'')
    else:
        directory = args.directory

    merge_directory_to_txt(
        source_dir=directory,
        output_file=args.output,
        recursive=not args.no_recursive
    )


if __name__ == "__main__":
    main()