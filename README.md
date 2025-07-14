## 🚀 Yacut — Сервис сокращения ссылок
Добро пожаловать в Yacut — миниатюрный, но мощный 🌟 сервис для сокращения длинных ссылок. Создавай короткие URL и делись ими легко и быстро!
🔗 https://very-very-very-long-url.com → http://yacut.ru/py123

### 🧩 Возможности

- 🔧 Создание коротких ссылок
- ✍ Поддержка собственных идентификаторов
- 🔁 Перенаправление на оригинальный URL
- 🧪 REST API для работы с фронтом/мобилкой
- ⚠️ Удобная обработка ошибок
- 💡 Простой и понятный интерфейс

### 📦 Установка проекта

Убедитесь, что у вас установлен Python 3.9+
🔽 1. Клонируй репозиторий:
```bash
git clone https://github.com/your-username/yacut.git
cd yacut
```
🐍 2. Создай виртуальное окружение и активируй его:
```bash
python -m venv venv
source venv/bin/activate        # для Linux/macOS
venv\Scripts\activate           # для Windows
```
📥 3. Установи зависимости:
```bash
pip install -r requirements.txt
```
⚙️ 4. Инициализируй базу данных:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
🚦 5. Запусти приложение:
```bash
flask run
```
Теперь ты можешь открыть в браузере:
🌐 http://localhost:5000

### 📡 Использование API

▶️ POST /api/id/
Создание новой короткой ссылки
Пример запроса:
```json
{
  "url": "https://www.python.org",
  "custom_id": "py"
}
```
Пример ответа:
```json
{
  "url": "https://www.python.org",
  "short_link": "http://localhost:5000/py"
}
```

📥 GET /api/id/<short_id>/
Получение оригинальной ссылки по short_id
Пример ответа:
```json
{
  "url": "https://www.python.org"
}
```

### ⚠️ Обработка ошибок

| Ошибка | Сообщение                                           |
| ------ | --------------------------------------------------- |
| 400    | Отсутствует тело запроса                            |
| 400    | "url" является обязательным полем!                  |
| 400    | Предложенный вариант короткой ссылки уже существует |
| 400    | Указано недопустимое имя для короткой ссылки        |
| 404    | Указанный id не найден                              |

### 🛠 Технологии

- 🐍 Python 3.9+
- 🧪 Flask + SQLAlchemy
- 💾 SQLite (по умолчанию)
- 💼 Flask-Migrate
- 🌐 REST API

### 📝 Лицензия

Проект распространяется под лицензией MIT

### 👤 Автор
Проект разработан с ❤️ и Flask

Имя: Дмитрий Радюк
Email: mitia.radiuk@yandex.ru
GitHub: github.com/Dzmitry-Radziuk






