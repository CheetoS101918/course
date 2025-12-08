"""
РАСЧЕТ НОРМАТИВА ОБОРОТНЫХ СРЕДСТВ
Версия 3.0 - с полными таблицами 2.5 и 2.6
"""

import csv


class Project:
    """Класс для хранения данных и результатов проекта"""

    def __init__(self, name):
        self.name = name

        # Исходные данные для Таблицы 2.5
        self.Q_t = 0.0        # 1. Годовой объем товарной продукции (тыс.руб)
        self.S_om = 0.0       # 2. Расходы основных материалов (тыс.руб)
        self.S_pok = 0.0      # 3. Расходы покупных полуфабрикатов (тыс.руб)
        self.S_vm = 0.0       # 4. Годовые расходы вспомогательных материалов (тыс.руб)
        self.N_om = 0         # 5. Норма запаса основных материалов (дн)
        self.N_pok = 0        # 6. Норма запаса покупных полуфабрикатов (дн)
        self.N_vm = 0         # 7. Норма запаса вспомогательных материалов (дн)
        self.OS_prz = 0.0     # 8. Норматив по прочим производственным запасам (тыс.руб)
        self.S = 0.0          # 9. Производственная себестоимость одного изделия (руб)
        self.S_m = 0.0        # 10. Начальные материальные расходы (руб)
        self.T_c = 0          # 11. Длительность производственного цикла (дн)
        self.N_gp = 0         # 12. Норма запаса готовой продукции (дн)
        self.OS_rbp = 0.0     # 13. Норматив на расходы будущих периодов (тыс.руб)
        self.S_r = 0.0        # Дополнительно: Производственная себестоимость годового выпуска (тыс.руб)

        # Результаты расчетов
        self.results = {}


def calculate_project(project):
    """Выполнение всех расчетов для проекта"""

    results = {}

    # 1. Производственные запасы
    # ОС основных материалов
    OS_om_calc = (project.S_om / 360) * project.N_om
    results['OS_om_calc'] = f"({project.S_om:.3f} / 360) * {project.N_om}"
    results['OS_om'] = round(OS_om_calc, 3)

    # ОС покупных полуфабрикатов
    OS_pok_calc = (project.S_pok / 360) * project.N_pok
    results['OS_pok_calc'] = f"({project.S_pok:.3f} / 360) * {project.N_pok}"
    results['OS_pok'] = round(OS_pok_calc, 3)

    # ОС вспомогательных материалов
    OS_vm_calc = (project.S_vm / 360) * project.N_vm
    results['OS_vm_calc'] = f"({project.S_vm:.3f} / 360) * {project.N_vm}"
    results['OS_vm'] = round(OS_vm_calc, 3)

    # Прочие производственные запасы
    results['OS_prz'] = round(project.OS_prz, 3)

    # Итого производственные запасы
    OS_pz_calc = results['OS_om'] + results['OS_pok'] + results['OS_vm'] + results['OS_prz']
    results['OS_pz_calc'] = f"{results['OS_om']:.3f} + {results['OS_pok']:.3f} + {results['OS_vm']:.3f} + {results['OS_prz']:.3f}"
    results['OS_pz'] = round(OS_pz_calc, 3)

    # 2. Незавершенное производство
    # Коэффициент нарастания затрат
    K_nz_calc = (project.S_m + 0.5 * (project.S - project.S_m)) / project.S
    results['K_nz_calc'] = f"({project.S_m:.3f} + 0.5*({project.S:.3f} - {project.S_m:.3f})) / {project.S:.3f}"
    results['K_nz'] = round(K_nz_calc, 3)

    # Норматив по незавершенному производству
    OS_np_calc = (project.S_r / 360) * project.T_c * results['K_nz']
    results['OS_np_calc'] = f"({project.S_r:.3f} / 360) * {project.T_c} * {results['K_nz']:.3f}"
    results['OS_np'] = round(OS_np_calc, 3)

    # 3. Готовая продукция
    OS_gp_calc = (project.Q_t * project.N_gp) / 360
    results['OS_gp_calc'] = f"({project.Q_t:.3f} * {project.N_gp}) / 360"
    results['OS_gp'] = round(OS_gp_calc, 3)

    # 4. Расходы будущих периодов
    results['OS_rbp'] = round(project.OS_rbp, 3)

    # 5. Итого по проекту
    Itogo_calc = results['OS_pz'] + results['OS_np'] + results['OS_gp'] + results['OS_rbp']
    results['Itogo_calc'] = f"{results['OS_pz']:.3f} + {results['OS_np']:.3f} + {results['OS_gp']:.3f} + {results['OS_rbp']:.3f}"
    results['Itogo'] = round(Itogo_calc, 3)

    project.results = results
    return results


