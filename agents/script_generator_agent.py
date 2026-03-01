
import sys
sys.path.append('/content')
from datetime import datetime

class ScriptGeneratorAgent:
    """
    Агент генерации скриптов разговоров и документов.
    Создает персонализированные тексты для операторов.
    """

    def __init__(self):
        self.name = "📝 Script Generator"

    def generate(self, debtor_data: dict, strategy: dict, scenario: str = "call") -> dict:
        """
        Генерирует скрипт для указанного сценария.

        Args:
            debtor_data: Данные должника
            strategy: Стратегия от Strategy Advisor
            scenario: Тип сценария (call, sms, email, letter)
        """
        print(f"\n[{self.name}] Генерация скрипта: {scenario}...")

        result = {
            "debtor_inn": debtor_data.get("inn", "unknown"),
            "scenario": scenario,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "script": "",
            "tips": [],
            "warnings": []
        }

        company = debtor_data.get("sources", {}).get("egrul", {}).get("company_name", "Должник")
        debt = debtor_data.get("sources", {}).get("fssp", {}).get("total_debt", 0)

        if scenario == "call":
            result["script"] = self._generate_call_script(company, debt, strategy)
            result["tips"] = [
                "Говорите спокойно и уверенно",
                "Не перебивайте должника",
                "Фиксируйте все обещания",
                "Соблюдайте 230-ФЗ"
            ]
            result["warnings"] = [
                "Не использовать угрозы",
                "Не звонить в запрещенное время",
                "Не превышать лимиты контактов"
            ]

        elif scenario == "sms":
            result["script"] = self._generate_sms_script(company, debt)
            result["tips"] = ["Максимум 160 символов", "Указать реквизиты"]
            result["warnings"] = ["Не более 2 SMS в неделю"]

        elif scenario == "email":
            result["script"] = self._generate_email_script(company, debt)
            result["tips"] = ["Прикрепить график платежей", "Указать контакты"]
            result["warnings"] = ["Проверить адрес перед отправкой"]

        elif scenario == "letter":
            result["script"] = self._generate_letter_script(company, debt)
            result["tips"] = ["Отправлять заказным письмом", "Сохранить квитанцию"]
            result["warnings"] = ["Соблюдать сроки уведомления"]

        print(f"  └─ Скрипт сгенерирован ({len(result['script'])} символов)")

        return result

    def _generate_call_script(self, company: str, debt: int, strategy: dict) -> str:
        """
        Генерирует скрипт телефонного разговора.
        """
        return f"""
═══════════════════════════════════════════════
📞 СКРИПТ ЗВОНКА ДОЛЖНИКУ
═══════════════════════════════════════════════

ОПЕРАТОР: Добрый день! Это {company}?

ДОЛЖНИК: Да.

ОПЕРАТОР: Меня зовут [Имя], я представляю [Название компании].
Звоню по вопросу задолженности в размере {debt:,} рублей.

───────────────────────────────────────────────
📋 ОСНОВНАЯ ЧАСТЬ:

1. Подтверждение долга:
   "Подскажите, вы осведомлены о наличии задолженности?"

2. Выяснение причин:
   "Что послужило причиной просрочки платежа?"

3. Предложение решения:
   "Мы можем предложить вам [вариант из стратегии]."

───────────────────────────────────────────────
✅ ЗАВЕРШЕНИЕ:

"Благодарю за разговор. Ожидаем оплату до [дата].
Хорошего дня!"

═══════════════════════════════════════════════
"""

    def _generate_sms_script(self, company: str, debt: int) -> str:
        return f"""
{company}: Напоминание о задолженности {debt:,} руб.
Оплатите до [дата] по реквизитам: [ссылка].
Тел.: 8-800-XXX-XX-XX
"""

    def _generate_email_script(self, company: str, debt: int) -> str:
        return f"""
Тема: Уведомление о задолженности — {company}

Уважаемый партнер!

Напоминаем о наличии задолженности в размере {debt:,} рублей.

Просим произвести оплату в ближайшее время.

С уважением,
[Название компании]
"""

    def _generate_letter_script(self, company: str, debt: int) -> str:
        return f"""
ДОСУДЕБНАЯ ПРЕТЕНЗИЯ

{company}
Адрес: [адрес]

ТРЕБУЕМ погасить задолженность в размере {debt:,} рублей
в течение 10 дней с момента получения.

В противном случае дело будет передано в суд.

[Дата] [Подпись]
"""


# Тестирование
if __name__ == "__main__":
    agent = ScriptGeneratorAgent()
    test_data = {"inn": "7712345678", "sources": {"egrul": {"company_name": "ООО Тест"}, "fssp": {"total_debt": 500000}}}
    test_strategy = {"strategy_type": "NEGOTIATION"}

    result = agent.generate(test_data, test_strategy, "call")
    print(result["script"])
