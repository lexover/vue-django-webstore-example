#Stage 1: Compile an frontend on node machine
FROM node:lts-alpine as build-stage
ENV NPM_CONFIG_LOGLEVEL info

WORKDIR /app

COPY ./vue-app/package*.json ./

RUN npm install

COPY ./vue-app .

RUN npm run build

#Stage 2: Copy frontend and run django api
FROM tiangolo/uwsgi-nginx:python3.8 as production-stage

ENV LISTEN_PORT 8080

EXPOSE 8080

COPY ./app /app

COPY ./app/custom.conf /etc/nginx/conf.d/custom.conf

COPY ./drugstore /app/drugstore

RUN pip install -r /app/drugstore/requirements.txt

WORKDIR /app/drugstore

RUN python manage.py makemigrations \ 
	&& python manage.py migrate \
	&& python manage.py collectstatic \
	&& python manage.py create_demo_base --path demo_db.json \
	&& echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@drugstore.com', 'admin123')" | python manage.py shell

COPY --from=build-stage /app/dist /app/html

RUN chown -R nginx:nginx /app/html/*

