
while ! nc -z pgdb 5432; do sleep 1; done;

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py create_demo_base --path demo_db.json
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@drugstore.com', 'admin123')" | python manage.py shell
