# что откуда берется
# та и тб из таблицы исх данных 1.1
# qa qb из джсон, уже есть
# qp qt нужно добавить в джсон
# фч и квн даны
# стп - себестоимость годового выпуска продукции, из табл калькуляции
# Среднегодовая стоимость основных производственных фондов - из 1.2 Фссов
# Суммарный норматив оборотных средств - из 1.3 ОС

import pandas as pd
import json
from math import ceil

df = pd.read_json('../task1/sebestoimost_structure.json')
C_god = df.loc[df['Наименование статей расходов'] == "ВСЕГО полная (коммерческая) себестоимость",
                "Себестоимость годового выпуска продукции, тыс.руб."].iloc[0]

df2 = pd.read_json('../task1/input_data_table.json')
ta = float(df2.loc[df2['Показатель'] == "Суммарная трудоемкость изделия",
                "Изделие А"].iloc[0])
tb = float(df2.loc[df2['Показатель'] == "Суммарная трудоемкость изделия",
                "Изделие Б"].iloc[0])


df3 = pd.read_csv('../task3/Таблица_2_Сводный_расчет_норматива_оборотных_средств.csv', delimiter=';')
oc = df3.loc[4, 'Сумма, тыс. руб']


with open('../task2/фссоф.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
fssof = round(data['Среднегодовая стоимость основных фондов'], 3)

with open('../task1/individual_product_volumes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
qt = round(data[-1]['Qt'], 3)
qr = round(data[-1]['Qr'], 3)

df4 = pd.read_json('../task1/individual_product_volumes.json')
qa = int(df4.loc[df4['Изделие'] == "А",
                "Годовой_объем_выпуска"].iloc[0])
qb = int(df4.loc[df4['Изделие'] == "Б",
                "Годовой_объем_выпуска"].iloc[0])

qa_calc = df4.loc[df4['Изделие'] == "А",
                "Объем_товарной_продукции_по_изделию тыс руб"].iloc[0]
qb_calc = df4.loc[df4['Изделие'] == "Б",
                "Объем_товарной_продукции_по_изделию тыс руб"].iloc[0]


fch = 1860
kvn = 1.1

Pr = qr - C_god #прибыль
R_osn = (ta * qa + tb * qb) / (fch * kvn)
R_vsp = ceil(R_osn) * 0.25
R_sl = (ceil(R_osn) + ceil(R_vsp)) * 0.04
R_ppp = ceil(R_osn) + ceil(R_vsp) + ceil(R_sl)


print(f"Росн  = ({ta} * {qa} + {tb} * {qb}) / ({fch} * {kvn}) = {R_osn:.3f} = {ceil(R_osn)} чел.")
print(f"Рвсп  = {ceil(R_osn)} * 0.25 = {R_vsp} = {ceil(R_vsp)} чел.")
print(f"Рсл  = ({ceil(R_vsp)} + {ceil(R_osn)}) * 0.04 = {R_sl} = {ceil(R_sl)} чел.")
print(f"Численность промышленно-производственного персонала ( Рппп ) определяется суммированием численности всех категорий персонала:")
print(f"Рппп  = {ceil(R_osn)} + {ceil(R_vsp)} + {ceil(R_sl)} = {R_ppp} чел.")
print(f"Пр  =  Q р –  Стп  = {qr} - {C_god} = {Pr}  тыс.руб .")

# 6. Формирование итоговой таблицы
results_data = {
    '№': [str(i) for i in range(1, 8)] + ['7.1', '7.1.1'],
    "Показатель": [
        "Объем товарной продукции",
        "Объем реализованной продукции",
        "Себестоимость товарной продукции",
        "Прибыль от реализации",
        "Среднегодовая стоимость основных производственных фондов",
        "Норматив оборотных средств",
        "Численность промышленно-производственного персонала",
        "в том числе рабочих (основные + вспомогательные)",
        "из них основных рабочих"
    ],
    "Ед.изм.": [
        "тыс.руб.",
        "тыс.руб.",
        "тыс.руб.",
        "тыс.руб.",
        "тыс.руб.",
        "тыс.руб",
        "чел.",
        "чел.",
        "чел."
    ],
    "Значение": [
        qt,
        qr,
        C_god,
        Pr,
        fssof,
        oc,
        R_ppp,
        ceil(R_osn) + ceil(R_vsp),
        ceil(R_osn)
    ]
}

df_results = pd.DataFrame(results_data)

# Сохранение таблицы в CSV
output_filename = 'Таблица_2_7_Показатели_деятельности_предприятия.csv'
df_results.to_csv(output_filename, index=False, sep=';', decimal='.', encoding='utf-8-sig')
print(f"\nИтоговая таблица сохранена в файл: {output_filename}")
