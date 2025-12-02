import os

# Папки и файлы, которые нужно игнорировать
IGNORE_DIRS = {'.git', '.idea', '__pycache__', 'venv', 'env', '.venv', 'migrations', 'static', 'assets'}
IGNORE_FILES = {'digest.py', 'db.sqlite3', '.DS_Store', 'poetry.lock', 'package-lock.json'}
# Расширения файлов, которые нам нужны (код)
ALLOWED_EXTENSIONS = {'.py', '.html', '.css', '.js', '.json', '.yaml', '.yml', '.ini', '.txt', '.md', '.dockerfile'}

output_file = 'project_context.txt'

with open(output_file, 'w', encoding='utf-8') as outfile:
    # Записываем дерево проекта для наглядности
    outfile.write("=== STRUCTURE ===\n")
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 4 * (level)
        outfile.write(f"{indent}{os.path.basename(root)}/\n")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f not in IGNORE_FILES:
                outfile.write(f"{subindent}{f}\n")

    outfile.write("\n=== FILE CONTENTS ===\n")

    # Записываем содержимое файлов
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]  # Исключаем папки на лету

        for file in files:
            if file in IGNORE_FILES:
                continue

            # Проверяем расширение
            ext = os.path.splitext(file)[1].lower()
            if ext in ALLOWED_EXTENSIONS or file == 'Dockerfile':
                file_path = os.path.join(root, file)

                outfile.write(f"\n\n{'=' * 20}\nFILE: {file_path}\n{'=' * 20}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"Error reading file: {e}")

print(f"Готово! Весь проект собран в {output_file}")