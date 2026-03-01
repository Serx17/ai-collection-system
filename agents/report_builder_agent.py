
import sys
sys.path.append('/content')
from datetime import datetime
import json

class ReportBuilderAgent:
    """
    Агент формирования итоговых отчетов.
    Создает красивые отчеты для Telegram, Email, PDF.
    """

    def __init__(self):
        self.name = "📈 Report Builder"

    def build(self, orchestrator_result: dict, format: str = "telegram") -> dict:
        """
        Формирует отчет в указанном формате.

        Args:
            orchestrator_result: Результат от оркестратора
            format: Формат отчета (telegram, email, pdf, json)
        """
        print(f"\n[{self.name}] Формирование отчета: {format}...")

        result = {
            "format": format,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "content": "",
            "attachments": []
        }

        if format == "telegram":
            result["content"] = self._build_telegram_report(orchestrator_result)
        elif format == "email":
            result["content"] = self._build_email_report(orchestrator_result)
        elif format == "pdf":
            result["content"] = self._build_pdf_report(orchestrator_result)
        elif format == "json":
            result["content"] = json.dumps(orchestrator_result, indent=2, ensure_ascii=False)

        print(f"  └─ Отчет сформирован ({len(result['content'])} символов)")

        return result

    def _build_telegram_report(self, data: dict) -> str:
        """
        Формирует отчет для Telegram.
        """
        decision = data.get("final_decision", {})
        agents = data.get("agents", {})

        risk = agents.get("risk_analyzer", {}).get("risk_level", "N/A")
        compliance = agents.get("compliance_checker", {}).get("risk_level", "N/A")

        return f"""
═══════════════════════════════════════
📋 ДОСЬЕ ДОЛЖНИКА
═══════════════════════════════════════

🏢 Компания: {data.get('company_name', 'N/A')}
🔢 ИНН: {data.get('inn', 'N/A')}
⏱ Время обработки: {data.get('execution_time', 0):.2f} сек

───────────────────────────────────────
📊 ОЦЕНКА РИСКОВ
───────────────────────────────────────
🎯 Уровень риска: {risk}
🔐 Комплаенс: {compliance}
⚡ Приоритет: {decision.get('priority', 'N/A')}

───────────────────────────────────────
🎯 РЕШЕНИЕ
───────────────────────────────────────
Действие: {decision.get('action', 'N/A')}

📌 СЛЕДУЮЩИЕ ШАГИ:
"""
        for i, step in enumerate(decision.get('next_steps', [])[:3], 1):
            result += f"   {i}. {step}\n"

        return result + "\n═══════════════════════════════════════"

    def _build_email_report(self, data: dict) -> str:
        return f"""
Тема: Отчет по должнику {data.get('inn', 'N/A')}

Уважаемый коллега!

Сформирован отчет по должнику: {data.get('company_name', 'N/A')}

Решение: {data.get('final_decision', {}).get('action', 'N/A')}

Полный отчет во вложении.

С уважением,
AI-Система Взыскания
"""

    def _build_pdf_report(self, data: dict) -> str:
        return "[PDF ОТЧЕТ] — требует библиотеки reportlab"


# Тестирование
if __name__ == "__main__":
    agent = ReportBuilderAgent()
    test_data = {
        "inn": "7712345678",
        "company_name": "ООО Тест",
        "execution_time": 2.5,
        "final_decision": {"action": "PRETRIAL", "priority": "P1", "next_steps": ["Шаг 1", "Шаг 2"]},
        "agents": {
            "risk_analyzer": {"risk_level": "HIGH"},
            "compliance_checker": {"risk_level": "low"}
        }
    }

    result = agent.build(test_data, "telegram")
    print(result["content"])
