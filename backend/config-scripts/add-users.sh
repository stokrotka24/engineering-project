rm -f ../db.sqlite3
rm -r ../voyager/migrations
python ../manage.py makemigrations voyager
python ../manage.py migrate
echo "from voyager.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python ../manage.py shell
echo "from voyager.models import User; User.objects.create_user('test', 'test@example.com', 'test')" | python ../manage.py shell
