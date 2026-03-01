
import sys
sys.path.append('/content')
from datetime import datetime

class StrategyAdvisorAgent:
    """
    Агент разработки стратегии взыскания.
    Формирует персонализированный план работы с должником.
    """

    def __init__(self):
        self.name = "🎯 Strategy Advisor"

    def advise(self, debtor_data: dict, risk_result: dict, compliance_result: dict) -> dict:
        """
        Разрабатывает стратегию взыскания.
        """
        print(f"\n[{self.name}] Разработка стратегии...")

        result = {
            "debtor_inn": debtor_data.get("inn", "unknown"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "strategy_type": "unknown",
            "channels": [],
            "frequency": "unknown",
            "tone": "unknown",
            "actions": [],
            "timeline": []
        }

        # Определяем тип стратегии по риску
        risk_level = risk_result.get("risk_level", "MEDIUM")

        if compliance_result.get("risk_level") == "critical":
            result["strategy_type"] = "COMPLIANCE_STOP"
            result["tone"] = "Нейтральный (только письменная коммуникация)"
            result["actions"] = ["Приостановить активное взыскание", "Передать юристу"]

        elif risk_level == "CRITICAL":
            result["strategy_type"] = "AGGRESSIVE_LEGAL"
            result["channels"] = ["Суд", "Арест активов", "Письмо"]
            result["frequency"] = "Ежедневно"
            result["tone"] = "Официальный, строгий"
            result["actions"] = [
                "Подготовка искового заявления",
                "Ходатайство об аресте счетов",
                "Уведомление о передаче коллекторам"
            ]

        elif risk_level == "HIGH":
            result["strategy_type"] = "PRETRIAL_PRESSURE"
            result["channels"] = ["Звонок", "Письмо", "SMS"]
            result["frequency"] = "3 раза в неделю"
            result["tone"] = "Настойчивый, но в рамках 230-ФЗ"
            result["actions"] = [
                "Досудебная претензия",
                "Серия звонков с напоминанием",
                "Предложение реструктуризации"
            ]

        elif risk_level == "MEDIUM":
            result["strategy_type"] = "NEGOTIATION"
            result["channels"] = ["Звонок", "Email"]
            result["frequency"] = "2 раза в неделю"
            result["tone"] = "Партнерский, конструктивный"
            result["actions"] = [
                "Переговоры о графике платежей",
                "Предложение скидки при досрочном погашении",
                "Мониторинг платежей"
            ]

        elif risk_level == "LOW":
            result["strategy_type"] = "SOFT_REMINDER"
            result["channels"] = ["SMS", "Email", "Push"]
            result["frequency"] = "1 раз в неделю"
            result["tone"] = "Дружелюбный, напоминающий"
            result["actions"] = [
                "SMS-напоминание о платеже",
                "Email с реквизитами",
                "Звонок через 14 дней"
            ]

        else:
            result["strategy_type"] = "MONITORING"
            result["channels"] = ["Мониторинг"]
            result["frequency"] = "1 раз в месяц"
            result["tone"] = "Пассивный"
            result["actions"] = ["Периодическая проверка реестров"]

        # Формируем таймлайн
        result["timeline"] = self._generate_timeline(result)

        print(f"  ├─ Тип стратегии: {result['strategy_type']}")
        print(f"  ├─ Каналы: {', '.join(result['channels'])}")
        print(f"  └─ Частота: {result['frequency']}")

        return result

    def _generate_timeline(self, strategy: dict) -> list:
        """
        Генерирует таймлайн действий.
        """
        timeline = []

        if strategy["strategy_type"] == "AGGRESSIVE_LEGAL":
            timeline = [
                "День 1: Отправка претензии",
                "День 3: Первый звонок",
                "День 7: Второй звонок + Email",
                "День 14: Подача иска в суд",
                "День 30: Ходатайство об аресте"
            ]
        elif strategy["strategy_type"] == "PRETRIAL_PRESSURE":
            timeline = [
                "День 1: Досудебная претензия",
                "День 2: Звонок",
                "День 5: SMS-напоминание",
                "День 10: Второй звонок",
                "День 20: Уведомление о передаче в суд"
            ]
        elif strategy["strategy_type"] == "NEGOTIATION":
            timeline = [
                "День 1: Звонок с предложением",
                "День 3: Отправка графика платежей",
                "День 7: Контрольный звонок",
                "День 14: Подтверждение оплаты",
                "День 30: Закрытие дела"
            ]
        else:
            timeline = [
                "День 1: SMS-напоминание",
                "День 7: Email",
                "День 30: Проверка статуса"
            ]

        return timeline


# Тестирование
if __name__ == "__main__":
    agent = StrategyAdvisorAgent()
    test_data = {"inn": "7712345678"}
    test_risk = {"risk_level": "HIGH"}
    test_compliance = {"risk_level": "low"}

    result = agent.advise(test_data, test_risk, test_compliance)
    print(f"\nСтратегия: {result['strategy_type']}")
    print(f"Действия: {result['actions']}")
