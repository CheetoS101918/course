import pandas as pd
from funcs import EnterpriseEconomicsCalculator
import json


df1 = pd.read_csv('../task2/Исходные_данные_основные_фонды.csv', delimiter=';')
machines_begin_oty = float(df1.iloc[0, -1])

df2 = pd.read_csv('../task2/Основные_производственные_фонды_предприятия.csv', delimiter=';')
cost_of_begin_oty = df2.iloc[:-1, -1] #Стоимость на конец года, тыс.руб каждое
#all_of_cost_end = df2.loc[10, 'Стоимость на конец года, тыс.руб'] # Стоимость на конец года, тыс.руб ИТОГО
all_of_cost_end = list(df2.iloc[:, -1] )[-1]

df3 = pd.read_csv('../task3/Таблица_2_Сводный_расчет_норматива_оборотных_средств.csv', delimiter=';')
os = df3.loc[4, 'Сумма, тыс. руб']

with open('../task2/фссоф.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
fsr = round(data['Среднегодовая стоимость основных фондов'], 3)

with open('../task1/individual_product_volumes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
qt = round(data[-1]['Qt'], 3)
qr = round(data[-1]['Qr'], 3)

df4 = pd.read_csv('../task4/Таблица_2_7_Показатели_деятельности_предприятия.csv', delimiter=';')
p = df4.loc[3, 'Значение']
ppp = df4.loc[6, 'Значение']
worker_main_and_add = df4.loc[7, 'Значение']
worker_main_only = df4.loc[8, 'Значение']

df5 = pd.read_csv('../task1/sebestoimost_structure.csv', delimiter=';')
som_a = df5.loc[0, 'Изделие А на годовой выпуск, тыс.руб.']
som_b = df5.loc[0, 'Изделие Б на годовой выпуск, тыс.руб.']
spf_and_skom_a = df5.loc[1, 'Изделие А на годовой выпуск, тыс.руб.']
spf_and_skom_b = df5.loc[1, 'Изделие Б на годовой выпуск, тыс.руб.']
s_tp = df5.iloc[-3, -2]



Frm = round((machines_begin_oty / all_of_cost_end) * 100, 3)
print(f'Frm = ({machines_begin_oty} / {all_of_cost_end}) * 100% = {Frm}')

items = [
    "1. Здания:",
    "2. Сооружения:",
    "3. Передаточные устройства:",
    "4. Машины и оборудование:",
    "4.1. Силовые машины и оборудование:",
    "4.2. Рабочие машины и оборудование:",
    "4.3. Измерительные приборы и устройства:",
    "4.4. Вычислительная техника:",
    "4.5. Другие машины и оборудование:",
    "5. Транспортные средства:",
    "6. Другие основные фонды:"
]
numbers = [
    "1.",
    "2.",
    "3.",
    "4.",
    "4.1.",
    "4.2.",
    "4.3.",
    "4.4.",
    "4.5.",
    "5.",
    "6.",
    '7',
    '7.1',
    '7.2'
]

keys = [
    "Здания",
    "Сооружения",
    "Передаточные устройства",
    "Машины и оборудование",
    "Силовые машины и оборудование",
    "Рабочие машины и оборудование",
    "Измерительные приборы и устройства",
    "Вычислительная техника",
    "Другие машины и оборудование",
    "Транспортные средства",
    "Другие основные фонды",
    'Всего',
    "Доля активной части",
    "Доля пассивной части"
]



doli_konets_goda = []
for n, i in enumerate(cost_of_begin_oty):
    temp = round((i / machines_begin_oty) * Frm, 3)
    doli_konets_goda.append(temp)
    print(f'{items[n]} ({i} / {machines_begin_oty}) * {Frm}% = {temp}%')


doli_konets_goda.append(100)
active_part_k = doli_konets_goda[3] + doli_konets_goda[-3]
passive_part_k = 100 - active_part_k
doli_konets_goda += [active_part_k, passive_part_k]


doli_nachalo_goda = [
    35.6,
    6.2,
    3.5,
    50.6,
    2.3,
    41.5,  # Базовая группа
    3.2,
    3.0,
    0.6,
    2.1,
    2,
    100
]
active_part_n = doli_nachalo_goda[3] + doli_nachalo_goda[-3]
passive_part_n = 100 - active_part_n
doli_nachalo_goda += [active_part_n, passive_part_n]

total_df = pd.DataFrame({
    '№': numbers,
    'Группы основных производственных фондов': keys,
    'На начало года': doli_nachalo_goda,
    'На конец года': doli_konets_goda
})
total_df.to_csv(
    'Структура_основных_производственных_фондов_%.csv',
                sep=';',
                encoding='utf-8-sig',
                index=False,
                decimal='.'
        )


calc = EnterpriseEconomicsCalculator()
calc.data = {
            # Данные для таблицы 9
            'Q_t': qt,  # Объем товарной продукции, тыс. руб
            'F_sr':fsr ,  # Среднегодовая стоимость ОФ, тыс. руб
            'P': p,  # Прибыль, тыс. руб

            # Данные для таблицы 10
            'Q_r': qr,  # Объем реализованной продукции, тыс. руб
            'OS_n': os,  # Норматив оборотных средств, тыс. руб
            'MZ': som_a + som_b + spf_and_skom_b + spf_and_skom_a,  # Материальные затраты, тыс. руб

            # Данные для таблицы 11
            'PP_count': ppp,  # Численность ППП, чел
            'workers_count': worker_main_and_add,  # Численность рабочих, чел
            'main_workers_count': worker_main_only,  # Численность основных рабочих, чел

            # Данные для таблицы 12
            'C_tp': s_tp,  # Себестоимость товарной продукции, тыс. руб
}
calc.calculate_all()
calc.save_to_csv()

