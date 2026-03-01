
import sys
sys.path.append('/content')
import asyncio
from datetime import datetime

# Aiogram для Telegram
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from orchestrator_v2 import FullOrchestrator

# ============================================
# ⚙️ НАСТРОЙКИ (заполните на VPS)
# ============================================
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Вставить токен от @BotFather
ADMIN_ID = 0  # Вставить ваш Telegram ID

# ============================================
# 🤖 ИНИЦИАЛИЗАЦИЯ
# ============================================
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
orchestrator = FullOrchestrator()

# ============================================
# ⌨️ КЛАВИАТУРА
# ============================================
def get_main_keyboard():
    keyboard = [
        [KeyboardButton(text="🔍 Проверить должника"), KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="📋 Последние отчеты"), KeyboardButton(text="⚙️ Настройки")],
        [KeyboardButton(text="❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# ============================================
# 📬 ОБРАБОТЧИКИ
# ============================================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Команда /start"""
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "🤖 Я — AI-Система Взыскания Долгов\n\n"
        "📋 Мои возможности:\n"
        "• Проверка должников по ИНН\n"
        "• Анализ рисков (ФССП, суды, ЕГРЮЛ)\n"
        "• Проверка 230-ФЗ и 152-ФЗ\n"
        "• Генерация скриптов для операторов\n\n"
        "Нажмите 🔍 Проверить должника для начала работы!",
        reply_markup=get_main_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Команда /help"""
    await message.answer(
        "📖 ПОМОЩЬ\n\n"
        "🔍 Проверка должника:\n"
        "Отправьте ИНН (10 или 12 цифр)\n\n"
        "📊 Статистика:\n"
        "Нажмите кнопку 'Статистика'\n\n"
        "⚙️ Команды:\n"
        "/start - Главное меню\n"
        "/help - Помощь\n"
        "/stats - Статистика системы"
    )

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    """Команда /stats"""
    stats = orchestrator.get_stats()
    await message.answer(
        f"📊 СТАТИСТИКА СИСТЕМЫ\n\n"
        f"Всего запросов: {stats['total']}\n"
        f"Успешно: {stats['success']}\n"
        f"Ошибок: {stats['failed']}\n\n"
        f"Время работы: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

@dp.message(lambda msg: msg.text == "🔍 Проверить должника")
async def check_debtor_menu(message: types.Message):
    """Кнопка проверки должника"""
    await message.answer(
        "🔍 ПРОВЕРКА ДОЛЖНИКА\n\n"
        "Отправьте ИНН организации (10 цифр)\n"
        "или физического лица (12 цифр)\n\n"
        "Пример: 7712345678"
    )

@dp.message(lambda msg: msg.text == "📊 Статистика")
async def stats_menu(message: types.Message):
    """Кнопка статистики"""
    stats = orchestrator.get_stats()
    await message.answer(
        f"📊 СТАТИСТИКА\n\n"
        f"✅ Успешно: {stats['success']}\n"
        f"❌ Ошибок: {stats['failed']}"
    )

@dp.message(lambda msg: msg.text == "❓ Помощь")
async def help_menu(message: types.Message):
    """Кнопка помощи"""
    await message.answer(
        "❓ ПОМОЩЬ\n\n"
        "Система автоматически проверяет должников\n"
        "и формирует рекомендации по взысканию.\n\n"
        "📞 Техподдержка: @your_username"
    )

@dp.message(lambda msg: msg.text and msg.text.isdigit() and len(msg.text) in [10, 12])
async def process_inn(message: types.Message):
    """Обработка ИНН"""
    inn = msg.text
    company_name = f"Должник_{inn}"
    
    # Отправляем статус обработки
    status_msg = await message.answer(
        f"⏳ Обрабатываю ИНН {inn}...\n\n"
        f"🔄 Запуск 7 агентов..."
    )
    
    try:
        # Запускаем оркестратор
        result = orchestrator.process(inn, company_name)
        
        # Формируем отчет
        report = format_report(result)
        
        # Отправляем отчет
        await message.answer(report, parse_mode="HTML")
        
        # Обновляем статус
        await status_msg.edit_text(f"✅ Обработка завершена!")
        
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
        await status_msg.edit_text("❌ Ошибка обработки")

@dp.message()
async def unknown_message(message: types.Message):
    """Неизвестные сообщения"""
    await message.answer(
        "❓ Не понял команду.\n\n"
        "Отправьте ИНН (10-12 цифр)\n"
        "или нажмите кнопку в меню."
    )

# ============================================
# 📄 ФОРМАТИРОВАНИЕ ОТЧЕТА
# ============================================
def format_report(result: dict) -> str:
    """Форматирует отчет для Telegram"""
    decision = result.get("final_decision", {})
    agents = result.get("agents", {})
    
    # Данные из агентов
    collector = agents.get("collector", {})
    compliance = agents.get("compliance", {})
    analyzer = agents.get("analyzer", {})
    strategy = agents.get("strategy", {})
    script = agents.get("script", {})
    
    # Формируем текст
    report = f"""
═══════════════════════════════════════
📋 ДОСЬЕ ДОЛЖНИКА
═══════════════════════════════════════

🏢 <b>Компания:</b> {result.get('company_name', 'N/A')}
🔢 <b>ИНН:</b> {result.get('inn', 'N/A')}
⏱ <b>Время:</b> {result.get('execution_time', 0):.2f} сек

───────────────────────────────────────
📊 ОЦЕНКА РИСКОВ
───────────────────────────────────────
🎯 <b>Уровень риска:</b> {analyzer.get('risk_level', 'N/A')}
📈 <b>Вероятность возврата:</b> {analyzer.get('recovery_probability', 0):.1f}%
⚡ <b>Приоритет:</b> {decision.get('priority', 'N/A')}

───────────────────────────────────────
🔐 КОМПЛАЕНС (230-ФЗ)
───────────────────────────────────────
Статус: {decision.get('compliance_status', 'N/A')}
Нарушения: {len(compliance.get('violations', []))}
"""
    
    # Добавляем нарушения если есть
    for v in compliance.get('violations', [])[:2]:
        report += f"  ❌ {v[:50]}...\n"
    
    report += f"""
───────────────────────────────────────
🎯 РЕШЕНИЕ
───────────────────────────────────────
<b>Действие:</b> {decision.get('action', 'N/A')}

<b>Следующие шаги:</b>
"""
    
    for i, step in enumerate(decision.get('next_steps', [])[:3], 1):
        report += f"  {i}. {step}\n"
    
    # Добавляем скрипт если есть
    if script.get('script'):
        report += f"""
───────────────────────────────────────
📝 СКРИПТ ДЛЯ ОПЕРАТОРА
───────────────────────────────────────
<pre>{script.get('script', '')[:500]}...</pre>
"""
    
    report += "\n═══════════════════════════════════════"
    
    return report

# ============================================
# 🚀 ЗАПУСК
# ============================================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("🤖 Telegram-бот готов к запуску!")
    print(f"Токен: {TELEGRAM_BOT_TOKEN[:10]}...")
