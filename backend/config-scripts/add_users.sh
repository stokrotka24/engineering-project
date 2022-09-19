echo "from authorization.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python ../manage.py shell
echo "from authorization.models import User; User.objects.create_user('t', 't@t.com', 't')" | python ../manage.py shell
cd ../
COMMANDS_FILE=data/users/insert_commands.txt
if ! [ -f "$COMMANDS_FILE" ]; then
  python3.10 -m data.users.generate_insert_commands
fi
python3.10 manage.py shell < $COMMANDS_FILE > /dev/null