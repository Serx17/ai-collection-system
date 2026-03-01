
import sys
sys.path.append('/content')
from datetime import datetime
import json

from agents.data_collector_agent import DataCollectorAgent
from agents.compliance_checker_agent import ComplianceCheckerAgent
from agents.risk_analyzer_agent import RiskAnalyzerAgent
from agents.strategy_advisor_agent import StrategyAdvisorAgent
from agents.script_generator_agent import ScriptGeneratorAgent
from agents.privacy_guardian_agent import PrivacyGuardianAgent
from agents.report_builder_agent import ReportBuilderAgent

class FullOrchestrator:
    """
    Полный оркестратор мультиагентной системы (7 агентов).
    """

    def __init__(self):
        self.name = "🎯 Оркестратор v2.0"

        # Инициализируем ВСЕХ 7 агентов
        self.collector = DataCollectorAgent()
        self.compliance = ComplianceCheckerAgent()
        self.analyzer = RiskAnalyzerAgent()
        self.strategy = StrategyAdvisorAgent()
        self.script = ScriptGeneratorAgent()
        self.privacy = PrivacyGuardianAgent()
        self.report = ReportBuilderAgent()

        self.stats = {"total": 0, "success": 0, "failed": 0}

    def process(self, inn: str, company_name: str = None) -> dict:
        """
        Полный цикл обработки через всех 7 агентов.
        """
        self.stats["total"] += 1
        start_time = datetime.now()

        print("\n" + "=" * 60)
        print(f"[{self.name}] ЗАПУСК ПОЛНОГО ЦИКЛА")
        print("=" * 60)
        print(f"ИНН: {inn} | Компания: {company_name or 'N/A'}")
        print("=" * 60)

        result = {
            "request_id": f"REQ-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "inn": inn,
            "company_name": company_name,
            "timestamp": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "agents": {},
            "final_decision": {},
            "execution_time": 0
        }

        try:
            # АГЕНТ 1: Сбор данных
            print("\n🔄 АГЕНТ 1/7: Сбор данных...")
            result["agents"]["collector"] = self.collector.collect(inn, company_name)

            # АГЕНТ 2: Комплаенс
            print("\n🔄 АГЕНТ 2/7: Проверка 230-ФЗ...")
            result["agents"]["compliance"] = self.compliance.check(result["agents"]["collector"])

            # АГЕНТ 3: Риски
            print("\n🔄 АГЕНТ 3/7: Анализ рисков...")
            result["agents"]["analyzer"] = self.analyzer.analyze(
                result["agents"]["collector"],
                result["agents"]["compliance"]
            )

            # АГЕНТ 4: Стратегия
            print("\n🔄 АГЕНТ 4/7: Разработка стратегии...")
            result["agents"]["strategy"] = self.strategy.advise(
                result["agents"]["collector"],
                result["agents"]["analyzer"],
                result["agents"]["compliance"]
            )

            # АГЕНТ 5: Скрипты
            print("\n🔄 АГЕНТ 5/7: Генерация скриптов...")
            result["agents"]["script"] = self.script.generate(
                result["agents"]["collector"],
                result["agents"]["strategy"],
                "call"
            )

            # АГЕНТ 6: Приватность
            print("\n🔄 АГЕНТ 6/7: Проверка 152-ФЗ...")
            result["agents"]["privacy"] = self.privacy.check(result["agents"]["collector"])

            # АГЕНТ 7: Отчет
            print("\n🔄 АГЕНТ 7/7: Формирование отчета...")
            result["agents"]["report"] = self.report.build(result, "telegram")

            # Финальное решение
            result["final_decision"] = self._make_decision(result["agents"])
            self.stats["success"] += 1

        except Exception as e:
            self.stats["failed"] += 1
            result["error"] = str(e)

        result["execution_time"] = (datetime.now() - start_time).total_seconds()
        self._print_summary(result)

        return result

    def _make_decision(self, agents: dict) -> dict:
        """Формирует финальное решение."""
        compliance = agents.get("compliance", {})
        analyzer = agents.get("analyzer", {})
        strategy = agents.get("strategy", {})

        return {
            "action": strategy.get("strategy_type", "UNKNOWN"),
            "priority": analyzer.get("priority", "N/A"),
            "risk_level": analyzer.get("risk_level", "N/A"),
            "compliance_status": "OK" if len(compliance.get("violations", [])) == 0 else "VIOLATIONS",
            "next_steps": strategy.get("actions", [])
        }

    def _print_summary(self, result: dict):
        """Выводит итоговую сводку."""
        print("\n" + "=" * 60)
        print("📋 ИТОГОВАЯ СВОДКА")
        print("=" * 60)
        decision = result.get("final_decision", {})
        print(f"✅ Действие: {decision.get('action', 'N/A')}")
        print(f"⚡ Приоритет: {decision.get('priority', 'N/A')}")
        print(f"⏱ Время: {result.get('execution_time', 0):.2f} сек")
        print("=" * 60)

    def get_stats(self):
        return self.stats


# Тестирование
if __name__ == "__main__":
    orch = FullOrchestrator()
    result = orch.process("7712345678", 'ООО "Тест"')
    print("\n📊 Статистика:", orch.get_stats())
