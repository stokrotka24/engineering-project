# Add cron job and add escaping spaces in crontab file
python3.10 manage.py crontab add
COMMAND_FILE="cron_command.txt"
crontab -l > $COMMAND_FILE
sed -i -E 's/\/([A-Za-z]+)\ /\/\1\\ /g' $COMMAND_FILE
cat $COMMAND_FILE | crontab -
rm $COMMAND_FILE

# HTTP:
# python3.10 manage.py runserver 0.0.0.0:5000
# HTTPS:
python3.10 manage.py runserver_plus --cert-file https/server_public_key.pem --key-file https/server_private_key.pem --keep-meta-shutdown 0.0.0.0:5000
python3.10 manage.py crontab remove