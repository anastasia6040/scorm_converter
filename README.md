# SCORM Converter — создание элементов электронных учебных курсов в формате SCORM на основе документов Microsoft Word

Веб-приложение на Flask, которое преобразует документ Microsoft Word (.docx) в SCORM 1.2-пакет, готовый к загрузке в систему дистанционного обучения (LMS), например Moodle.

---

## Технологический стек

- **Backend:** Python 3.11, Flask, Flask-Login
- **База данных:** SQLite, SQLAlchemy
- **Парсинг документов:** python-docx
- **Шаблонизация:** Jinja2
- **Упаковка:** стандартная библиотека `zipfile`
- **Frontend курса:** HTML/CSS/JavaScript, интеграция SCORM 1.2 API через `SCORM_API_wrapper.js` и `scorm_12_libs.js`


## Развёртывание

### Требования

- Python 3.11 или новее
- pip

### Установка

1. Клонировать репозиторий:

   ```bash
   git clone <ссылка-на-репозиторий>
   cd scorm_converter
   ```

2. Создать и активировать виртуальное окружение:

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux / macOS
   source venv/bin/activate
   ```

3. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Инициализировать базу данных (SQLite):

   База данных SQLite создаётся автоматически при первом запуске приложения (файл `scorm.db` появится в корне проекта), отдельная команда инициализации не требуется.


### Запуск

```bash
python main.py
```

По умолчанию приложение доступно по адресу `http://127.0.0.1:5000`.

## Внешний вид

### Регистрация

!(screenshots/Регистрация.png)

### Авторизация

!(screenshots/Авторизация.png)

### Загрузка документа

!(screenshots/Загрузка документа.png)

### Заполнение метаданных

!(screenshots/Заполнение метаданных.png)

### Прогресс конветрации

!(screenshots/Прогресс.png)

### Предпросмотр курса

!(screenshots/Предпросмотр.png)

### Встроенный редактор курса

!(screenshots/Редактор.png)

### История конвертаций

!(screenshots/История.png)
