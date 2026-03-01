
import sys
sys.path.append('/content')
from datetime import datetime, timedelta

class ComplianceCheckerAgent:
    """
    Агент проверки соблюдения 230-ФЗ о взыскании долгов.
    Анализирует действия коллекторов на наличие нарушений.
    """

    def __init__(self):
        self.name = "⚖️ Compliance Checker"

        # Лимиты по 230-ФЗ
        self.max_calls_per_week = 2
        self.max_calls_per_month = 8
        self.max_sms_per_week = 2
        self.call_start_hour = 8
        self.call_end_hour = 22
        self.weekend_call_allowed = False

    def check(self, debtor_data: dict) -> dict:
        """
        Проверяет все действия по должнику на соответствие 230-ФЗ.

        Args:
            debtor_data: Данные от Data Collector

        Returns:
            dict: Результат проверки с нарушениями и рекомендациями
        """
        print(f"\n[{self.name}] Запуск проверки 230-ФЗ...")

        result = {
            "debtor_inn": debtor_data.get("inn", "unknown"),
            "check_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "violations": [],
            "warnings": [],
            "risk_level": "low",
            "recommendation": "Действия разрешены",
            "details": {}
        }

        # 1. Проверка истории звонков
        call_history = debtor_data.get("sources", {}).get("calls", [])
        call_check = self._check_calls(call_history)
        result["details"]["calls"] = call_check
        result["violations"].extend(call_check["violations"])
        result["warnings"].extend(call_check["warnings"])

        # 2. Проверка статуса должника (банкротство)
        court_data = debtor_data.get("sources", {}).get("court", {})
        bankruptcy_check = self._check_bankruptcy(court_data)
        result["details"]["bankruptcy"] = bankruptcy_check
        result["violations"].extend(bankruptcy_check["violations"])
        result["warnings"].extend(bankruptcy_check["warnings"])

        # 3. Проверка статуса компании
        egrul_data = debtor_data.get("sources", {}).get("egrul", {})
        company_check = self._check_company_status(egrul_data)
        result["details"]["company"] = company_check
        result["warnings"].extend(company_check["warnings"])

        # 4. Определение уровня риска
        result["risk_level"] = self._calculate_risk_level(result)

        # 5. Формирование рекомендации
        result["recommendation"] = self._generate_recommendation(result)

        print(f"  ├─ Нарушения: {len(result['violations'])}")
        print(f"  ├─ Предупреждения: {len(result['warnings'])}")
        print(f"  └─ Уровень риска: {result['risk_level'].upper()}")

        return result

    def _check_calls(self, call_history: list) -> dict:
        """
        Проверка истории звонков на нарушения 230-ФЗ.
        """
        result = {"violations": [], "warnings": [], "stats": {}}

        if not call_history:
            result["stats"] = {"total_calls": 0, "this_week": 0}
            return result

        # Считаем звонки за неделю
        today = datetime.now()
        week_ago = today - timedelta(days=7)

        calls_this_week = []
        for call in call_history:
            call_date = datetime.strptime(call["date"], "%Y-%m-%d")
            if call_date >= week_ago:
                calls_this_week.append(call)

        result["stats"] = {
            "total_calls": len(call_history),
            "this_week": len(calls_this_week)
        }

        # Проверка лимита звонков
        if len(calls_this_week) > self.max_calls_per_week:
            result["violations"].append(
                f"Превышен лимит звонков: {len(calls_this_week)} за неделю (лимит: {self.max_calls_per_week})"
            )

        # Проверка времени звонков
        for call in calls_this_week:
            hour = int(call["time"].split(":")[0])
            if hour < self.call_start_hour or hour >= self.call_end_hour:
                result["violations"].append(
                    f"Звонок в запрещенное время: {call['date']} {call['time']}"
                )

        return result

    def _check_bankruptcy(self, court_data: dict) -> dict:
        """
        Проверка на наличие дела о банкротстве.
        """
        result = {"violations": [], "warnings": [], "status": "no_cases"}

        if not court_data.get("cases"):
            return result

        for case in court_data["cases"]:
            if "Банкротство" in case.get("type", ""):
                result["status"] = "bankruptcy_found"
                result["violations"].append(
                    f"Обнаружено дело о банкротстве: {case['number']}. "
                    "Взыскание должно быть приостановлено!"
                )
                break

        return result

    def _check_company_status(self, egrul_data: dict) -> dict:
        """
        Проверка статуса компании по ЕГРЮЛ.
        """
        result = {"violations": [], "warnings": [], "status": "unknown"}

        status = egrul_data.get("status", "unknown")
        result["status"] = status

        if status == "Ликвидация":
            result["warnings"].append(
                "Компания в ликвидации. Требуется особый порядок взыскания."
            )
        elif status == "Реорганизация":
            result["warnings"].append(
                "Компания в реорганизации. Необходимо уточнить правопреемника."
            )

        return result

    def _calculate_risk_level(self, result: dict) -> str:
        """
        Вычисляет общий уровень риска.
        """
        if len(result["violations"]) > 0:
            return "critical"
        elif len(result["warnings"]) > 2:
            return "high"
        elif len(result["warnings"]) > 0:
            return "medium"
        else:
            return "low"

    def _generate_recommendation(self, result: dict) -> str:
        """
        Генерирует рекомендацию на основе проверки.
        """
        if result["risk_level"] == "critical":
            return "🛑 НЕМЕДЛЕННО ПРЕКРАТИТЬ взыскание! Есть нарушения 230-ФЗ."
        elif result["risk_level"] == "high":
            return "⚠️ Требуется ручная проверка перед продолжением взыскания."
        elif result["risk_level"] == "medium":
            return "⚡ Можно продолжать с осторожностью. Учтите предупреждения."
        else:
            return "✅ Действия соответствуют 230-ФЗ. Можно продолжать взыскание."


# Тестирование агента
if __name__ == "__main__":
    # Тестовые данные
    test_data = {
        "inn": "7712345678",
        "sources": {
            "calls": [
                {"date": "2026-03-01", "time": "10:00", "result": "Дозвон"},
                {"date": "2026-03-03", "time": "14:00", "result": "Дозвон"},
                {"date": "2026-03-05", "time": "09:00", "result": "Дозвон"}  # 3-й звонок за неделю!
            ],
            "court": {
                "cases": [
                    {"number": "А40-12345/2026", "type": "Банкротство", "status": "Рассмотрение"}
                ]
            },
            "egrul": {
                "status": "Действующая"
            }
        }
    }

    agent = ComplianceCheckerAgent()
    result = agent.check(test_data)

    print("\n" + "=" * 60)
    print("📋 ОТЧЕТ COMPLIANCE CHECKER")
    print("=" * 60)
    print(f"ИНН: {result['debtor_inn']}")
    print(f"Дата проверки: {result['check_date']}")
    print(f"\nНарушения: {len(result['violations'])}")
    for v in result['violations']:
        print(f"  ❌ {v}")
    print(f"\nПредупреждения: {len(result['warnings'])}")
    for w in result['warnings']:
        print(f"  ⚠️ {w}")
    print(f"\nУровень риска: {result['risk_level'].upper()}")
    print(f"\nРекомендация: {result['recommendation']}")
    print("=" * 60)
