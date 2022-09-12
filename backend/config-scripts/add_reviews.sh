cd ../
COMMANDS_FILE=data/reviews/insert_commands.txt
if ! [ -f "$COMMANDS_FILE" ]; then
    python3.10 -m data.reviews.generate_insert_commands
fi
python3.10 manage.py shell < $COMMANDS_FILE