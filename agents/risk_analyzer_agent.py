
import sys
sys.path.append('/content')
from datetime import datetime

class RiskAnalyzerAgent:
    """
    Агент анализа рисков должника.
    Оценивает вероятность возврата долга и приоритет работы.
    """

    def __init__(self):
        self.name = "📊 Risk Analyzer"

        # Весовые коэффициенты для оценки риска
        self.weights = {
            "debt_amount": 0.25,      # Сумма долга
            "days_overdue": 0.25,     # Дней просрочки
            "court_cases": 0.20,      # Судебные дела
            "bankruptcy": 0.20,       # Банкротство
            "company_status": 0.10    # Статус компании
        }

    def analyze(self, debtor_data: dict, compliance_result: dict) -> dict:
        """
        Анализирует риск должника и рассчитывает приоритет.

        Args:
            debtor_data: Данные от Data Collector
            compliance_result: Результат проверки Compliance Checker

        Returns:
            dict: Оценка риска и рекомендации по стратегии
        """
        print(f"\n[{self.name}] Запуск анализа рисков...")

        result = {
            "debtor_inn": debtor_data.get("inn", "unknown"),
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "scores": {},
            "total_score": 0,
            "risk_level": "unknown",
            "recovery_probability": 0,
            "priority": "unknown",
            "strategy": "unknown",
            "details": {}
        }

        # 1. Анализ суммы долга
        debt_score = self._analyze_debt_amount(debtor_data)
        result["scores"]["debt_amount"] = debt_score
        result["details"]["debt_amount"] = debt_score["details"]

        # 2. Анализ просрочки
        overdue_score = self._analyze_overdue(debtor_data)
        result["scores"]["days_overdue"] = overdue_score
        result["details"]["days_overdue"] = overdue_score["details"]

        # 3. Анализ судебных дел
        court_score = self._analyze_court_cases(debtor_data)
        result["scores"]["court_cases"] = court_score
        result["details"]["court_cases"] = court_score["details"]

        # 4. Анализ банкротства
        bankruptcy_score = self._analyze_bankruptcy(debtor_data)
        result["scores"]["bankruptcy"] = bankruptcy_score
        result["details"]["bankruptcy"] = bankruptcy_score["details"]

        # 5. Анализ статуса компании
        company_score = self._analyze_company_status(debtor_data)
        result["scores"]["company_status"] = company_score
        result["details"]["company_status"] = company_score["details"]

        # 6. Расчет общего scores
        result["total_score"] = self._calculate_total_score(result["scores"])

        # 7. Определение уровня риска
        result["risk_level"] = self._determine_risk_level(result["total_score"])

        # 8. Расчет вероятности возврата
        result["recovery_probability"] = self._calculate_recovery_probability(result)

        # 9. Определение приоритета
        result["priority"] = self._determine_priority(result)

        # 10. Рекомендация стратегии
        result["strategy"] = self._generate_strategy(result, compliance_result)

        print(f"  ├─ Общий score: {result['total_score']:.2f}")
        print(f"  ├─ Уровень риска: {result['risk_level']}")
        print(f"  ├─ Вероятность возврата: {result['recovery_probability']:.1f}%")
        print(f"  └─ Приоритет: {result['priority']}")

        return result

    def _analyze_debt_amount(self, debtor_data: dict) -> dict:
        """
        Анализ суммы долга (0-100 баллов).
        Больше долг = выше приоритет взыскания.
        """
        fssp = debtor_data.get("sources", {}).get("fssp", {})
        debt = fssp.get("total_debt", 0)

        if debt == 0:
            score = 0
            details = "Долг не обнаружен"
        elif debt < 100000:
            score = 30
            details = f"Малый долг: {debt:,} ₽"
        elif debt < 500000:
            score = 50
            details = f"Средний долг: {debt:,} ₽"
        elif debt < 1000000:
            score = 70
            details = f"Крупный долг: {debt:,} ₽"
        else:
            score = 100
            details = f"Особо крупный долг: {debt:,} ₽"

        return {"score": score, "details": details, "value": debt}

    def _analyze_overdue(self, debtor_data: dict) -> dict:
        """
        Анализ дней просрочки (0-100 баллов).
        Больше просрочка = выше риск невозврата.
        """
        fssp = debtor_data.get("sources", {}).get("fssp", {})
        days = fssp.get("days_overdue", 0)

        if days == 0:
            score = 0
            details = "Просрочка не обнаружена"
        elif days < 90:
            score = 30
            details = f"Ранняя просрочка: {days} дней"
        elif days < 180:
            score = 50
            details = f"Средняя просрочка: {days} дней"
        elif days < 365:
            score = 75
            details = f"Длительная просрочка: {days} дней"
        else:
            score = 100
            details = f"Критическая просрочка: {days} дней"

        return {"score": score, "details": details, "value": days}

    def _analyze_court_cases(self, debtor_data: dict) -> dict:
        """
        Анализ судебных дел (0-100 баллов).
        Больше дел = выше риск.
        """
        court = debtor_data.get("sources", {}).get("court", {})
        cases = court.get("cases", [])
        num_cases = len(cases)

        if num_cases == 0:
            score = 0
            details = "Судебных дел нет"
        elif num_cases == 1:
            score = 40
            details = f"1 судебное дело"
        elif num_cases <= 3:
            score = 70
            details = f"{num_cases} судебных дела"
        else:
            score = 100
            details = f"{num_cases}+ судебных дел (критично)"

        return {"score": score, "details": details, "value": num_cases}

    def _analyze_bankruptcy(self, debtor_data: dict) -> dict:
        """
        Анализ риска банкротства (0-100 баллов).
        Банкротство = максимальный риск.
        """
        court = debtor_data.get("sources", {}).get("court", {})
        cases = court.get("cases", [])

        has_bankruptcy = any("Банкротство" in case.get("type", "") for case in cases)

        if has_bankruptcy:
            score = 100
            details = "⚠️ ОБНАРУЖЕНО ДЕЛО О БАНКРОТСТВЕ!"
        else:
            score = 0
            details = "Дел о банкротстве нет"

        return {"score": score, "details": details, "value": 1 if has_bankruptcy else 0}

    def _analyze_company_status(self, debtor_data: dict) -> dict:
        """
        Анализ статуса компании (0-100 баллов).
        Ликвидация = высокий риск.
        """
        egrul = debtor_data.get("sources", {}).get("egrul", {})
        status = egrul.get("status", "unknown")

        if status == "Действующая":
            score = 0
            details = "Компания действующая"
        elif status == "Реорганизация":
            score = 50
            details = "⚠️ Компания в реорганизации"
        elif status == "Ликвидация":
            score = 100
            details = "🛑 Компания в ликвидации"
        else:
            score = 75
            details = f"Статус: {status}"

        return {"score": score, "details": details, "value": status}

    def _calculate_total_score(self, scores: dict) -> float:
        """
        Расчет общего scores с весовыми коэффициентами.
        """
        total = 0
        for key, weight in self.weights.items():
            if key in scores:
                total += scores[key]["score"] * weight
        return total

    def _determine_risk_level(self, total_score: float) -> str:
        """
        Определение уровня риска по общему scores.
        """
        if total_score >= 80:
            return "CRITICAL"
        elif total_score >= 60:
            return "HIGH"
        elif total_score >= 40:
            return "MEDIUM"
        elif total_score >= 20:
            return "LOW"
        else:
            return "MINIMAL"

    def _calculate_recovery_probability(self, result: dict) -> float:
        """
        Расчет вероятности возврата долга (0-100%).
        Обратная зависимость от риска.
        """
        # Базовая вероятность 80%, уменьшается с ростом риска
        base_probability = 80
        risk_reduction = result["total_score"] * 0.7
        probability = max(5, base_probability - risk_reduction)
        return probability

    def _determine_priority(self, result: dict) -> str:
        """
        Определение приоритета работы с должником.
        """
        if result["risk_level"] == "CRITICAL":
            return "🔴 P0 - Немедленное действие"
        elif result["risk_level"] == "HIGH":
            return "🟠 P1 - Высокий приоритет"
        elif result["risk_level"] == "MEDIUM":
            return "🟡 P2 - Средний приоритет"
        elif result["risk_level"] == "LOW":
            return "🟢 P3 - Низкий приоритет"
        else:
            return "⚪ P4 - Мониторинг"

    def _generate_strategy(self, result: dict, compliance_result: dict) -> str:
        """
        Генерация стратегии взыскания.
        """
        # Сначала проверяем compliance
        if compliance_result.get("risk_level") == "critical":
            return "🛑 СТОП: Нарушения 230-ФЗ. Требуется ручная проверка."

        # Затем по риску должника
        if result["risk_level"] == "CRITICAL":
            return "⚡ СРОЧНО: Подготовка иска + арест активов"
        elif result["risk_level"] == "HIGH":
            return "📋 Досудебная претензия + усиленный контроль"
        elif result["risk_level"] == "MEDIUM":
            return "📞 Телефонные переговоры + реструктуризация"
        elif result["risk_level"] == "LOW":
            return "✉️ SMS/Email напоминания + мягкий контакт"
        else:
            return "📊 Мониторинг без активных действий"


# Тестирование агента
if __name__ == "__main__":
    # Тестовые данные
    test_debtor_data = {
        "inn": "7712345678",
        "sources": {
            "fssp": {"total_debt": 1500000, "days_overdue": 187},
            "court": {"cases": [{"type": "Банкротство"}]},
            "egrul": {"status": "Действующая"}
        }
    }

    test_compliance = {
        "risk_level": "low",
        "violations": []
    }

    agent = RiskAnalyzerAgent()
    result = agent.analyze(test_debtor_data, test_compliance)

    print("\n" + "=" * 60)
    print("📊 ОТЧЕТ RISK ANALYZER")
    print("=" * 60)
    print(f"ИНН: {result['debtor_inn']}")
    print(f"Общий score: {result['total_score']:.2f}")
    print(f"Уровень риска: {result['risk_level']}")
    print(f"Вероятность возврата: {result['recovery_probability']:.1f}%")
    print(f"Приоритет: {result['priority']}")
    print(f"\nСтратегия: {result['strategy']}")
    print("=" * 60)
