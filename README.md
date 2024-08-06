## Проект Foodgram

### **Описание проекта**:  

Foodgram - Это сеть, где люди могут размещать рецепты. Здесь можно добавить, изменить или удалить рецепты, но для этого нужно зарегистрироваться иначе данные доступны только для просмотра. Изменять данные чужих рецептов нельзя, они доступны только для просмотра. Так же вы можете добавлять любые рецепты в избранное и список. Покупок можно скачать файлом.

Проект доступен по [ссылке](https://foodgram-final.zapto.org/)


### **Технологии**:  

Python, Django, Django Rest Framework, Djoser, React, PostgreSQL, Docker, Nginx, Gunicorn 

### **Как запустить проект на сервере:**

- Клонировать репозиторий (локально):
```
git@github.com:Mystique333/foodgram.git
```

- Последовательно установить на сервер Docker, Docker Compose. Список команд:

```
sudo apt install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo apt-get install docker-compose-plugin
```

- Создать на сервере папку foodgram и перейти в неё:

```
mkdir foodgram
cd foodgram
```

- Копировать в папку foodgram на сервере файлы docker-compose.yml, nginx.conf 
из папки infra локального проекта (при необходимости, укажите в файле docker-compose.yml ссылки на собственные образы):

- Создать в папке foodgram на сервере файл .env:

```
sudo touch .env
```

- Добавьте в файл .env личную информацию о БД (пример):

```
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
POSTGRES_DB=foodgram_db
DB_HOST=db
DB_PORT=5432
```

- Запустить контейнеры Docker (на сервере):

```
sudo docker compose up -d
```

- Создать миграции, создать суперпользователя, собрать статику:

```
sudo docker compose exec backend python manage.py makemigrations
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py collectstatic
sudo docker compose exec backend python manage.py createsuperuser
```

### **Автор**  
*Павлов Роман*
