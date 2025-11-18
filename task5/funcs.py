import csv
import math


class EnterpriseEconomicsCalculator:
    def __init__(self):
        self.results = {}

    def set_input_data(self):
        """Установка исходных данных из примера"""
        self.data = {
            # Данные для таблицы 9
            'Q_t': 61284.34,  # Объем товарной продукции, тыс. руб
            'F_sr': 43283.83,  # Среднегодовая стоимость ОФ, тыс. руб
            'P': 11357.66,  # Прибыль, тыс. руб

            # Данные для таблицы 10
            'Q_r': 61590.72,  # Объем реализованной продукции, тыс. руб
            'OS_n': 5763.25,  # Норматив оборотных средств, тыс. руб
            'MZ': 1296.78 + 413.32 + 17361.73 + 10478.94,  # Материальные затраты, тыс. руб

            # Данные для таблицы 11
            'PP_count': 66,  # Численность ППП, чел
            'workers_count': 63,  # Численность рабочих, чел
            'main_workers_count': 50,  # Численность основных рабочих, чел

            # Данные для таблицы 12
            'C_tp': 50233.06,  # Себестоимость товарной продукции, тыс. руб
        }

    def calculate_all(self):
        """Выполняет все расчёты"""
        self._calculate_fixed_assets()  # Таблица 9
        self._calculate_working_capital()  # Таблица 10
        self._calculate_labor_productivity()  # Таблица 11
        self._calculate_summary_indicators()  # Таблица 12

    def _calculate_fixed_assets(self):
        """Расчёт показателей использования основных фондов (Таблица 9)"""
        Q_t = self.data['Q_t']
        F_sr = self.data['F_sr']
        P = self.data['P']

        # Фондоотдача
        F_o = round(Q_t / F_sr, 3)
        # Фондоемкость
        F_e = round(1 / F_o, 3)
        # Прибыль на 1 рубль ОФ
        P_per_F = round(P / F_sr, 3)

        self.results['table9'] = {
            'headers': ['№', 'Показатели', 'Ед. измер.', 'Значение'],
            'data': [
                [1, 'Объем товарной продукции', 'тыс. руб', Q_t],
                [2, 'Среднегодовая стоимость основных производственных фондов', 'тыс. руб', F_sr],
                [3, 'прибыль', 'тыс. руб', P],
                [4, 'фондоотдача', 'руб/руб', F_o],
                [5, 'фондоемкость', 'руб/руб', F_e],
                [6, 'Прибыль на 1 руб. стоимости основных фондов', 'руб/руб', P_per_F]
            ]
        }

        # Вывод в консоль
        print("=== РАСЧЕТ ТАБЛИЦЫ 9 ===")
        print(f"Фондоотдача (Фо) = Qт / Фср = {Q_t} / {F_sr} = {F_o} руб/руб")
        print(f"Фондоемкость (ФЕ) = 1 / Фо = 1 / {F_o} = {F_e} руб/руб")
        print(f"Прибыль на 1 руб ОФ = Пр / Фср = {P} / {F_sr} = {P_per_F} руб/руб")
        print()

    def _calculate_working_capital(self):
        Q_r = self.data['Q_r']
        OS_n = self.data['OS_n']
        MZ = self.data['MZ']
        Q_t = self.data['Q_t']

        # Коэффициент оборачиваемости
        K_ob = round(Q_r / OS_n, 3)
        # Коэффициент закрепления
        K_z = round(1 / K_ob, 3)
        # Длительность одного оборота
        T_ob = round(360 / K_ob, 3)
        # Материалоемкость
        M_e = round(sum(MZ) / Q_t, 3)

        self.results['table10'] = {
            'headers': ['№', 'Показатели', 'Ед. измер.', 'Значение'],
            'data': [
                [1, 'Объем реализованной продукции', 'тыс. руб', Q_r],
                [2, 'Норматив оборотных средств', 'тыс. руб', OS_n],
                [3, 'Коэффициент оборачиваемости', 'руб/руб', K_ob],
                [4, 'Время оборота', 'Дн.', math.ceil(T_ob)],
                [5, 'Коэффициент закрепления (загрузки)', 'руб/руб', K_z],
                [6, 'Материалоемкость', 'руб/руб', M_e]
            ]
        }

        # Вывод в консоль с разложением МЗ
        print("=== РАСЧЕТ ТАБЛИЦЫ 10 ===")
        print(f"Коэффициент оборачиваемости (Коб) = Qр / ОСн = {Q_r} / {OS_n} = {K_ob} об")
        print(f"Коэффициент закрепления (Кз) = 1 / Коб = 1 / {K_ob} = {K_z} руб/руб")
        print(f"Длительность оборота (Тоб) = 360 / Коб = 360 / {K_ob} = {T_ob} = {math.ceil(T_ob)} дн")

        mz_formula = " + ".join(str(float(comp)) for comp in MZ)
        print(f"Материалоемкость (МЕ) = МЗ / Qт = {mz_formula} / {Q_t} = {M_e} руб/руб")
        print()

    def _calculate_labor_productivity(self):
        """Расчёт показателей производительности труда (Таблица 11)"""
        Q_t = self.data['Q_t']
        PP_count = self.data['PP_count']
        workers_count = self.data['workers_count']
        main_workers_count = self.data['main_workers_count']

        # Выработка на одного ППП
        V_ppp = round(Q_t / PP_count, 3)
        # Выработка на одного рабочего
        V_worker = round(Q_t / workers_count, 3)
        # Выработка на одного основного рабочего
        V_main_worker = round(Q_t / main_workers_count, 3)

        self.results['table11'] = {
            'headers': ['№', 'Показатели', 'Ед. измер.', 'Значение'],
            'data': [
                [1, 'Товарная продукция', 'тыс.руб', Q_t],
                [2, 'Численность промышленно-производственного персонала', 'Чел.', PP_count],
                [3, 'Численность рабочих', 'Чел.', workers_count],
                [4, 'Численность основных рабочих', 'Чел.', main_workers_count],
                [5, 'Выработка продукции:', '', ''],
                [5.1, 'нa одного работающего', 'тыс. руб/чел.', V_ppp],
                [5.2, 'нa одного рабочего', 'тыс. руб/чел.', V_worker],
                [5.3, 'на одного основного рабочего', 'тыс. руб/чел.', V_main_worker]
            ]
        }

        # Вывод в консоль
        print("=== РАСЧЕТ ТАБЛИЦЫ 11 ===")
        print(f"Выработка на 1 ППП = Qт / Рппп = {Q_t} / {PP_count} = {V_ppp} тыс.руб/чел (1.29) ")
        print(f"Выработка на 1 рабочего = Qт / Рраб = {Q_t} / {workers_count} = {V_worker} тыс.руб/чел (1.30)")
        print(
            f"Выработка на 1 основного рабочего = Qт / Росн = {Q_t} / {main_workers_count} = {V_main_worker} тыс.руб/чел (1.31)")
        print()

    def _calculate_summary_indicators(self):
        """Расчёт обобщающих показателей эффективности (Таблица 12)"""
        C_tp = self.data['C_tp']
        Q_t = self.data['Q_t']
        P = self.data['P']
        F_sr = self.data['F_sr']
        OS_n = self.data['OS_n']
        Q_r = self.data['Q_r']

        # Затраты на 1 рубль товарной продукции
        Z_1rub = round(C_tp / Q_t, 3)
        # Уровень общей рентабельности
        R_total = round((P / (F_sr + OS_n)) * 100, 3)
        # Рентабельность продаж
        R_sales = round((P / Q_r) * 100, 3)
        # Рентабельность себестоимости
        R_cost = round((P / C_tp) * 100, 3)

        self.results['table12'] = {
            'headers': ['№', 'Показатели', 'Ед. измер.', 'Значение'],
            'data': [
                [1, 'Расходы на 1 руб товарной продукции', 'руб/руб', Z_1rub],
                [2, 'Уровень общей рентабельности', '%', R_total],
                [3, 'Уровень рентабельности', '', ''],
                ['', '- реализованной продукции (рентабельность продаж)', '%', R_sales],
                ['', '- себестоимости продукции (рентабельность затрат)', '%', R_cost]
            ]
        }

        # Вывод в консоль
        print("=== РАСЧЕТ ТАБЛИЦЫ 12 ===")
        print(f"Затраты на 1 руб ТП = Стп / Qт = {C_tp} / {Q_t} = {Z_1rub} руб (1.32)")
        print(
            f"Уровень общей рентабельности = (Пр / (Фср.г. + ОС)) * 100% = ({P} / ({F_sr} + {OS_n})) * 100% = {R_total}% (1.33)")
        print(f"Рентабельность продаж = (Пр / Qр) * 100% = ({P} / {Q_r}) * 100% = {R_sales}% (1.34)")
        print(f"Рентабельность себестоимости = (Пр / Стп) * 100% = ({P} / {C_tp}) * 100% = {R_cost}% (1.35)")
        print()

    def save_to_csv(self):
        """Сохранение всех таблиц в CSV файлы"""
        for table_name, table_data in self.results.items():
            filename = f"{table_name}.csv"
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                # Записываем заголовки
                writer.writerow(table_data['headers'])
                # Записываем данные
                for row in table_data['data']:
                    writer.writerow(row)
            print(f"Таблица сохранена в файл: {filename}")

# Использование класса
def main():
    calculator = EnterpriseEconomicsCalculator()

    # Установка исходных данных
    calculator.set_input_data()

    # Выполнение всех расчётов
    calculator.calculate_all()

    # Сохранение результатов в CSV
    calculator.save_to_csv()


if __name__ == "__main__":
    main()