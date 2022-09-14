cd ../

echo "from hotels.models import Hotel; Hotel.objects.all().delete()" | python3.10 manage.py shell
rm -r hotels/migrations
python manage.py makemigrations hotels
python manage.py migrate

COMMANDS_FILE=data/hotels/insert_commands.txt
if ! [ -f "$COMMANDS_FILE" ]; then
    python3.10 -m data.hotels.generate_insert_commands
fi
python3.10 manage.py shell < $COMMANDS_FILE