
# Конфигурация системы взыскания

# Режим работы: True = Mock (тесты), False = Real LLM (VPS)
USE_MOCK = True

# Настройки Ollama (для VPS)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

# Настройки Telegram бота (заполните на VPS)
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_ADMIN_ID = ""

# Лимиты 230-ФЗ
MAX_CALLS_PER_WEEK = 2
CALL_START_HOUR = 8
CALL_END_HOUR = 22
