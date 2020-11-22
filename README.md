# Simple Webstore Example App

This is a real world webstore (pharmacy) example, including both the frontend and backend. In addition, everything can be packed in a Docker container using Dockerfile in the root of project.

The design of this webstore is based on a free **Bootstrap** template from  [Colorlib](https://colorlib.com). [Vue.js 2](https://vuejs.org/) was chosen for building the frontend. To implement the realtionship between **Vue.js** and **Bootstrap** used [Bootstrap Vue](https://bootstrap-vue.org). [Django REST Framework](https://www.django-rest-framework.org/) used for backend and website administration. Authorization is implemented using JSON Web Tokens for which used [jango-rest-framework-simplejwt](https://github.com/SimpleJWT/django-rest-framework-simplejwt). An [Axios](https://github.com/axios/axios) is used for interaction between the frontend and the backend. All of this can be packaged in [Docker](https://www.docker.com/) container with [Nginx](https://nginx.org/) webserver that communicates with the backend via [uWSGI](https://github.com/unbit/uwsgi).

This example is not preapred for porduction ant it does not cover security issues, the CORS mechanism is disabled on backend to allow work with backend and frontend on one computer (in one container). 

To use this example you need to install any CORS disable plugin to your browser. I use [Allow CORS](https://mybrowseraddon.com/). In other case you can get **XMLHttpRequest error** in your browser.

To run this application as Docker container you should run:

```bash
$ docker build -t webstore-example .
```

It build the container with name ```webstore-example``` which can be run then:
```bash
$ docker run -it --rm -p 8080:8080 webstore-example
```

Then in browser you can show the application on ```localhost:8080``` admin panel available on ```localhost:8080/admin/```. Default admin:
```
login: admin
password: admin123
```
You can also run frontend and backend separately. For this you should initialyse and run backend (on Linux system):
```bash
$ cd drugstore
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py create_demo_base --path demo_db.json
$ python manage.py createsuperuser
$ python manage.py runserver
```
To start the frontend, you first need to change the address at which it accesses the backend. 
In vue-app/src/common/config.js chenge the line:
```
export const API_URL = 'http://localhost:8080/api';
```
to
```
export const API_URL = 'http://localhost:8000';
```

And then run (Node.js should be installed):
```bash
$ cd vue-app
$ npm install
$ npm run serve
```