def print_detailed_calculation(project):
    """Вывод подробного расчета для проекта"""
    print(f"\n{'='*60}")
    print(f"**{project.name}**")
    print(f"{'='*60}")

    print(f"ОСом = {project.results['OS_om_calc']} = {project.results['OS_om']:.3f} тыс.руб.")
    print(f"ОСпок = {project.results['OS_pok_calc']} = {project.results['OS_pok']:.3f} тыс.руб.")
    print(f"ОСвм = {project.results['OS_vm_calc']} = {project.results['OS_vm']:.3f} тыс.руб.")
    print(f"ОСпрз = {project.results['OS_prz']:.3f} тыс.руб.")
    print(f"ОСпз = {project.results['OS_pz_calc']} = {project.results['OS_pz']:.3f} тыс.руб.")

    print(f"Кнз = {project.results['K_nz_calc']} = {project.results['K_nz']:.3f}")
    print(f"ОСнп = {project.results['OS_np_calc']} = {project.results['OS_np']:.3f} тыс.руб.")

    print(f"ОСгп = {project.results['OS_gp_calc']} = {project.results['OS_gp']:.3f} тыс.руб.")

    print(f"ОСрбп = {project.results['OS_rbp']:.3f} тыс.руб.")

    print(f"Итого = {project.results['Itogo_calc']} = {project.results['Itogo']:.3f} тыс.руб.")


def generate_table_2_5_csv(project1, project2, filename="table_2_5_initial_data.csv"):
    """Генерация CSV файла с таблицей 2.5 - Исходные данные"""

    # Заголовки таблицы 2.5
    headers = ["№", "Показатели", "Един. измерения", "Условные обозначения",
               f"{project1.name}", f"{project2.name}"]

    # Данные таблицы 2.5 (13 строк)
    data = [
        [1, "Годовой объем товарной продукции", "тыс.руб", "Qт",
         f"{project1.Q_t:.3f}", f"{project2.Q_t:.3f}"],
        [2, "Расходы основных материалов на годовой выпуск", "тыс.руб", "Сом",
         f"{project1.S_om:.3f}", f"{project2.S_om:.3f}"],
        [3, "Расходы покупных полуфабрикатов и комплектующих на годовой выпуск",
         "тыс.руб", "Спок", f"{project1.S_pok:.3f}", f"{project2.S_pok:.3f}"],
        [4, "Годовые расходы вспомогательных материалов", "тыс.руб", "Свм",
         f"{project1.S_vm:.3f}", f"{project2.S_vm:.3f}"],
        [5, "Норма запаса основных материалов", "дн", "Ном",
         f"{project1.N_om}", f"{project2.N_om}"],
        [6, "Норма запаса покупных полуфабрикатов и комплектующих", "дн", "Нпок",
         f"{project1.N_pok}", f"{project2.N_pok}"],
        [7, "Норма запаса вспомогательных материалов", "дн", "Нвм",
         f"{project1.N_vm}", f"{project2.N_vm}"],
        [8, "Норматив оборотных средств по прочим производственным запасам",
         "тыс.руб", "ОСпрз", f"{project1.OS_prz:.3f}", f"{project2.OS_prz:.3f}"],
        [9, "Производственная себестоимость одного изделия", "руб", "С",
         f"{project1.S:.3f}", f"{project2.S:.3f}"],
        [10, "Начальные материальные расходы (сумма расходов по первым двум статьям калькуляции)",
         "руб", "См", f"{project1.S_m:.3f}", f"{project2.S_m:.3f}"],
        [11, "Длительность производственного цикла", "дн", "Тц",
         f"{project1.T_c}", f"{project2.T_c}"],
        [12, "Норма запаса готовой продукции", "дн", "Нгп",
         f"{project1.N_gp}", f"{project2.N_gp}"],
        [13, "Норматив оборотных средств на расходы будущих периодов",
         "тыс.руб", "ОСрбп", f"{project1.OS_rbp:.3f}", f"{project2.OS_rbp:.3f}"]
    ]

    # Запись в CSV файл
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

    print(f"Таблица 2.5 сохранена в файл: {filename}")

    return data


