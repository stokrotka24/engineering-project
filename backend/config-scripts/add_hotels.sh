cd ../data/hotels
python3.10 generate_insert_commands.py
python3.10 ../../manage.py shell < insert_commands.txt