# Add cron job and add escaping spaces in crontab file
python3.10 manage.py crontab add
COMMAND_FILE="cron_command.txt"
crontab -l > $COMMAND_FILE
sed -i -E 's/\/([A-Za-z]+)\ /\/\1\\ /g' $COMMAND_FILE
cat $COMMAND_FILE | crontab -
rm $COMMAND_FILE