FROM python:3.10-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip

# Копируем файлы зависимостей
COPY requirements.txt /app/

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное в контейнер
COPY . /app

# Открываем порт для приложения
EXPOSE 8080

# Запуск приложения
CMD ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "8080", "--reload"]