def generate_table_2_6_csv(project1, project2, filename="table_2_6_summary.csv"):
    """Генерация CSV файла с таблицей 2.6 - Сводный расчет"""

    # Подготовка данных для таблицы 2.6
    headers = ["№", "Наименование элементов оборотных средств",
               "Условные обозначения", f"{project1.name}", f"{project2.name}"]

    data = [
        [1, "Производственные запасы", "ОСпз",
         f"{project1.results['OS_pz']:.3f}", f"{project2.results['OS_pz']:.3f}"],
        [2, "Незавершенное производство", "ОСнп",
         f"{project1.results['OS_np']:.3f}", f"{project2.results['OS_np']:.3f}"],
        [3, "Расходы будущих периодов", "ОСрбп",
         f"{project1.results['OS_rbp']:.3f}", f"{project2.results['OS_rbp']:.3f}"],
        [4, "Готовая продукция", "ОСгп",
         f"{project1.results['OS_gp']:.3f}", f"{project2.results['OS_gp']:.3f}"],
        ["", "Всего", "",
         f"{project1.results['Itogo']:.3f}", f"{project2.results['Itogo']:.3f}"]
    ]

    # Запись в CSV файл
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)


    print(f"Таблица 2.6 сохранена в файл: {filename}")

    return data


def create_test_projects():
    """Создание тестовых проектов с данными из ос22.docx"""

    # Проект 1
    project1 = Project("Проект 1")
    # Данные из Таблицы 2.5, столбец "1"
    project1.Q_t = 136533.4108        # Годовой объем товарной продукции
    project1.S_om = 4063.37           # Расходы основных материалов
    project1.S_pok = 53086.63         # Расходы покупных полуфабрикатов
    project1.S_vm = 1600.0            # Годовые расходы вспомогательных материалов
    project1.N_om = 29                # Норма запаса основных материалов
    project1.N_pok = 15               # Норма запаса покупных полуфабрикатов
    project1.N_vm = 8                 # Норма запаса вспомогательных материалов
    project1.OS_prz = 400.0           # Норматив по прочим производственным запасам
    project1.S = 315851.87            # Производственная себестоимость одного изделия
    project1.S_m = 166133.75          # Начальные материальные расходы
    project1.T_c = 8                  # Длительность производственного цикла
    project1.N_gp = 2                 # Норма запаса готовой продукции
    project1.OS_rbp = 320.0           # Норматив на расходы будущих периодов
    # Дополнительные данные из расчетов
    project1.S_r = 108653.04          # Производственная себестоимость годового выпуска

    # Проект 2
    project2 = Project("Проект 2")
    # Данные из Таблицы 2.5, столбец "2"
    project2.Q_t = 147655.32          # Годовой объем товарной продукции
    project2.S_om = 4344.73           # Расходы основных материалов
    project2.S_pok = 57424.49         # Расходы покупных полуфабрикатов
    project2.S_vm = 800.0             # Годовые расходы вспомогательных материалов
    project2.N_om = 25                # Норма запаса основных материалов
    project2.N_pok = 14               # Норма запаса покупных полуфабрикатов
    project2.N_vm = 8                 # Норма запаса вспомогательных материалов
    project2.OS_prz = 300.0           # Норматив по прочим производственным запасам
    project2.S = 322812.72            # Производственная себестоимость одного изделия
    project2.S_m = 169695.64          # Начальные материальные расходы
    project2.T_c = 7                  # Длительность производственного цикла
    project2.N_gp = 2                 # Норма запаса готовой продукции
    project2.OS_rbp = 800.0           # Норматив на расходы будущих периодов
    # Дополнительные данные из расчетов
    project2.S_r = 117503.83          # Производственная себестоимость годового выпуска

    return project1, project2


