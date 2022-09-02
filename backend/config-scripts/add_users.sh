echo "from authorization.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python ../manage.py shell
echo "from authorization.models import User; User.objects.create_user('test', 'test@example.com', 'test')" | python ../manage.py shell
echo "from authorization.models import User; User.objects.create_user('t', 't@t.com', 't')" | python ../manage.py shell
