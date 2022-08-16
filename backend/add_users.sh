rm -f db.sqlite3
rm -r voyager/migrations
python manage.py makemigrations voyager
python manage.py migrate
python manage.py createsuperuser
#echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell
