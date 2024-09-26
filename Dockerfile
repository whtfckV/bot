FROM python:3.12-slim

WORKDIR /app

# Устанавливаем Poetry и зависимости
RUN pip install --no-cache poetry

# Копируем файлы проекта
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копируем весь проект в контейнер
COPY . .

# Запуск бота
CMD ["python", "bot.py"]