# Webstore SPA using Vue and DRF

This is a real world webstore (pharmacy) example, including both the frontend and backend. In addition, everything can be packed in a Docker container using Dockerfile in the root of project.

The design of this webstore is based on a free **Bootstrap** template from  [Colorlib](https://colorlib.com). The [Vue.js 2](https://vuejs.org/) was chosen for building the frontend. To implement the realtionship between **Vue.js** and **Bootstrap** used [Bootstrap Vue](https://bootstrap-vue.org). The [Django REST Framework](https://www.django-rest-framework.org/) is used for backend and website administration. Authorization is implemented using JSON Web Tokens for which used [jango-rest-framework-simplejwt](https://github.com/SimpleJWT/django-rest-framework-simplejwt). The [Axios](https://github.com/axios/axios) is used for interaction between the frontend and the backend. All of this can be packaged in [Docker](https://www.docker.com/) container with [Nginx](https://nginx.org/) webserver that communicates with the backend via [uWSGI](https://github.com/unbit/uwsgi). For asyncronus tasks used [Celery](https://docs.celeryproject.org/en/stable/) and [Redis](https://redis.io/) as message broker.

This example is not preapred for porduction and it does not cover security issues, the CORS mechanism is disabled on backend to allow work with backend and frontend on one computer (in one container). 

To use this example you need to install any CORS disable plugin to your browser. I use [Allow CORS](https://mybrowseraddon.com/). In other case you can get **XMLHttpRequest error** in your browser.

If you would like to try sending email after placing your order you should specify SMTP server parameters at the end of file `drugstore/drugstore/setting.py`:
```sh
# E-mail settings
EMAIL_HOST = 'smpt.some_mail_host.com' 
EMAIL_HOST_USER = 'any_user@name.com' 
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

To run this application as Docker container you should run:

```sh
$ docker-compose up --build -d
```

Then in browser you can show the application on ```localhost:8080``` admin panel available on ```localhost:8080/admin/```. Default admin:
```
login: admin
password: admin123
```