def create_custom_projects():
    """Создание проектов с пользовательскими данными"""

    # Проект 1 - ВАШИ ДАННЫЕ
    project1 = Project("Проект 1")
    project1.Q_t = 132967.44         # Годовой объем товарной продукции (тыс.руб)
    project1.S_om = 4667.84          # Расходы основных материалов (тыс.руб)
    project1.S_pok = 68701.66         # Расходы покупных полуфабрикатов (тыс.руб)
    project1.S_vm = 1600           # Годовые расходы вспомогательных материалов (тыс.руб)
    project1.N_om = 29               # Норма запаса основных материалов (дн)
    project1.N_pok = 15               # Норма запаса покупных полуфабрикатов (дн)
    project1.N_vm = 8                 # Норма запаса вспомогательных материалов (дн)
    project1.OS_prz = 400.0           # Норматив по прочим производственным запасам (тыс.руб)
    project1.S = 256140.09            # Производственная себестоимость одного изделия (руб)
    project1.S_m = 11329.72 + 166751.60 # Начальные материальные расходы (руб)
    project1.T_c = 8                  # Длительность производственного цикла (дн)
    project1.N_gp = 2                 # Норма запаса готовой продукции (дн)
    project1.OS_rbp = 320           # Норматив на расходы будущих периодов (тыс.руб)
    project1.S_r = 105529.72          # Производственная себестоимость годового выпуска (тыс.руб)

    # Проект 2 - ВАШИ ДАННЫЕ
    project2 = Project("Проект 2")
    project2.Q_t = 136684.17          # Годовой объем товарной продукции (тыс.руб)
    project2.S_om = 4926.99           # Расходы основных материалов (тыс.руб)
    project2.S_pok = 71917.03         # Расходы покупных полуфабрикатов (тыс.руб)
    project2.S_vm = 800.0             # Годовые расходы вспомогательных материалов (тыс.руб)
    project2.N_om = 25                # Норма запаса основных материалов (дн)
    project2.N_pok = 14               # Норма запаса покупных полуфабрикатов (дн)
    project2.N_vm = 8                 # Норма запаса вспомогательных материалов (дн)
    project2.OS_prz = 300.0           # Норматив по прочим производственным запасам (тыс.руб)
    project2.S = 250530.03            # Производственная себестоимость одного изделия (руб)
    project2.S_m = 11378.73 + 166090.14 # Начальные материальные расходы (руб)
    project2.T_c = 7                  # Длительность производственного цикла (дн)
    project2.N_gp = 2                 # Норма запаса готовой продукции (дн)
    project2.OS_rbp = 800           # Норматив на расходы будущих периодов (тыс.руб)
    project2.S_r = 108479.5          # Производственная себестоимость годового выпуска (тыс.руб)

    return project1, project2


def main():
    print("РАСЧЕТ НОРМАТИВА ОБОРОТНЫХ СРЕДСТВ")
    print("="*60)
    print("Версия 3.0 - с таблицами 2.5 и 2.6 в CSV")
    print("="*60)

    # === ВЫБОР РЕЖИМА ===
    print("\nВыберите режим работы:")
    print("1 - Использовать тестовые данные из файла ос22.docx")
    print("2 - Использовать свои данные (задать в коде)")

    choice = input("Введите номер варианта (1 или 2): ").strip()

    if choice == "1":
        print("\nЗагружены тестовые данные из файла ос22.docx")
        project1, project2 = create_test_projects()
    else:
        print("\nИспользованы данные из функции create_custom_projects()")
        print("Для изменения данных отредактируйте функцию create_custom_projects()")
        project1, project2 = create_custom_projects()

    # Выполнение расчетов

    calculate_project(project1)
    calculate_project(project2)

    # Вывод подробных расчетов
    print_detailed_calculation(project1)
    print_detailed_calculation(project2)

    # Генерация таблиц в CSV
    print("\n" + "="*60)
    print("СОЗДАНИЕ ТАБЛИЦ В CSV ФОРМАТЕ")
    print("="*60)

    # Таблица 2.5 - Исходные данные
    generate_table_2_5_csv(project1, project2, "table_2_5_initial_data.csv")

    # Таблица 2.6 - Сводный расчет
    generate_table_2_6_csv(project1, project2, "table_2_6_summary.csv")

    print("\n" + "="*60)
    print("РАСЧЕТ ЗАВЕРШЕН!")
    print("="*60)
    print("Созданы файлы:")
    print("1. table_2_5_initial_data.csv - Исходные данные")
    print("2. table_2_6_summary.csv - Результаты расчетов")


if __name__ == "__main__":
    main()