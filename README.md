<h2 align="center">FatCode()</h2>



## Мы в сети
- [Telegram](https://t.me/django_school)
- [YouTube](https://www.youtube.com/channel/UC_hPYclmFCIENpMUHpPY8FQ)
- [VK](https://vk.com/djangochannel)

### Функционал
- Курсы
- База знаний
- Вопрос \ Ответ

## Старт

#### В корне проекта создать .env.dev и прописать свои настройки

    DEBUG=1
    DJANGO_SECRET_KEY=djB*gi87bgh-ug*T^&*GUIaiy=g0y6l=j+7(#m&@mvJguBY4#@$^&^*
    DJANGO_ALLOWED_HOSTS=*
    CORS_ALLOWED_HOSTS=http://127.0.0.1:8000 http://localhost:3000
    
    # Data Base
    POSTGRES_DB=имя_твоей_бд
    POSTGRES_USER=имя_твоего_пользователя
    POSTGRES_PASSWORD=пароль_бд
    DB_ENGINE=django.db.backends.postgresql
    DB_HOST=db
    DB_PORT=5432

#### Запустить сервер

    docker-compose build
    docker-compose up

    or

    docker-compose up --build

#### Запустить тесты

    docker-compose run web sh -c "python manage.py test"

#### Войти в контейнер

    docker exec -it fatcode bash

### Создать пользователя

    docker-compose run web python manage.py createsuperuser
