mongo voyager --eval "db.dropDatabase()"
rm -r ../authorization/migrations
python ../manage.py makemigrations authorization
python ../manage.py migrate
echo "from authorization.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python ../manage.py shell
echo "from authorization.models import User; User.objects.create_user('test', 'test@example.com', 'test')" | python ../manage.py shell
