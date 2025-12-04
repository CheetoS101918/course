"""
Курсовая работа по экономике предприятия - расчет проектной части
Этап 1: Расчет себестоимости продукции
"""

import csv
import math
from typing import Dict, List, Tuple, Any
import os

class CostCalculator:
    """Класс для расчета себестоимости продукции"""

    def __init__(self):
        # Инициализация всех данных из примера студента
        self.load_student_example_data()

    def load_student_example_data(self):
        """Загрузка точных данных из примера студента (вариант 3)"""

        # Коэффициенты из примера
        self.Ka = 1.06  # коэффициент для объема производства
        self.Ktr = 1.15  # транспортно-заготовительные расходы

        # Данные по проектам из таблицы 2.1 примера (Исходные данные для экономического обоснования варианта проекта)
        self.projects_data = {
            "project_1": {
                "name": "Проект 1",
                "annual_volume_base": 450,  # шт - Годовой объем производства (строка 1 таблицы 2.1)
                "annual_volume_corrected": round(450 * self.Ka),
                # Снижение норм расходов (%) - раздел "К расчету себестоимости продукции" таблицы 2.1
                "steel_rolling_reduction": 10,  # % - Снижение норм расходов: стального проката (строка 2.1)
                "steel_pipes_reduction": 12,  # % - Снижение норм расходов: стальных труб (строка 2.2)
                "castings_reduction": 18,  # % - Снижение норм расходов: отливок черных и цветных металлов (строка 2.3)
                "other_materials_reduction": 7,
                # % - Снижение расходов и стоимости других материалов и комплектующих (строка 3)
                "labor_intensity_reduction": 15,  # % - Снижение трудоемкости (строка 4)
                # Капитальные затраты (тыс. руб) - раздел "Капитальные затраты" таблицы 2.1
                "design_survey_cost": 2000,  # тыс.руб - Расходы на проектно-изыскательские работы (Кпир) (строка 5)
                "fixed_assets_investment": 27000,  # тыс.руб - Капитальные вложения в основные фонды (Косн) (строка 6)
                "startup_cost": 1800,
                # тыс.руб - Расходы, связанные с пуском, наладкой и освоением производства (Косв) (строка 7)
                "residual_value_percent": 1.2
                # % - Остаточная стоимость основных фондов, которые должны пойти на слом (Кл) (строка 8)
            },
            "project_2": {
                "name": "Проект 2",
                "annual_volume_base": 410,  # шт - Годовой объем производства (строка 1 таблицы 2.1)
                "annual_volume_corrected": round(410 * self.Ka),
                # Снижение норм расходов (%) - значения для Проекта 2 из таблицы 2.1
                "steel_rolling_reduction": 12,  # % - стального проката
                "steel_pipes_reduction": 13,  # % - стальных труб
                "castings_reduction": 15,  # % - отливок черных и цветных металлов
                "other_materials_reduction": 9,  # % - других материалов и комплектующих
                "labor_intensity_reduction": 20,  # % - трудоемкости
                # Капитальные затраты (тыс. руб) - значения для Проекта 2 из таблицы 2.1
                "design_survey_cost": 1800,  # тыс.руб - Кпир
                "fixed_assets_investment": 22000,  # тыс.руб - Косн
                "startup_cost": 2200,  # тыс.руб - Косв
                "residual_value_percent": 1.12  # % - Кл
            }
        }

        # Данные для расчета себестоимости (таблица 2.3 - "Данные для расчета себестоимости, прибыли и цены изделия по проектам")
        self.cost_calculation_data = {
            "project_1": {
                # ОСНОВНЫЕ МАТЕРИАЛЫ (раздел 1 таблицы 2.3)
                "steel_rolling_consumption": 0.3564,  # т - расходы стального проката (пункт 1.1)
                "steel_rolling_waste": 0.0535,  # т - отходы стального проката (пункт 1.1)
                "steel_pipes_consumption": 0.030624,  # т - расходы стальных труб (пункт 1.2)
                "steel_pipes_waste": 0.002144,  # т - отходы стальных труб (пункт 1.2)
                "nonferrous_rolling": 2697,  # руб - прокат цветных металлов (пункт 1.3)
                "other_materials": 1674,  # руб - другие материалы (пункт 1.4)

                # ПОКУПНЫЕ ПОЛУФАБРИКАТЫ (раздел 2 таблицы 2.3)
                "castings_black_consumption": 3.14,  # т - расходы отливок черных металлов (пункт 2.1)
                "castings_black_waste": 0.47,  # т - отходы отливок черных металлов (пункт 2.1)
                "castings_color_consumption": 0.209,  # т - расходы отливок цветных металлов (пункт 2.2)
                "castings_color_waste": 0.052,  # т - отходы отливок цветных металлов (пункт 2.2)

                # КОМПЛЕКТУЮЩИЕ (раздел 3 таблицы 2.3)
                "purchased_components": 132804,  # руб - покупные комплектующие изделия (пункт 3)

                # ЦЕНЫ МАТЕРИАЛОВ (разделы 4-6 таблицы 2.3)
                "price_steel_rolling": 12800,  # руб/т - цена стального проката (пункт 4)
                "price_steel_pipes": 18500,  # руб/т - цена стальных труб (пункт 5)
                "price_castings_black": 10500,  # руб/т - цена отливок черных металлов (пункт 6)
                "price_castings_color": 22600,  # руб/т - цена отливок цветных металлов (пункт 6)

                # ЦЕНЫ ОТХОДОВ (раздел 7 таблицы 2.3)
                "price_waste_steel_rolling": 7500,  # руб/т - цена отходов стального проката (пункт 7)
                "price_waste_steel_pipes": 6300,  # руб/т - цена отходов труб стальных (пункт 7)
                "price_waste_castings_black": 7200,  # руб/т - цена отходов отливок черных металлов (пункт 7)
                "price_waste_castings_color": 16900,  # руб/т - цена отходов отливок цветных металлов (пункт 7)

                # ТОПЛИВО И ЭНЕРГИЯ (раздел 8 таблицы 2.3)
                "fuel_energy_percent": 1,  # % - топливо и энергия на технологические потребности (пункт 8)

                # ТРУДОЕМКОСТЬ И ЗАРПЛАТА (разделы 9-10 таблицы 2.3)
                "labor_intensity": 782,  # н-час - суммарная трудоемкость изделия (пункт 9)
                "hourly_rate": 41.5,  # руб - часовая тарифная ставка (пункт 10)

                # ПРОЦЕНТЫ ДЛЯ РАСЧЕТОВ (разделы 11-17 таблицы 2.3)
                "additional_salary_percent": 40,  # % - дополнительная зарплата (пункт 11)
                "social_insurance_percent": 22,  # % - отчисление на социальное страхование (пункт 12)
                "equipment_maintenance_percent": 87,  # % - расходы на содержание и эксплуатацию оборудования (пункт 13)
                "overhead_production_percent": 85,  # % - общепроизводственные расходы (пункт 14)
                "general_business_percent": 98,  # % - общехозяйственные расходы (пункт 15)
                "non_production_percent": 5,  # % - внепроизводственные расходы (пункт 16)
                "profitability_percent": 20  # % - норматив рентабельности к себестоимости (пункт 17)
                # Примечание: Годовой объем производства (пункт 18) хранится в projects_data
            },
            "project_2": {
                # ОСНОВНЫЕ МАТЕРИАЛЫ для Проекта 2 (таблица 2.3, колонка Проект 2)
                "steel_rolling_consumption": 0.0396,  # т - скорректированный расход стального проката
                "steel_rolling_waste": 0.00396,  # т - скорректированные отходы стального проката
                "steel_pipes_consumption": 0.00383,  # т - скорректированный расход стальных труб
                "steel_pipes_waste": 0.00023,  # т - скорректированные отходы стальных труб
                "nonferrous_rolling": 2790,  # руб - скорректированный прокат цветных металлов
                "other_materials": 1547,  # руб - скорректированные другие материалы

                # ПОКУПНЫЕ ПОЛУФАБРИКАТЫ для Проекта 2
                "castings_black_consumption": 1.533,  # т - скорректированные расходы отливок черных металлов
                "castings_black_waste": 0.337,  # т - скорректированные отходы отливок черных металлов
                "castings_color_consumption": 0.174,  # т - скорректированные расходы отливок цветных металлов
                "castings_color_waste": 0.0348,  # т - скорректированные отходы отливок цветных металлов

                # КОМПЛЕКТУЮЩИЕ для Проекта 2
                "purchased_components": 68978,  # руб - скорректированные покупные комплектующие

                # ЦЕНЫ МАТЕРИАЛОВ и ОТХОДОВ (одинаковые для обоих проектов)
                "price_steel_rolling": 12800,  # руб/т - цена стального проката
                "price_steel_pipes": 18500,  # руб/т - цена стальных труб
                "price_castings_black": 10500,  # руб/т - цена отливок черных металлов
                "price_castings_color": 22600,  # руб/т - цена отливок цветных металлов
                "price_waste_steel_rolling": 7500,  # руб/т - цена отходов стального проката
                "price_waste_steel_pipes": 6300,  # руб/т - цена отходов труб стальных
                "price_waste_castings_black": 7200,  # руб/т - цена отходов отливок черных металлов
                "price_waste_castings_color": 16900,  # руб/т - цена отходов отливок цветных металлов

                # ТОПЛИВО И ЭНЕРГИЯ (одинаковое для обоих проектов)
                "fuel_energy_percent": 0.9,  # %

                # ТРУДОЕМКОСТЬ И ЗАРПЛАТА для Проекта 2
                "labor_intensity": 125.856,  # н-час - скорректированная трудоемкость
                "hourly_rate": 35.6,  # руб - часовая тарифная ставка (та же)

                # ПРОЦЕНТЫ ДЛЯ РАСЧЕТОВ (разделы 11-17 таблицы 2.3)
                "additional_salary_percent": 40,  # % - дополнительная зарплата (пункт 11)
                "social_insurance_percent": 22,  # % - отчисление на социальное страхование (пункт 12)
                "equipment_maintenance_percent": 87,  # % - расходы на содержание и эксплуатацию оборудования (пункт 13)
                "overhead_production_percent": 85,  # % - общепроизводственные расходы (пункт 14)
                "general_business_percent": 98,  # % - общехозяйственные расходы (пункт 15)
                "non_production_percent": 5,  # % - внепроизводственные расходы (пункт 16)
                "profitability_percent": 20  # % - норматив рентабельности к себестоимости (пункт 17)
            }
        }

        # Результаты расчетов
        self.calculation_results = {
            "project_1": {},
            "project_2": {}
        }

    def calculate_material_costs(self, project: str) -> float:
        """Расчет основных материалов за вычетом возвратных отходов (пункт 1)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"1. РАСЧЕТ ОСНОВНЫХ МАТЕРИАЛОВ ЗА ВЫЧЕТОМ ВОЗВРАТНЫХ ОТХОДОВ")
        print(f"{'═'*80}")

        # Стальной прокат
        steel_rolling_raw = data["steel_rolling_consumption"] * data["price_steel_rolling"] * self.Ktr
        steel_rolling_waste = data["steel_rolling_waste"] * data["price_waste_steel_rolling"]
        steel_rolling_cost = steel_rolling_raw - steel_rolling_waste

        print(f"   Стальной прокат: ({data['steel_rolling_consumption']:.4f} × {data['price_steel_rolling']:,} × {self.Ktr}) - ({data['steel_rolling_waste']:.5f} × {data['price_waste_steel_rolling']:,})")
        print(f"   = ({steel_rolling_raw:,.2f}) - ({steel_rolling_waste:,.2f}) = {steel_rolling_cost:,.2f} руб.")

        # Трубы стальные
        steel_pipes_raw = data["steel_pipes_consumption"] * data["price_steel_pipes"] * self.Ktr
        steel_pipes_waste = data["steel_pipes_waste"] * data["price_waste_steel_pipes"]
        steel_pipes_cost = steel_pipes_raw - steel_pipes_waste

        print(f"\n   Трубы стальные: ({data['steel_pipes_consumption']:.4f} × {data['price_steel_pipes']:,} × {self.Ktr}) - ({data['steel_pipes_waste']:.5f} × {data['price_waste_steel_pipes']:,})")
        print(f"   = ({steel_pipes_raw:,.2f}) - ({steel_pipes_waste:,.2f}) = {steel_pipes_cost:,.2f} руб.")

        # Прокат цветных металлов и другие материалы
        print(f"\n   Прокат цветных металлов: {data['nonferrous_rolling']:,} руб.")
        print(f"   Другие материалы: {data['other_materials']:,} руб.")

        # Итого
        total_cost = steel_rolling_cost + steel_pipes_cost + data["nonferrous_rolling"] + data["other_materials"]

        print(f"\n   ИТОГО: {steel_rolling_cost:,.2f} + {steel_pipes_cost:,.2f} + {data['nonferrous_rolling']:,} + {data['other_materials']:,}")
        print(f"        = {total_cost:,.2f} руб.")

        return round(total_cost, 2)

    def calculate_purchased_semi_components(self, project: str) -> float:
        """Расчет покупных полуфабрикатов и комплектующих (пункт 2)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"2. РАСЧЕТ ПОКУПНЫХ ПОЛУФАБРИКАТОВ И КОМПЛЕКТУЮЩИХ")
        print(f"{'═'*80}")

        # Отливки черных металлов
        castings_black_raw = data["castings_black_consumption"] * data["price_castings_black"] * self.Ktr
        castings_black_waste = data["castings_black_waste"] * data["price_waste_castings_black"]
        castings_black_cost = castings_black_raw - castings_black_waste

        print(f"   Отливки черных металлов: ({data['castings_black_consumption']:.3f} × {data['price_castings_black']:,} × {self.Ktr}) - ({data['castings_black_waste']:.4f} × {data['price_waste_castings_black']:,})")
        print(f"   = ({castings_black_raw:,.2f}) - ({castings_black_waste:,.2f}) = {castings_black_cost:,.2f} руб.")

        # Отливки цветных металлов
        castings_color_raw = data["castings_color_consumption"] * data["price_castings_color"] * self.Ktr
        castings_color_waste = data["castings_color_waste"] * data["price_waste_castings_color"]
        castings_color_cost = castings_color_raw - castings_color_waste

        print(f"\n   Отливки цветных металлов: ({data['castings_color_consumption']:.3f} × {data['price_castings_color']:,} × {self.Ktr}) - ({data['castings_color_waste']:.5f} × {data['price_waste_castings_color']:,})")
        print(f"   = ({castings_color_raw:,.2f}) - ({castings_color_waste:,.2f}) = {castings_color_cost:,.2f} руб.")

        # Комплектующие
        print(f"\n   Покупные комплектующие изделия: {data['purchased_components']:,} руб.")

        # Итого
        total_cost = castings_black_cost + castings_color_cost + data["purchased_components"]

        print(f"\n   ИТОГО: {castings_black_cost:,.2f} + {castings_color_cost:,.2f} + {data['purchased_components']:,}")
        print(f"        = {total_cost:,.2f} руб.")

        return round(total_cost, 2)

    def calculate_fuel_energy(self, project: str, material_costs: float,
                            semi_components_costs: float) -> float:
        """Расчет топлива и энергии на технологические потребности (пункт 3)"""
        data = self.cost_calculation_data[project]
        beta = data["fuel_energy_percent"]

        print(f"\n{'═'*80}")
        print(f"3. РАСЧЕТ ТОПЛИВА И ЭНЕРГИИ НА ТЕХНОЛОГИЧЕСКИЕ ПОТРЕБНОСТИ")
        print(f"{'═'*80}")

        # Формула: Впер = ((Вом + Впф + Вком) * β) / (100 - β)
        sum_materials = material_costs + semi_components_costs
        numerator = sum_materials * beta
        denominator = 100 - beta

        fuel_energy_cost = numerator / denominator

        print(f"   Формула: Впер = ((Вом + Впф + Вком) × β) / (100 - β)")
        print(f"   Вом = {material_costs:,.2f} руб. (основные материалы)")
        print(f"   Впф + Вком = {semi_components_costs:,.2f} руб. (полуфабрикаты и комплектующие)")
        print(f"   β = {beta}%")
        print(f"\n   Расчет: (({material_costs:,.2f} + {semi_components_costs:,.2f}) × {beta}) / (100 - {beta})")
        print(f"         = ({sum_materials:,.2f} × {beta}) / {denominator}")
        print(f"         = {numerator:,.2f} / {denominator}")
        print(f"         = {fuel_energy_cost:,.2f} руб.")

        return round(fuel_energy_cost, 2)

    def calculate_basic_salary(self, project: str) -> float:
        """Расчет основной заработной платы (пункт 4)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"4. РАСЧЕТ ОСНОВНОЙ ЗАРАБОТНОЙ ПЛАТЫ ПРОИЗВОДСТВЕННЫХ РАБОЧИХ")
        print(f"{'═'*80}")

        basic_salary = data["labor_intensity"] * data["hourly_rate"]

        print(f"   Формула: Сосн = t × Т")
        print(f"   t = {data['hourly_rate']:.2f} руб./час (часовая тарифная ставка)")
        print(f"   Т = {data['labor_intensity']:.2f} н-час (суммарная трудоемкость)")
        print(f"\n   Расчет: {data['labor_intensity']:.2f} × {data['hourly_rate']:.2f}")
        print(f"         = {basic_salary:,.2f} руб.")

        return round(basic_salary, 2)

    def calculate_additional_salary(self, project: str, basic_salary: float) -> float:
        """Расчет дополнительной заработной платы (пункт 5)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"5. РАСЧЕТ ДОПОЛНИТЕЛЬНОЙ ЗАРАБОТНОЙ ПЛАТЫ")
        print(f"{'═'*80}")

        additional_salary = basic_salary * data["additional_salary_percent"] / 100

        print(f"   Формула: Сдоп = Сосн × %доп")
        print(f"   Сосн = {basic_salary:,.2f} руб. (основная зарплата)")
        print(f"   %доп = {data['additional_salary_percent']}%")
        print(f"\n   Расчет: {basic_salary:,.2f} × {data['additional_salary_percent']}%")
        print(f"         = {basic_salary:,.2f} × {data['additional_salary_percent']/100}")
        print(f"         = {additional_salary:,.2f} руб.")

        return round(additional_salary, 2)

    def calculate_social_insurance(self, project: str, basic_salary: float,
                                 additional_salary: float) -> float:
        """Расчет отчислений на социальное страхование (пункт 6)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"6. РАСЧЕТ ОТЧИСЛЕНИЙ В ФОНДЫ СОЦИАЛЬНЫХ МЕРОПРИЯТИЙ")
        print(f"{'═'*80}")

        total_salary = basic_salary + additional_salary
        social_insurance = total_salary * data["social_insurance_percent"] / 100

        print(f"   Формула: Ссоц = (Сосн + Сдоп) × %соц")
        print(f"   Сосн = {basic_salary:,.2f} руб.")
        print(f"   Сдоп = {additional_salary:,.2f} руб.")
        print(f"   %соц = {data['social_insurance_percent']}%")
        print(f"\n   Расчет: ({basic_salary:,.2f} + {additional_salary:,.2f}) × {data['social_insurance_percent']}%")
        print(f"         = {total_salary:,.2f} × {data['social_insurance_percent']/100}")
        print(f"         = {social_insurance:,.2f} руб.")

        return round(social_insurance, 2)

    def calculate_equipment_maintenance(self, project: str, basic_salary: float) -> float:
        """Расчет расходов на содержание и эксплуатацию оборудования (пункт 7)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"7. РАСЧЕТ РАСХОДОВ НА СОДЕРЖАНИЕ И ЭКСПЛУАТАЦИЮ ОБОРУДОВАНИЯ")
        print(f"{'═'*80}")

        equipment_cost = basic_salary * data["equipment_maintenance_percent"] / 100

        print(f"   Формула: Рсэо = Сосн × %рсэо")
        print(f"   Сосн = {basic_salary:,.2f} руб. (основная зарплата)")
        print(f"   %рсэо = {data['equipment_maintenance_percent']}%")
        print(f"\n   Расчет: {basic_salary:,.2f} × {data['equipment_maintenance_percent']}%")
        print(f"         = {basic_salary:,.2f} × {data['equipment_maintenance_percent']/100}")
        print(f"         = {equipment_cost:,.2f} руб.")

        return round(equipment_cost, 2)

    def calculate_overhead_production(self, project: str, basic_salary: float) -> float:
        """Расчет общепроизводственных расходов (пункт 8)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"8. РАСЧЕТ ОБЩЕПРОИЗВОДСТВЕННЫХ РАСХОДОВ")
        print(f"{'═'*80}")

        overhead = basic_salary * data["overhead_production_percent"] / 100

        print(f"   Формула: Роп = Сосн × %роп")
        print(f"   Сосн = {basic_salary:,.2f} руб. (основная зарплата)")
        print(f"   %роп = {data['overhead_production_percent']}%")
        print(f"\n   Расчет: {basic_salary:,.2f} × {data['overhead_production_percent']}%")
        print(f"         = {basic_salary:,.2f} × {data['overhead_production_percent']/100}")
        print(f"         = {overhead:,.2f} руб.")

        return round(overhead, 2)

    def calculate_general_business(self, project: str, basic_salary: float) -> float:
        """Расчет общехозяйственных расходы (пункт 9)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"9. РАСЧЕТ ОБЩЕХОЗЯЙСТВЕННЫХ РАСХОДОВ")
        print(f"{'═'*80}")

        general_business = basic_salary * data["general_business_percent"] / 100

        print(f"   Формула: Рох = Сосн × %рох")
        print(f"   Сосн = {basic_salary:,.2f} руб. (основная зарплата)")
        print(f"   %рох = {data['general_business_percent']}%")
        print(f"\n   Расчет: {basic_salary:,.2f} × {data['general_business_percent']}%")
        print(f"         = {basic_salary:,.2f} × {data['general_business_percent']/100}")
        print(f"         = {general_business:,.2f} руб.")

        return round(general_business, 2)

    def calculate_non_production(self, project: str, production_cost: float) -> float:
        """Расчет внепроизводственных расходов (пункт 11)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"11. РАСЧЕТ ВНЕПРОИЗВОДСТВЕННЫХ РАСХОДОВ")
        print(f"{'═'*80}")

        non_production = production_cost * data["non_production_percent"] / 100

        print(f"   Формула: Впр = Спроиз × %впр")
        print(f"   Спроиз = {production_cost:,.2f} руб. (производственная себестоимость)")
        print(f"   %впр = {data['non_production_percent']}%")
        print(f"\n   Расчет: {production_cost:,.2f} × {data['non_production_percent']}%")
        print(f"         = {production_cost:,.2f} × {data['non_production_percent']/100}")
        print(f"         = {non_production:,.2f} руб.")

        return round(non_production, 2)

    def calculate_profit(self, project: str, full_cost: float) -> float:
        """Расчет прибыли (пункт 13)"""
        data = self.cost_calculation_data[project]

        print(f"\n{'═'*80}")
        print(f"13. РАСЧЕТ ПРИБЫЛИ")
        print(f"{'═'*80}")

        profit = full_cost * data["profitability_percent"] / 100

        print(f"   Формула: П = Сполн × %рент")
        print(f"   Сполн = {full_cost:,.2f} руб. (полная себестоимость)")
        print(f"   %рент = {data['profitability_percent']}% (норматив рентабельности)")
        print(f"\n   Расчет: {full_cost:,.2f} × {data['profitability_percent']}%")
        print(f"         = {full_cost:,.2f} × {data['profitability_percent']/100}")
        print(f"         = {profit:,.2f} руб.")

        return round(profit, 2)

    def calculate_wholesale_price(self, full_cost: float, profit: float) -> float:
        """Расчет оптовой цены (пункт 14)"""

        print(f"\n{'═'*80}")
        print(f"14. РАСЧЕТ ОПТОВОЙ ЦЕНЫ")
        print(f"{'═'*80}")

        wholesale_price = full_cost + profit

        print(f"   Формула: Цопт = Сполн + П")
        print(f"   Сполн = {full_cost:,.2f} руб. (полная себестоимость)")
        print(f"   П = {profit:,.2f} руб. (прибыль)")
        print(f"\n   Расчет: {full_cost:,.2f} + {profit:,.2f}")
        print(f"         = {wholesale_price:,.2f} руб.")

        return round(wholesale_price, 2)

    def calculate_annual_costs(self, unit_cost: float, annual_volume: float, item_name: str = "") -> float:
        """Расчет годовых затрат (тыс. руб)"""
        annual_cost = (unit_cost * annual_volume) / 1000  # переводим в тыс. руб

        if item_name:
            print(f"\n   Годовые затраты на '{item_name}':")
            print(f"   {unit_cost:,.2f} руб./ед. × {annual_volume:.0f} шт. / 1000")
            print(f"   = {annual_cost:,.2f} тыс. руб.")

        return round(annual_cost, 2)

    def calculate_all_costs(self):
        """Основной метод расчета всех статей себестоимости для обоих проектов"""

        for project_key in ["project_1", "project_2"]:
            project_name = self.projects_data[project_key]["name"]
            annual_volume = self.projects_data[project_key]["annual_volume_corrected"]

            print(f"\n{'═'*80}")
            print(f"РАСЧЕТ СЕБЕСТОИМОСТИ ДЛЯ {project_name}")
            print(f"{'═'*80}")

            print(f"\nИСХОДНЫЕ ДАННЫЕ:")
            print(f"  Годовой объем: {annual_volume} шт.")
            print(f"  Коэффициент Ктр: {self.Ktr}")

            # 1. Основные материалы
            material_costs = self.calculate_material_costs(project_key)
            self.calculation_results[project_key]["material_costs"] = material_costs

            # 2. Покупные полуфабрикаты и комплектующие
            semi_components = self.calculate_purchased_semi_components(project_key)
            self.calculation_results[project_key]["semi_components"] = semi_components

            # 3. Топливо и энергия
            fuel_energy = self.calculate_fuel_energy(project_key, material_costs, semi_components)
            self.calculation_results[project_key]["fuel_energy"] = fuel_energy

            # 4. Основная зарплата
            basic_salary = self.calculate_basic_salary(project_key)
            self.calculation_results[project_key]["basic_salary"] = basic_salary

            # 5. Дополнительная зарплата
            additional_salary = self.calculate_additional_salary(project_key, basic_salary)
            self.calculation_results[project_key]["additional_salary"] = additional_salary

            # 6. Отчисления на социальное страхование
            social_insurance = self.calculate_social_insurance(project_key, basic_salary, additional_salary)
            self.calculation_results[project_key]["social_insurance"] = social_insurance

            # 7. Расходы на содержание и эксплуатацию оборудования
            equipment_maintenance = self.calculate_equipment_maintenance(project_key, basic_salary)
            self.calculation_results[project_key]["equipment_maintenance"] = equipment_maintenance

            # 8. Общепроизводственные расходы
            overhead_production = self.calculate_overhead_production(project_key, basic_salary)
            self.calculation_results[project_key]["overhead_production"] = overhead_production

            # 9. Общехозяйственные расходы
            general_business = self.calculate_general_business(project_key, basic_salary)
            self.calculation_results[project_key]["general_business"] = general_business

            # 10. Производственная себестоимость
            print(f"\n{'═'*80}")
            print(f"10. РАСЧЕТ ПРОИЗВОДСТВЕННОЙ СЕБЕСТОИМОСТИ")
            print(f"{'═'*80}")

            production_costs = [
                material_costs,
                semi_components,
                fuel_energy,
                basic_salary,
                additional_salary,
                social_insurance,
                equipment_maintenance,
                overhead_production,
                general_business
            ]

            production_cost = round(sum(production_costs), 2)

            print(f"\n   Суммируем все производственные расходы:")
            print(f"   1. Основные материалы: {material_costs:,.2f} руб.")
            print(f"   2. Полуфабрикаты и комплектующие: {semi_components:,.2f} руб.")
            print(f"   3. Топливо и энергия: {fuel_energy:,.2f} руб.")
            print(f"   4. Основная зарплата: {basic_salary:,.2f} руб.")
            print(f"   5. Дополнительная зарплата: {additional_salary:,.2f} руб.")
            print(f"   6. Отчисления: {social_insurance:,.2f} руб.")
            print(f"   7. Содержание оборудования: {equipment_maintenance:,.2f} руб.")
            print(f"   8. Общепроизводственные расходы: {overhead_production:,.2f} руб.")
            print(f"   9. Общехозяйственные расходы: {general_business:,.2f} руб.")
            print(f"\n   ИТОГО: {production_cost:,.2f} руб.")

            self.calculation_results[project_key]["production_cost"] = production_cost

            # 11. Внепроизводственные расходы
            non_production = self.calculate_non_production(project_key, production_cost)
            self.calculation_results[project_key]["non_production"] = non_production

            # 12. Полная себестоимость
            print(f"\n{'═'*80}")
            print(f"12. РАСЧЕТ ПОЛНОЙ СЕБЕСТОИМОСТИ")
            print(f"{'═'*80}")

            full_cost = production_cost + non_production

            print(f"\n   Формула: Сполн = Спроиз + Впр")
            print(f"   Спроиз = {production_cost:,.2f} руб.")
            print(f"   Впр = {non_production:,.2f} руб.")
            print(f"\n   Расчет: {production_cost:,.2f} + {non_production:,.2f}")
            print(f"         = {full_cost:,.2f} руб.")

            self.calculation_results[project_key]["full_cost"] = full_cost

            # 13. Прибыль
            profit = self.calculate_profit(project_key, full_cost)
            self.calculation_results[project_key]["profit"] = profit

            # 14. Оптовая цена
            wholesale_price = self.calculate_wholesale_price(full_cost, profit)
            self.calculation_results[project_key]["wholesale_price"] = wholesale_price

            # Годовые затраты
            print(f"\n{'═'*80}")
            print(f"РАСЧЕТ ГОДОВЫХ ЗАТРАТ И ВЫПУСКА")
            print(f"{'═'*80}")

            annual_material = self.calculate_annual_costs(material_costs, annual_volume, "Основные материалы")
            annual_semi = self.calculate_annual_costs(semi_components, annual_volume, "Полуфабрикаты и комплектующие")
            annual_fuel = self.calculate_annual_costs(fuel_energy, annual_volume, "Топливо и энергия")
            annual_basic_salary = self.calculate_annual_costs(basic_salary, annual_volume, "Основная зарплата")
            annual_additional_salary = self.calculate_annual_costs(additional_salary, annual_volume, "Дополнительная зарплата")
            annual_social = self.calculate_annual_costs(social_insurance, annual_volume, "Отчисления")
            annual_equipment = self.calculate_annual_costs(equipment_maintenance, annual_volume, "Содержание оборудования")
            annual_overhead = self.calculate_annual_costs(overhead_production, annual_volume, "Общепроизводственные расходы")
            annual_general = self.calculate_annual_costs(general_business, annual_volume, "Общехозяйственные расходы")
            annual_production = self.calculate_annual_costs(production_cost, annual_volume, "Производственная себестоимость")
            annual_non_production = self.calculate_annual_costs(non_production, annual_volume, "Внепроизводственные расходы")
            annual_full_cost = self.calculate_annual_costs(full_cost, annual_volume, "Полная себестоимость")
            annual_profit = self.calculate_annual_costs(profit, annual_volume, "Прибыль")

            # Объем товарной продукции
            commodity_output = (wholesale_price * annual_volume) / 1000  # тыс. руб
            print(f"\n   Объем товарной продукции (Qт):")
            print(f"   {wholesale_price:,.2f} руб./ед. × {annual_volume} шт. / 1000")
            print(f"   = {commodity_output:,.2f} тыс. руб.")


            # Сохраняем результаты
            self.calculation_results[project_key]["annual_costs"] = {
                "material": annual_material,
                "semi_components": annual_semi,
                "fuel_energy": annual_fuel,
                "basic_salary": annual_basic_salary,
                "additional_salary": annual_additional_salary,
                "social_insurance": annual_social,
                "equipment_maintenance": annual_equipment,
                "overhead_production": annual_overhead,
                "general_business": annual_general,
                "production_cost": annual_production,
                "non_production": annual_non_production,
                "full_cost": annual_full_cost,
                "profit": annual_profit,
                "commodity_output": commodity_output
            }

            print(f"\n{'═'*80}")
            print(f"ИТОГОВЫЕ РЕЗУЛЬТАТЫ ДЛЯ {project_name}")
            print(f"{'═'*80}")
            print(f"  Полная себестоимость единицы: {full_cost:,.2f} руб.")
            print(f"  Прибыль единицы: {profit:,.2f} руб.")
            print(f"  Оптовая цена единицы: {wholesale_price:,.2f} руб.")
            print(f"  Годовая полная себестоимость: {annual_full_cost:,.2f} тыс. руб.")
            print(f"  Годовая прибыль: {annual_profit:,.2f} тыс. руб.")
            print(f"  Объем товарной продукции: {commodity_output:,.2f} тыс. руб.")

    def create_cost_table_2_4(self):
        """Создание таблицы 2.4 - Калькуляция себестоимости, прибыль и оптовая цена"""

        # Заголовки таблицы
        headers = [
            "Наименование статей расходов",
            "Проект 1",
            " ",
            "Проект 2",
            " "
        ]

        subheaders = [
            "",
            "на единицу, руб.",
            "на годовой выпуск, тыс.руб.",
            "на единицу, руб.",
            "на годовой выпуск, тыс.руб."
        ]

        # Данные для таблицы
        rows = []

        # 1. Основные материалы
        rows.append([
            "1.Основные материалы за вычетом возвратных отходов",
            f"{self.calculation_results['project_1']['material_costs']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['material']:.2f}",
            f"{self.calculation_results['project_2']['material_costs']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['material']:.2f}"
        ])

        # 2. Покупные полуфабрикаты и комплектующие
        rows.append([
            "2.Покупные полуфабрикаты и комплектующие изделия",
            f"{self.calculation_results['project_1']['semi_components']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['semi_components']:.2f}",
            f"{self.calculation_results['project_2']['semi_components']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['semi_components']:.2f}"
        ])

        # 3. Топливо и энергия
        rows.append([
            "3.Топливо и энергия на технологические потребности",
            f"{self.calculation_results['project_1']['fuel_energy']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['fuel_energy']:.2f}",
            f"{self.calculation_results['project_2']['fuel_energy']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['fuel_energy']:.2f}"
        ])

        # 4. Основная зарплата
        rows.append([
            "4.Основная заработная плата производственных рабочих",
            f"{self.calculation_results['project_1']['basic_salary']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['basic_salary']:.2f}",
            f"{self.calculation_results['project_2']['basic_salary']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['basic_salary']:.2f}"
        ])

        # 5. Дополнительная зарплата
        rows.append([
            "5.Дополнительная заработная плата производственных рабочих",
            f"{self.calculation_results['project_1']['additional_salary']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['additional_salary']:.2f}",
            f"{self.calculation_results['project_2']['additional_salary']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['additional_salary']:.2f}"
        ])

        # 6. Отчисления на социальное страхование
        rows.append([
            "6.Отчисление в фонды социальных мероприятий",
            f"{self.calculation_results['project_1']['social_insurance']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['social_insurance']:.2f}",
            f"{self.calculation_results['project_2']['social_insurance']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['social_insurance']:.2f}"
        ])

        # 7. Расходы на содержание и эксплуатацию оборудования
        rows.append([
            "7.Расходы по содержанию и эксплуатации оборудования",
            f"{self.calculation_results['project_1']['equipment_maintenance']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['equipment_maintenance']:.2f}",
            f"{self.calculation_results['project_2']['equipment_maintenance']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['equipment_maintenance']:.2f}"
        ])

        # 8. Общепроизводственные расходы
        rows.append([
            "8.Общепроизводственные расходы",
            f"{self.calculation_results['project_1']['overhead_production']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['overhead_production']:.2f}",
            f"{self.calculation_results['project_2']['overhead_production']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['overhead_production']:.2f}"
        ])

        # 9. Общехозяйственные расходы
        rows.append([
            "9.Общехозяйственные расходы",
            f"{self.calculation_results['project_1']['general_business']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['general_business']:.2f}",
            f"{self.calculation_results['project_2']['general_business']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['general_business']:.2f}"
        ])

        # 10. ИТОГО производственная себестоимость
        rows.append([
            "ВСЕГО производственная себестоимость",
            f"{self.calculation_results['project_1']['production_cost']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['production_cost']:.2f}",
            f"{self.calculation_results['project_2']['production_cost']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['production_cost']:.2f}"
        ])

        # 11. Внепроизводственные расходы
        rows.append([
            "10.Внепроизводственные расходы",
            f"{self.calculation_results['project_1']['non_production']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['non_production']:.2f}",
            f"{self.calculation_results['project_2']['non_production']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['non_production']:.2f}"
        ])

        # 12. ИТОГО полная себестоимость
        rows.append([
            "ВСЕГО полная себестоимость",
            f"{self.calculation_results['project_1']['full_cost']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['full_cost']:.2f}",
            f"{self.calculation_results['project_2']['full_cost']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['full_cost']:.2f}"
        ])

        # 13. Прибыль
        rows.append([
            "Прибыль",
            f"{self.calculation_results['project_1']['profit']:.2f}",
            f"{self.calculation_results['project_1']['annual_costs']['profit']:.2f}",
            f"{self.calculation_results['project_2']['profit']:.2f}",
            f"{self.calculation_results['project_2']['annual_costs']['profit']:.2f}"
        ])

        # 14. Оптовая цена
        rows.append([
            "Оптовая цена",
            f"{self.calculation_results['project_1']['wholesale_price']:.2f}",
            "",
            f"{self.calculation_results['project_2']['wholesale_price']:.2f}",
            ""
        ])

        # Создаем CSV файл
        filename = "таблица_2_4_себестоимость.csv"

        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            # Записываем заголовки
            writer.writerow(headers)
            writer.writerow(subheaders)

            # Записываем данные
            for row in rows:
                writer.writerow(row)

        print(f"\nТаблица 2.4 сохранена в файл: {filename}")
        return filename

    def create_input_data_table_2_3(self):
        """Создание таблицы 2.3 - Данные для расчета себестоимости"""

        # Заголовки таблицы
        headers = ["№", "Показатели", "Ед. измерения", "Проект 1", "Проект 2"]

        # Данные для таблицы (основные показатели)
        rows = [
            ["1", "Основные материалы", "", "", ""],
            ["1.1", "Стальной прокат:", "", "", ""],
            ["", " - расходы", "т",
             f"{self.cost_calculation_data['project_1']['steel_rolling_consumption']:.4f}",
             f"{self.cost_calculation_data['project_2']['steel_rolling_consumption']:.4f}"],
            ["", " - отходы", "т",
             f"{self.cost_calculation_data['project_1']['steel_rolling_waste']:.5f}",
             f"{self.cost_calculation_data['project_2']['steel_rolling_waste']:.6f}"],
            ["1.2", "Трубы стальные:", "", "", ""],
            ["", " - расходы", "т",
             f"{self.cost_calculation_data['project_1']['steel_pipes_consumption']:.4f}",
             f"{self.cost_calculation_data['project_2']['steel_pipes_consumption']:.4f}"],
            ["", " - отходы", "т",
             f"{self.cost_calculation_data['project_1']['steel_pipes_waste']:.5f}",
             f"{self.cost_calculation_data['project_2']['steel_pipes_waste']:.6f}"],
            ["1.3", "Прокат цветных металлов", "руб",
             f"{self.cost_calculation_data['project_1']['nonferrous_rolling']:.0f}",
             f"{self.cost_calculation_data['project_2']['nonferrous_rolling']:.0f}"],
            ["1.4", "Другие материалы", "руб",
             f"{self.cost_calculation_data['project_1']['other_materials']:.0f}",
             f"{self.cost_calculation_data['project_2']['other_materials']:.0f}"],
            ["2", "Покупные полуфабрикаты (отливки):", "", "", ""],
            ["2.1", "черных металлов", "", "", ""],
            ["", " - расходы", "т",
             f"{self.cost_calculation_data['project_1']['castings_black_consumption']:.3f}",
             f"{self.cost_calculation_data['project_2']['castings_black_consumption']:.3f}"],
            ["", " - отходы", "т",
             f"{self.cost_calculation_data['project_1']['castings_black_waste']:.4f}",
             f"{self.cost_calculation_data['project_2']['castings_black_waste']:.5f}"],
            ["2.2", "цветных металлов", "", "", ""],
            ["", " - расходы", "т",
             f"{self.cost_calculation_data['project_1']['castings_color_consumption']:.3f}",
             f"{self.cost_calculation_data['project_2']['castings_color_consumption']:.4f}"],
            ["", " - отходы", "т",
             f"{self.cost_calculation_data['project_1']['castings_color_waste']:.5f}",
             f"{self.cost_calculation_data['project_2']['castings_color_waste']:.6f}"],
            ["3", "покупные комплектующие изделия", "руб",
             f"{self.cost_calculation_data['project_1']['purchased_components']:.0f}",
             f"{self.cost_calculation_data['project_2']['purchased_components']:.0f}"],
            ["4", "Цена стального проката", "руб/т",
             f"{self.cost_calculation_data['project_1']['price_steel_rolling']:.0f}",
             f"{self.cost_calculation_data['project_2']['price_steel_rolling']:.0f}"],
            ["5", "Цена стальных труб", "руб/т",
             f"{self.cost_calculation_data['project_1']['price_steel_pipes']:.0f}",
             f"{self.cost_calculation_data['project_2']['price_steel_pipes']:.0f}"],
            ["6", "Цена отливок:", "", "", ""],
            ["", "-черных металлов", "руб/т",
             f"{self.cost_calculation_data['project_1']['price_castings_black']:.0f}",
             f"{self.cost_calculation_data['project_2']['price_castings_black']:.0f}"],
            ["", "-цветных металлов", "руб/т",
             f"{self.cost_calculation_data['project_1']['price_castings_color']:.0f}",
             f"{self.cost_calculation_data['project_2']['price_castings_color']:.0f}"],
            ["7", "Цена отходов:", "", "", ""],
            ["", "-стального проката", "руб/т",
             f"{self.cost_calculation_data['project_1']['price_waste_steel_rolling']:.0f}",
             f"{self.cost_calculation_data['project_2']['price_waste_steel_rolling']:.0f}"],
            ["", "-труб стальных", "руб/т",
             f"{self.cost_calculation_data['project_1']['price_waste_steel_pipes']:.0f}",
             f"{self.cost_calculation_data['project_2']['price_waste_steel_pipes']:.0f}"],
            ["", "-отливок черных металлов", "руб/т",
             f"{self.cost_calculation_data['project_1']['price_waste_castings_black']:.0f}",
             f"{self.cost_calculation_data['project_2']['price_waste_castings_black']:.0f}"],
            ["", "-отливок цветных металлов", "руб/т",
             f"{self.cost_calculation_data['project_1']['price_waste_castings_color']:.0f}",
             f"{self.cost_calculation_data['project_2']['price_waste_castings_color']:.0f}"],
            ["8", "Топливо и энергия на технологические потребности", "%",
             f"{self.cost_calculation_data['project_1']['fuel_energy_percent']:.1f}",
             f"{self.cost_calculation_data['project_2']['fuel_energy_percent']:.1f}"],
            ["9", "Суммарная трудоемкость изделия", "н-час",
             f"{self.cost_calculation_data['project_1']['labor_intensity']:.2f}",
             f"{self.cost_calculation_data['project_2']['labor_intensity']:.2f}"],
            ["10", "Часовая тарифная ставка", "руб",
             f"{self.cost_calculation_data['project_1']['hourly_rate']:.2f}",
             f"{self.cost_calculation_data['project_2']['hourly_rate']:.2f}"],
            ["11", "Дополнительная зарплата", "%",
             f"{self.cost_calculation_data['project_1']['additional_salary_percent']:.0f}",
             f"{self.cost_calculation_data['project_2']['additional_salary_percent']:.0f}"],
            ["12", "Отчисление на социальное страхование", "%",
             f"{self.cost_calculation_data['project_1']['social_insurance_percent']:.0f}",
             f"{self.cost_calculation_data['project_2']['social_insurance_percent']:.0f}"],
            ["13", "Расходы на содержание и эксплуатацию оборудования", "%",
             f"{self.cost_calculation_data['project_1']['equipment_maintenance_percent']:.0f}",
             f"{self.cost_calculation_data['project_2']['equipment_maintenance_percent']:.0f}"],
            ["14", "Общепроизводственные расходы", "%",
             f"{self.cost_calculation_data['project_1']['overhead_production_percent']:.0f}",
             f"{self.cost_calculation_data['project_2']['overhead_production_percent']:.0f}"],
            ["15", "Общехозяйственные расходы", "%",
             f"{self.cost_calculation_data['project_1']['general_business_percent']:.0f}",
             f"{self.cost_calculation_data['project_2']['general_business_percent']:.0f}"],
            ["16", "Внепроизводственные расходы", "%",
             f"{self.cost_calculation_data['project_1']['non_production_percent']:.0f}",
             f"{self.cost_calculation_data['project_2']['non_production_percent']:.0f}"],
            ["17", "Норматив рентабельности к себестоимости", "%",
             f"{self.cost_calculation_data['project_1']['profitability_percent']:.0f}",
             f"{self.cost_calculation_data['project_2']['profitability_percent']:.0f}"],
            ["18", "Годовой объем производства", "шт",
             f"{self.projects_data['project_1']['annual_volume_corrected']:.0f}",
             f"{self.projects_data['project_2']['annual_volume_corrected']:.0f}"]
        ]

        # Создаем CSV файл
        filename = "таблица_2_3_данные_для_расчета.csv"

        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            # Записываем заголовки
            writer.writerow(headers)

            # Записываем данные
            for row in rows:
                writer.writerow(row)

        print(f"Таблица 2.3 сохранена в файл: {filename}")
        return filename

    # def create_verification_report(self):
    #     """Создание отчета проверки расчетов"""
    #
    #     # Данные из примера студента (для проверки)
    #     student_data_project1 = {
    #         "material_costs": 11812.14,
    #         "semi_components": 154321.606,
    #         "fuel_energy": 2701.36,
    #         "basic_salary": 32612.36,
    #         "additional_salary": 13044.944,
    #         "social_insurance": 10044.61,
    #         "equipment_maintenance": 26089.89,
    #         "overhead_production": 29351.12,
    #         "general_business": 35873.60,
    #         "production_cost": 315851.87,
    #         "non_production": 9475.55,
    #         "full_cost": 325327.42,
    #         "profit": 71572.03,
    #         "wholesale_price": 396899.45,
    #         "annual_material": 4063.37,
    #         "annual_semi": 53086.63,
    #         "annual_fuel": 929.26,
    #         "annual_basic_salary": 11218.65,
    #         "annual_additional_salary": 4487.46,
    #         "annual_social": 3455.34,
    #         "annual_equipment": 8974.92,
    #         "annual_overhead": 10096.78,
    #         "annual_general": 12340.51,
    #         "annual_production": 108653.04,
    #         "annual_non_production": 3259.59,
    #         "annual_full_cost": 111912.64,
    #         "annual_profit": 24620.78
    #     }
    #
    #     student_data_project2 = {
    #         "material_costs": 11936.07,
    #         "semi_components": 157759.57,
    #         "fuel_energy": 2759.27,
    #         "basic_salary": 33353.55,
    #         "additional_salary": 13341.42,
    #         "social_insurance": 10272.89,
    #         "equipment_maintenance": 26682.84,
    #         "overhead_production": 30018.20,
    #         "general_business": 36688.91,
    #         "production_cost": 322812.72,
    #         "non_production": 9684.38,
    #         "full_cost": 332497.10,
    #         "profit": 73149.36,
    #         "wholesale_price": 405646.46
    #     }
    #
    #     print(f"\n{'═'*80}")
    #     print("ПРОВЕРКА РАСЧЕТОВ")
    #     print("(сравнение с данными из примера студента)")
    #     print(f"{'═'*80}")
    #
    #     # Проверяем Проект 1
    #     print(f"\n{'═'*80}")
    #     print("ПРОЕКТ 1 - СРАВНЕНИЕ С ПРИМЕРОМ СТУДЕНТА")
    #     print(f"{'═'*80}")
    #
    #     mismatches = []
    #
    #     for key, student_value in student_data_project1.items():
    #         if key in self.calculation_results["project_1"]:
    #             our_value = self.calculation_results["project_1"][key]
    #             difference = round(abs(our_value - student_value), 2)
    #
    #             if difference > 0.01:  # Допустимая погрешность
    #                 mismatches.append((key, our_value, student_value, difference))
    #                 print(f"  ❌ {key}: наш={our_value:.2f}, пример={student_value:.2f}, разница={difference:.2f}")
    #             else:
    #                 print(f"  ✅ {key}: наш={our_value:.2f}, пример={student_value:.2f} (совпадает)")
    #
    #     # Проверяем Проект 2
    #     print(f"\n{'═'*80}")
    #     print("ПРОЕКТ 2 - СРАВНЕНИЕ С ПРИМЕРОМ СТУДЕНТА")
    #     print(f"{'═'*80}")
    #
    #     for key, student_value in student_data_project2.items():
    #         if key in self.calculation_results["project_2"]:
    #             our_value = self.calculation_results["project_2"][key]
    #             difference = round(abs(our_value - student_value), 2)
    #
    #             if difference > 0.01:  # Допустимая погрешность
    #                 mismatches.append((f"project_2_{key}", our_value, student_value, difference))
    #                 print(f"  ❌ {key}: наш={our_value:.2f}, пример={student_value:.2f}, разница={difference:.2f}")
    #             else:
    #                 print(f"  ✅ {key}: наш={our_value:.2f}, пример={student_value:.2f} (совпадает)")
    #
    #     # Итог проверки
    #     print(f"\n{'═'*80}")
    #     print("ИТОГ ПРОВЕРКИ")
    #     print(f"{'═'*80}")
    #
    #     if not mismatches:
    #         print("✅ ВСЕ РАСЧЕТЫ СОВПАДАЮТ С ПРИМЕРОМ СТУДЕНТА!")
    #     else:
    #         print(f"⚠️  Обнаружено {len(mismatches)} расхождений:")
    #         for mismatch in mismatches:
    #             print(f"   - {mismatch[0]}: наш={mismatch[1]:.2f}, пример={mismatch[2]:.2f}, разница={mismatch[3]:.2f}")
    #
    #     # Создаем CSV файл с результатами проверки
    #     filename = "проверка_расчетов.csv"
    #
    #     headers = ["Показатель", "Наш расчет", "Пример студента", "Разница", "Статус"]
    #     rows = []
    #
    #     # Проект 1
    #     for key, student_value in student_data_project1.items():
    #         if key in self.calculation_results["project_1"]:
    #             our_value = self.calculation_results["project_1"][key]
    #             difference = round(abs(our_value - student_value), 2)
    #             status = "Совпадает" if difference <= 0.01 else "Расхождение"
    #             rows.append([f"Проект 1: {key}", f"{our_value:.2f}", f"{student_value:.2f}", f"{difference:.2f}", status])
    #
    #     # Проект 2
    #     for key, student_value in student_data_project2.items():
    #         if key in self.calculation_results["project_2"]:
    #             our_value = self.calculation_results["project_2"][key]
    #             difference = round(abs(our_value - student_value), 2)
    #             status = "Совпадает" if difference <= 0.01 else "Расхождение"
    #             rows.append([f"Проект 2: {key}", f"{our_value:.2f}", f"{student_value:.2f}", f"{difference:.2f}", status])
    #
    #     with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
    #         writer = csv.writer(csvfile, delimiter=';')
    #         writer.writerow(headers)
    #         for row in rows:
    #             writer.writerow(row)
    #
    #     print(f"\nОтчет проверки сохранен в файл: {filename}")
    #
    #     return len(mismatches)

def main():
    """Основная функция"""

    print("="*80)
    print("РАСЧЕТ ПРОЕКТНОЙ ЧАСТИ КУРСОВОЙ РАБОТЫ")
    print("Этап 1: Расчет себестоимости продукции")
    print("Используются данные из примера студента (вариант 3)")
    print("="*80)

    # Создаем экземпляр калькулятора
    calculator = CostCalculator()

    # Выполняем расчеты с промежуточными выводами
    calculator.calculate_all_costs()

    # Создаем таблицы CSV
    calculator.create_input_data_table_2_3()
    calculator.create_cost_table_2_4()

    # Проверяем расчеты
    #ismatches = calculator.create_verification_report()

    print(f"\n{'='*80}")
    print("ЭТАП 1 ЗАВЕРШЕН")
    print("="*80)
    print("Созданы файлы:")
    print("  - таблица_2_3_данные_для_расчета.csv")
    print("  - таблица_2_4_себестоимость.csv")
    print("  - проверка_расчетов.csv")
   # print(f"\nРезультат проверки: {mismatches} расхождений с примером студента")
    print("="*80)

if __name__ == "__main__":
    main()