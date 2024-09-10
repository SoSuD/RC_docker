# Используем базовый образ с Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем все зависимости
RUN pip install -r requirements.txt

# Копируем оставшиеся файлы приложения в контейнер
COPY . .

# Открываем порт 5000 для работы Flask
EXPOSE 5000

# Команда для запуска Flask-приложения
CMD ["python", "server.py"]
