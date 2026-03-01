
import random
from datetime import datetime, timedelta

class MockDataGenerator:
    """
    Генератор тестовых данных для демонстрации системы.
    Имитирует ответы от ФССП, арбитражных судов и ЕГРЮЛ.
    """

    def __init__(self):
        self.first_names = ["Иван", "Петр", "Сергей", "Александр", "Дмитрий", "Андрей"]
        self.last_names = ["Иванов", "Петров", "Сидоров", "Козлов", "Смирнов", "Волков"]
        self.company_names = [
            "ООО \"Рога и Копыта\"",
            "ООО \"Вектор\"",
            "АО \"Прогресс\"",
            "ООО \"Финанс Групп\"",
            "ИП Смирнов А.В."
        ]

    def generate_fssp_data(self, inn: str) -> dict:
        """
        Имитация ответа от ФССП
        """
        # Генерируем случайные данные
        has_debt = random.choice([True, False, False])  # 33% шанс долга

        if not has_debt:
            return {
                "status": "no_debt",
                "message": "Исполнительные производства не найдены",
                "data": None
            }

        # Генерируем данные о долге
        debt_amount = random.choice([50000, 150000, 500000, 1500000, 3000000])
        days_overdue = random.randint(30, 365)

        return {
            "status": "active",
            "executive_proceedings": [
                {
                    "number": f"{random.randint(10000, 99999)}/{random.randint(20, 26)}/{random.randint(77, 99)}-ИП",
                    "amount": debt_amount,
                    "date": (datetime.now() - timedelta(days=days_overdue)).strftime("%Y-%m-%d"),
                    "reason": "Неисполнение обязательств по договору",
                    "department": f"ОСП-{random.randint(1, 10)} г. Москвы"
                }
            ],
            "total_debt": debt_amount,
            "days_overdue": days_overdue
        }

    def generate_court_data(self, inn: str) -> dict:
        """
        Имитация ответа из арбитражного суда
        """
        has_cases = random.choice([True, False, False, False])  # 25% шанс дел

        if not has_cases:
            return {
                "status": "no_cases",
                "message": "Дела в арбитражных судах не найдены",
                "data": []
            }

        # Генерируем судебные дела
        cases = []
        num_cases = random.randint(1, 3)

        for i in range(num_cases):
            case_number = f"А40-{random.randint(10000, 99999)}/{random.randint(2024, 2026)}"
            case_type = random.choice([
                "Банкротство",
                "Взыскание задолженности",
                "Признание сделки недействительной",
                "Корпоративный спор"
            ])

            cases.append({
                "number": case_number,
                "type": case_type,
                "status": random.choice(["Рассмотрение", "Решение вынесено", "Исполнение"]),
                "date": (datetime.now() - timedelta(days=random.randint(10, 200))).strftime("%Y-%m-%d"),
                "amount": random.choice([100000, 500000, 1000000, 2000000]),
                "court": random.choice([
                    "Арбитражный суд г. Москвы",
                    "Арбитражный суд Московской области",
                    "Девятый арбитражный апелляционный суд"
                ])
            })

        return {
            "status": "found",
            "cases": cases,
            "total_cases": len(cases)
        }

    def generate_egrul_data(self, inn: str) -> dict:
        """
        Имитация ответа из ЕГРЮЛ
        """
        return {
            "status": "active",
            "company_name": random.choice(self.company_names),
            "inn": inn,
            "ogrn": f"1{random.randint(1000000000000, 9999999999999)}",
            "registration_date": f"{random.randint(2010, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "status": random.choice(["Действующая", "Ликвидация", "Реорганизация"]),
            "director": f"{random.choice(self.last_names)} {random.choice(self.first_names)} {random.choice(self.first_names)[0]}."
        }

    def generate_call_history(self, debtor_id: str) -> list:
        """
        Генерация истории звонков должнику
        """
        num_calls = random.randint(0, 5)
        calls = []

        for i in range(num_calls):
            call_date = datetime.now() - timedelta(days=random.randint(0, 14))
            call_hour = random.randint(8, 21)  # В разрешенное время
            call_minute = random.randint(0, 59)

            calls.append({
                "date": call_date.strftime("%Y-%m-%d"),
                "time": f"{call_hour:02d}:{call_minute:02d}",
                "duration": random.randint(30, 600),  # секунды
                "result": random.choice(["Дозвон", "Нет ответа", "Обещание оплатить", "Агрессия"]),
                "operator": f"Оператор_{random.randint(1, 10)}"
            })

        return sorted(calls, key=lambda x: x["date"], reverse=True)


# Тестирование
if __name__ == "__main__":
    generator = MockDataGenerator()

    # Тест ФССП
    print("📊 Тест ФССП:")
    fssp_data = generator.generate_fssp_data("7712345678")
    print(f"  Статус: {fssp_data['status']}")
    if fssp_data.get('total_debt'):
        print(f"  Долг: {fssp_data['total_debt']:,} ₽")
        print(f"  Дней просрочки: {fssp_data['days_overdue']}")

    # Тест суда
    print("\n⚖️ Тест арбитражного суда:")
    court_data = generator.generate_court_data("7712345678")
    print(f"  Статус: {court_data['status']}")
    if court_data.get('total_cases'):
        print(f"  Найдено дел: {court_data['total_cases']}")

    # Тест ЕГРЮЛ
    print("\n📄 Тест ЕГРЮЛ:")
    egrul_data = generator.generate_egrul_data("7712345678")
    print(f"  Компания: {egrul_data['company_name']}")
    print(f"  Статус: {egrul_data['status']}")

    print("\n✅ Mock-генератор работает!")
