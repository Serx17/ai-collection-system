
import sys
sys.path.append('/content')
from datetime import datetime

class PrivacyGuardianAgent:
    """
    Агент защиты персональных данных (152-ФЗ).
    Контролирует безопасность обработки данных должника.
    """

    def __init__(self):
        self.name = "🔐 Privacy Guardian"

        # Требования 152-ФЗ
        self.requirements = [
            "Данные хранятся в РФ",
            "Доступ только авторизованным лицам",
            "Логирование всех операций",
            "Шифрование при передаче",
            "Согласие на обработку данных"
        ]

    def check(self, debtor_data: dict, system_config: dict = None) -> dict:
        """
        Проверяет соответствие обработки данных 152-ФЗ.
        """
        print(f"\n[{self.name}] Проверка 152-ФЗ...")

        result = {
            "debtor_inn": debtor_data.get("inn", "unknown"),
            "check_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "compliance_status": "unknown",
            "checks": [],
            "violations": [],
            "recommendations": []
        }

        # Имитация проверок (в продакшене — реальные проверки)
        checks = [
            {"name": "Локализация данных", "status": "PASS", "note": "Сервер в РФ"},
            {"name": "Шифрование данных", "status": "PASS", "note": "TLS 1.3"},
            {"name": "Контроль доступа", "status": "PASS", "note": "2FA включен"},
            {"name": "Логирование", "status": "PASS", "note": "Все операции логируются"},
            {"name": "Согласие на обработку", "status": "CHECK", "note": "Требуется проверка договора"}
        ]

        result["checks"] = checks

        # Подсчитываем статус
        passed = sum(1 for c in checks if c["status"] == "PASS")
        total = len(checks)

        if passed == total:
            result["compliance_status"] = "COMPLIANT"
        elif passed >= total - 1:
            result["compliance_status"] = "MOSTLY_COMPLIANT"
            result["recommendations"].append("Проверить согласие на обработку данных")
        else:
            result["compliance_status"] = "NON_COMPLIANT"
            result["violations"].append("Критические нарушения 152-ФЗ")

        print(f"  ├─ Проверок: {total}")
        print(f"  ├─ Пройдено: {passed}")
        print(f"  └─ Статус: {result['compliance_status']}")

        return result

    def get_requirements(self) -> list:
        """
        Возвращает список требований 152-ФЗ.
        """
        return self.requirements


# Тестирование
if __name__ == "__main__":
    agent = PrivacyGuardianAgent()
    test_data = {"inn": "7712345678"}

    result = agent.check(test_data)
    print(f"\nСтатус: {result['compliance_status']}")
    print(f"Требования: {agent.get_requirements()}")
