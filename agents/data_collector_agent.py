
import sys
sys.path.append('/content')

from mocks.mock_data_generator import MockDataGenerator

class DataCollectorAgent:
    """
    Агент сбора данных о должнике.
    Имитирует запросы к ФССП, арбитражным судам и ЕГРЮЛ.
    """

    def __init__(self):
        self.mock_generator = MockDataGenerator()
        self.name = "🔍 Data Collector"

    def collect(self, inn: str, company_name: str = None) -> dict:
        """
        Собирает все доступные данные о должнике по ИНН.

        Args:
            inn: ИНН должника
            company_name: Название компании (опционально)

        Returns:
            dict: Собранные данные из всех источников
        """
        print(f"\n[{self.name}] Запуск сбора данных по ИНН: {inn}")

        result = {
            "inn": inn,
            "company_name": company_name or "Не указано",
            "sources": {},
            "summary": {}
        }

        # 1. Запрос к ФССП
        print(f"  ├─ Запрос ФССП...")
        fssp_data = self.mock_generator.generate_fssp_data(inn)
        result["sources"]["fssp"] = fssp_data
        print(f"  │  Статус: {fssp_data['status']}")

        # 2. Запрос к арбитражным судам
        print(f"  ├─ Запрос арбитражных судов...")
        court_data = self.mock_generator.generate_court_data(inn)
        result["sources"]["court"] = court_data
        print(f"  │  Статус: {court_data['status']}")

        # 3. Запрос к ЕГРЮЛ
        print(f"  ├─ Запрос ЕГРЮЛ...")
        egrul_data = self.mock_generator.generate_egrul_data(inn)
        result["sources"]["egrul"] = egrul_data
        print(f"  │  Статус: {egrul_data['status']}")

        # 4. История звонков
        print(f"  ├─ Запрос истории звонков...")
        call_history = self.mock_generator.generate_call_history(inn)
        result["sources"]["calls"] = call_history
        print(f"  │  Найдено звонков: {len(call_history)}")

        # Формируем краткую сводку
        result["summary"] = self._create_summary(result["sources"])

        print(f"  └─ Сбор данных завершен!")

        return result

    def _create_summary(self, sources: dict) -> dict:
        """
        Создает краткую сводку по всем источникам.
        """
        summary = {
            "total_debt": 0,
            "total_cases": 0,
            "company_status": "unknown",
            "risk_flags": []
        }

        # Долги ФССП
        if sources["fssp"].get("total_debt"):
            summary["total_debt"] = sources["fssp"]["total_debt"]
            summary["risk_flags"].append("Есть исполнительное производство")

        # Судебные дела
        if sources["court"].get("total_cases"):
            summary["total_cases"] = sources["court"]["total_cases"]
            # Проверка на банкротство
            for case in sources["court"].get("cases", []):
                if "Банкротство" in case.get("type", ""):
                    summary["risk_flags"].append("⚠️ Дело о банкротстве!")

        # Статус компании
        if sources["egrul"].get("status"):
            summary["company_status"] = sources["egrul"]["status"]
            if sources["egrul"]["status"] != "Действующая":
                summary["risk_flags"].append("⚠️ Компания в ликвидации/реорганизации")

        return summary


# Тестирование агента
if __name__ == "__main__":
    agent = DataCollectorAgent()
    result = agent.collect("7712345678", "ООО \"Тестовая Компания\"")

    print("\n" + "=" * 60)
    print("📊 СВОДКА ПО ДОЛЖНИКУ")
    print("=" * 60)
    print(f"ИНН: {result['inn']}")
    print(f"Компания: {result['company_name']}")
    print(f"Общий долг: {result['summary']['total_debt']:,} ₽")
    print(f"Судебных дел: {result['summary']['total_cases']}")
    print(f"Статус компании: {result['summary']['company_status']}")
    print(f"\nФлаги риска:")
    for flag in result['summary']['risk_flags']:
        print(f"  • {flag}")
    print("=" * 60)
