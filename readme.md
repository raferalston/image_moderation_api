## deep-ai стал платным, поэтому переделано на sightengine

## NSFW Image Moderation API (FastAPI + Sightengine)

Это минималистичное FastAPI-приложение для проверки изображений на наличие NSFW-контента (обнажённость, оружие, наркотики, насилие и другие категории) с использованием API сервиса [Sightengine](https://sightengine.com/).

** Данные api можно узнать в [Sightengine api-credentials](https://dashboard.sightengine.com/api-credentials) **

### Установка и запуск:

```bash
# 1. Клонируйте репозиторий:
git clone <URL вашего репозитория>
cd <папка с проектом>/app

# 2. Установите зависимости:
python -m venv env
source env/bin/activate  # Для Windows: env\Scripts\activate
pip install -r requirements.txt

# 3. Создайте файл app/.env с данными доступа *Подробнее о структуре ниже:
API_USER=your_api_user_here
API_KEY=your_api_key_here

# 4. Запуск приложения *из корня app/:
uvicorn main:app --reload

# 5. Добавить изображения в качестве файлов в app/
Например app/example.jpg

# 6. Проверить api
curl -X POST -F "file=@example.jpg" http://localhost:8000/moderate

```

---

### API Документация:

После запуска откройте:

```
http://localhost:8000/docs
```

Вы увидите интерактивную документацию Swagger.


### Запуск тестов:

```bash
pytest
```

Тесты покрывают:

* успешную проверку безопасного изображения;
* выявление NSFW-контента;
* ошибку при отсутствии файла.

---

### Настройки:

Все параметры настроек (например, список моделей или порог NSFW) настраиваются в `.env`:

```env
API_KEY=API secret
API_USER=API user
NSFW_THRESHHOLD=0.5
MODELS=...Строка с моделями
AI_URL=эндпоинт
```

---

### Основные возможности:

* Принимает изображение через POST-запрос (`multipart/form-data`).
* Отправляет изображение на модерацию в Sightengine API.
* Автоматически определяет, нарушает ли изображение правила безопасности (NSFW, violence, drugs и пр.).
* Возвращает:

  * `{"status": "OK"}` — если контент безопасен.
  * `{"status": "REJECTED", "reason": "NSFW content"}` — если контент нарушает правила.

---

### Структура проекта:

```
app/
└──
   ├── core/              # Конфигурация приложения
   │   └── config.py
   ├── routers/           # Маршруты FastAPI
   │   └── moderate.py
   ├── schemas/           # Pydantic-схемы
   │   └── moderate.py
   ├── services/          # Бизнес-логика (модерация изображений)
   │   └── moderate.py
   ├── tests/             # Тесты
   │   └── test_moderate.py
   ├── main.py            # Точка входа FastAPI
   ├── .env               # Конфигурация API-ключей (не коммитится)
   └── requirements.txt   # Зависимости
└── readme.md          # Документация
```

---

### Требования:

* Python 3.10+
* Sightengine API (нужен аккаунт на [https://sightengine.com](https://sightengine.com))


