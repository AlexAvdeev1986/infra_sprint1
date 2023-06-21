# infra_sprint1

Инструкция для серверов с предустановленным python.
Все комманды делаем без кавычек.



 - заходим на удалённый свервер и обновляем пакеты - 'sudo apt update' 

 - проверяем версию и наличие git - 'git --version', если его нет, то устанавливаем 
   'sudo apt install git'
   
 - клонируем - 'git clone git@github.com:anemiaa1986/infra_sprint1.git'
 
 - переходим в backend в корне проекта и содаём и активируем вирутальной окружение:
   'sudo apt install python3-pip python3-venv -y'
   'python3 -m venv venv'
   'source venv/bin/activate'
   'pip install -r requirements.txt'
   
 - применяем миграции - 'python manage.py migrate'
 
 - создаём суперпользователя - 'python manage.py createsuperuser'
 
 - заходим в settings.py в диреектории infra_sprint1/backend/kittygram_backend
   и меняем/добавляем следующие данные:
   
   DEBUG = False   
   ALLOWED_HOSTS = ['158.160.65.62', '127.0.0.1', 'localhost', 'sprt14kitty.ddns.net']
   STATIC_URL = 'static_backend'
   STATIC_ROOT = BASE_DIR / 'static_backend' 
   MEDIA_ROOT = BASE_DIR / '/var/www/ifra_sprint/media/'
   
 - в папке /var/www/ifra_sprint/ создать папку media
 
 - запускаем фронтенд, устанавливаем на сервер пакетный менеджер npm(одной строкой):
   'curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - &&\'
   ' sudo apt-get install -y nodejs' и проверяем версию 'npm -v'
  
 - из дерриктории infra_sprint1/fronted устанавливаем зависимости 'npm i'
 
 - запускаем unit:
   'pip install gunicorn==20.1.0'
   из папки infra в корневой папке  копируем файл gunicorn_kittygram.service в папку /etc/systemd/
   system/ и запускаем его - 'sudo systemctl start gunicorn_kittygram'
   добавляем в автозагрузку - 'sudo systemctl enable gunicorn_kittygram'
   проверяем статус - 'sudo systemctl status gunicorn_kittygram'
   
 - запускаем Nginx:
   'sudo apt install nginx -y'
   'sudo systemctl start nginx'
   'sudo ufw allow 'Nginx Full''
   'sudo ufw allow OpenSSH'
   'sudo ufw enable'
   проверяем статус 'sudo ufw status'
   
 - подгружаем фронт:
   из папки infra_sprint1/frontend - 'npm run build'
   'sudo cp -r /home/yc-user/infra_sprint1/frontend/build/. /var/www/infra_sprint1/'
   из папки infra_sprint1/infra/ копируем файл default в папку корня /etc/nginx/sites-enabled/
   проверяем на ошибки и загружаем 
   'sudo nginx -t'
   'sudo systemctl reload nginx'
   
 - переходим в backend в корне проекта и загружаем статитку для backend
   'python manage.py collectstatic'
   переходим корень проекта и копируем файлы 'sudo cp -r infra_sprint1/backend/static_backend/ /var/www/infra_sprint1/'
   
 - 'sudo reboot' и после перезагрузки северва всё загрудается автоматические.
 
 - переходи по sprt14kitty.ddns.net;
 

 
 
