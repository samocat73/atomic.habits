# Трекер привычек
## API сервис управления привычками на Django/DRF. Интегрирован с Telegram.
## Полное описание всех реализованных эндпоинтов доступно в [документации по проекту](http://127.0.0.1:8000/redoc/).
## О моделях:
### Реализована модель Habit для хранения информации о привычках. Эта модель связана с моделью User через поле user. Так же эта модель ссылается на саму себя в поле related_habit. Это нужно для разделения типов привычек по тех. заданию.
## О интеграции:
### Для интеграции с Telegram использовалось официальное API. Реализован запрос по эндпоинту:
```commandline
requests.get(
        f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage", params=params
    )
```
## О периодических и фоновых задачах:
### Celery используется в фоновой задаче по отправке сообщения в telegram.
### Celery Beat используется для периодической задачи для отслеживания времени напоминания.
## О деплое:
### Приложение и его зависимости запущены в контейнерах с помощью Docker. Оркестрация выполнена через Docker Compose.
## Технологии
**Django, djangorestframework, celery, redis, django-celery-beat, requests, django-cors-headers, drf-yasg, djangorestframework_simplejwt==5.5.1, docker, docker-compose**
## Инструкции по запуску
### Клонирование репозитория:
```commandline
https://github.com/samocat73/atomic.habits.git
```
### Настройка виртуального окружения:
```commandline
python -m venv venv
venv\Scripts\Activate
```
### Установка зависимостей проекта
```commandline
pip install -r requirements.txt
```
### Настройка переменных окружения
**Копируйте файл .env.example и заполните переменные окружения. Переименуйте файл в .env**
### Применение миграций
```commandline
python manage.py migrate
```
### Запуск проекта
```commandline
python manage.py runserver
```