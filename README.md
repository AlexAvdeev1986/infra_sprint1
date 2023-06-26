# Kittygram - социальная сеть на самых минималках для размещение фотографий котиков. Учебный проект Яндекс.Практикум.

## Описание проекта
Проект написан в рамках учебного курса по Python от Яндекс.Практикум.
Пользователи могут регистрироваться, загружать фотографии своих котов с кратким описанием, и смотреть котиков других пользователей. Основная задача  - обучение деплою проекта на сервер.

## Технологии

 - Python 3.9
 - Django==3.2.3
 - djangorestframework==3.12.4
 - Nginx
 - gunicorn
 
## Установка проекта на локальный компьютер из репозитория 
 - Клонировать репозиторий `git clone https://github.com/AlexAvdeev1986/infra_sprint1.git`
 - перейти в директорию с клонированным репозиторием
 - установить виртуальное окружение `python3 -m venv venv`
 - войти `cd infra_sprint1`
 - установить зависимости `pip install -r requirements.txt`
 - в директории `cd /backend/kittygram_backend/` создать файл touch .env
 - в файле `nano .env` прописать ваш SECRET_KEY в виде: SECRET_KEY = 'django-insecure-cg6*%6d51ef8f#4!r3*$vmxm4)abgjw8mo!4y-q*uq1!4$-89$'

# Деплой проекта на удаленный сервер

## Подключение сервера к аккаунту на GitHub
- на сервере должен быть установлен Git. Для проверки выполнить `sudo apt update` `git --version`
- если Git не установлен - установить командой `sudo apt install git`
- находясь на сервере сгенерировать пару SSH-ключей командой `ssh-keygen`
- сохранить открытый ключ в вашем аккаунте на GitHub. Для этого вывести ключ в терминал командой `cat .ssh/id_rsa.pub`. Скопировать ключ от символов ssh-rsa, включительно, и до конца. Добавить это ключ к вашему аккаунту на GitHub.
- `ssh -i /home/ea703557/Загрузки/555/yc-ea703557 yc-user@158.160.28.33`
-
- клонировать проект с GitHub на сервер: `git clone https://github.com/AlexAvdeev1986/infra_sprint1.git`

## Запуск backend проекта на сервере
- 
- Установить пакетный менеджер и утилиту для создания виртуального окружения `sudo apt install python3-pip python3-venv -y`
- `cd ~/infra_sprint1` 
- находясь в директории с проектом создать и активировать виртуальное окружение `python3 -m venv venv`  `source venv/bin/activate` 
- установить зависимости `pip install -r requirements.txt`
- `cd backend/kittygram_backend/`
- `touch .env`
- `nano .env` вставить SECRET_KEY = 'django-insecure-cg6*%6d51ef8f#4!r3*$vmxm4)abgjw8mo!4y-q*uq1!4$-89$'
- `cd ~/infra_sprint1/backend`
- выполнить миграции `python3 manage.py migrate`
- создать суперюзера `python3 manage.py createsuperuser`
- отредактировать settings.py на сервере: в список ALLOWED_HOSTS добавить внешний IP-адрес вашего сервера и адреса `127.0.0.1` и `localhost` . 

ALLOWED_HOSTS = ['158.160.28.33', '127.0.0.1', 'localhost', 'alextaski.ddns.net']

