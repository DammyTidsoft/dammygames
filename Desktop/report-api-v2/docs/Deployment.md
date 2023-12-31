## Deployment Guide

https://medium.com/@_christopher/deploying-my-django-app-to-a-real-server-part-i-de78962e95ac
https://medium.com/@_christopher/deploying-my-django-app-to-a-real-server-part-ii-f0c277c338f4

#### Todo

- Installing necessary packages.
- Initial server setups.
- Preparing our django app for production.
- Setting up gunicorn.
- Setting up nginx.

### Installing necessary packages

> $ sudo apt-get update
>
> $ sudo apt-get install nginx mysql-server python3-pip python3-dev libmysqlclient-dev ufw virtualenv

### Initial server setup

> $ sudo ufw default deny
>
> $ sudo ufw allow 8800
>
> $ sudo ufw allow 22
>
>$ sudo ufw enable

##### Set up my sql

> $ mysql_secure_installation

> $ mysql -u root -p
>
> mysql> CREATE DATABASE report CHARACTER SET 'utf8';
>
> mysql> CREATE USER mkan;
>
>mysql> GRANT ALL ON report.* TO 'mkan'@'localhost' IDENTIFIED BY 'khudam@2019';
>
> mysql> quit

##### Virtual environment

> $ virtualenv venv
>
> $ source venv/bin/activate
>
> (env) $ pip install -r requirements.txt

#### Make migrations

> (env) $ python manage.py makemigrations
>
> (env) $ python manage.py migrate
>
> (env) $ python manage.py collectstatic

#### Gunicorn

> (env) $ gunicorn --bind 0.0.0.0:8800 config.wsgi:application

> (env) $ deactivate

Create service file

> $ sudo nano /etc/systemd/system/gunicorn.service

Write this in the service

``` [Unit]
Description=gunicorn service
After=network.target
   
[Service]
User=chris
Group=www-data
WorkingDirectory=/home/mkan/tajnid/
ExecStart=/home/mkan/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/mkan/tajnid/tajnid.sock config.wsgi:application
   
[Install]
WantedBy=multi-user.target 
```

```
$ sudo systemctl enable gunicorn.service
$ sudo systemctl start gunicorn.service
$ sudo systemctl status gunicorn.service
```

#### Configuring nginx

```$ sudo nano /etc/nginx/sites-available/tahnid```

Paste the following insde

```
server {
       listen 80;    
       server_name 127.0.0.1;
       location = /favicon.ico {access_log off;log_not_found off;} 
       
       location = /static/ {
         root /home/mkan/tajnid/tajnid
       }
       location = /media/ {
         root/home/mkan/tajnid/tajnid;
       }
       
       location = / {
         include proxy_params;
         proxy_pass http://unix:/home/mkan/tajnid/tajnid.sock;
       }
     }
```

```
$ sudo ln -s /etc/nginx/sites-available/awesome /etc/nginx/sites-enabled
```

```
sudo nginx -t
$ sudo ufw delete allow 8800
$ sudo ufw allow 'Nginx Full'
```

