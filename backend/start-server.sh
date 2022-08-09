# HTTP:
# python3.10 manage.py runserver 0.0.0.0:5000
# HTTPS:
python3.10 manage.py runserver_plus --cert-file https/server-public-key.pem --key-file https/server-private-key.pem --keep-meta-shutdown 0.0.0.0:5000