## Запуск frontend проекта на сервере
- установить на сервер `Node.js`   командами
`curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - &&\`
`sudo apt-get install -y nodejs`
- установить зависимости frontend приложения. Из директории `cd ~/infra_sprint1/frontend/` выполнить команду: `sudo apt install npm` `npm i` `npm audit' 'npm audit fix --force`

## Установка и запуск Gunicorn
- при активированном виртуальном окружении проекта установить пакет gunicorn `pip install gunicorn==20.1.0`
- открыть файл settings.py проекта и установить для константы `DEBUG` значение `False` `DEBUG = False`
- В директории _/etc/systemd/system/_ создайте файл _gunicorn.service_ `sudo nano /etc/systemd/system/gunicorn.service`  со следующим кодом (без комментариев):

	    [Unit]
    
	    Description=gunicorn daemon
    
	    After=network.target
    
	    [Service]
    
	    User=yc-user
    
	    WorkingDirectory=/home/yc-user/infra_sprint1/backend/
    
	    ExecStart=/home/yc-user/infra_sprint1/venv/bin/gunicorn --bind 0.0.0.0:8080 kittygram_backend.wsgi
    
	    [Install]
    
	    WantedBy=multi-user.target

Чтобы точно узнать путь до Gunicorn можно при активированном виртуальном окружении использовать команду `which gunicorn`

## Установка и настройка Nginx

 - На сервере из любой директории выполнить команду: `sudo apt install nginx -y`
- Для установки ограничений на открытые порты выполнить по очереди команды: `sudo ufw allow 'Nginx Full'`  `sudo ufw allow OpenSSH`
- включить файервол `sudo ufw enable`
	### собрать и разместить статику frontend-приложения.
- Перейти в директорию `cd ~/infra_sprint1/frontend/` и выполнить команду `npm run build` Результат сохранится в директории ..._/frontend/build/_.  В системную директорию сервера _/var/www/_ скопировать содержимое папки _/frontend/build/_
- открыть файл конфигурации веб-сервера `sudo nano /etc/nginx/sites-enabled/default` и заменить его содержимое следующим кодом:

    	
        server {
    
	        listen 80;
	        server_name 158.160.28.33 alexkittygram.ddns.net;
        
	        location / {
            root   /var/www/kittygram;
            index  index.html index.htm;
            try_files $uri /index.html;
	        }
    
	    }
- проверить корректность конфигурации `sudo nginx -t`
- перезагрузить конфигурацию Nginx `sudo systemctl reload nginx`
	### настроить проксирование запросов
- Открыть файл конфигурации Nginx `sudo nano /etc/nginx/sites-enabled/default` и добавить в него ещё один блок `location`

	    server {
    
	        listen 80;
	        server_name 158.160.28.33 alexkittygram.ddns.net;
    
	        location /api/ {
	            proxy_pass http://127.0.0.1:8080;
	        }
	        
		    location /admin/ {
			    proxy_pass http://127.0.0.1:8000;
				}
			
	        location / {
	            root   /var/www/kittygram;
	            index  index.html index.htm;
	            try_files $uri /index.html;
	        }
    
	    }

- Сохранить изменения, проверить и перезагрузить конфигурацию веб-сервера:

	    sudo nginx -t
	    sudo systemctl reload nginx

	### собрать и настроить статику для backend-приложения.
- в файле `nano settings.py` прописать настройки 
	

	    STATIC_URL = 'static_backend'
	    STATIC_ROOT = BASE_DIR / 'static_backend'


- `cd ~/infra_sprint1/backend/` будет создcdана директория _static_backend/_ 
- активировать виртуальное окружение проекта, перейти в 
директорию с файлом _manage.py_ и выполнить команду `python3 manage.py collectstatic`
- в директории 
- Скопировать директорию _static_backend/_ в директорию _/var/www/<имя_проекта>/_

## Добавление доменного имени в настройки Django
- в файле _settings.py_ добавить в список `ALLOWED_HOSTS` доменное имя: 
	ALLOWED_HOSTS = ['ip_адрес_вашего_сервера', '127.0.0.1', 'localhost', 'ваш-домен'] 
	
- сохранить изменения и перезапустить gunicorn `sudo systemctl restart gunicorn`
- внести изменения в конфигурацию Nginx. Открыть конфигурационный файл командой: `sudo nano /etc/nginx/sites-enabled/default`
- Добавьте в строку `server_name` выданное вам доменное имя (через пробел, без `< >`):

		server {
		...
		     server_name 158.160.28.33 alexkittygram.ddns.net;
		...
		}
- Проверить конфигурацию `sudo nginx -t` и перезагрузить её командой `sudo systemctl reload nginx`, чтобы изменения вступили в силу.

 ## Получение и настройка SSL-сертификата
 **Установка certbot**
 - Зайдите на сервер и последовательно выполните команды:

	    sudo apt install snapd
	    sudo snap install core; 
		sudo snap refresh core
	    sudo snap install --classic certbot
	    `sudo ln -s /snap/bin/certbot /usr/bin/certbot
- запустить certbot и получить SSL-сертификат`:

		sudo certbot --nginx
- сертификат автоматически сохранится на вашем сервере в системной директории _/etc/ssl/_  Также будет автоматически изменена конфигурация Nginx: в файл _/etc/nginx/sites-enabled/default_ добавятся новые настройки и будут прописаны пути к сертификату.
- перезагрузить конфигурацию Nginx `sudo systemctl reload nginx`
