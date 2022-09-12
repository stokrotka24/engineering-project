cd ../
COMMANDS_FILE=data/hotels/insert_commands.txt
if ! [ -f "$COMMANDS_FILE" ]; then
    python3.10 -m data.hotels.generate_insert_commands
fi
python3.10 manage.py shell < $COMMANDS_FILE