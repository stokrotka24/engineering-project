# HTTP:
# python3.10 manage.py runserver 0.0.0.0:5000
# HTTPS:
python3.10 manage.py runserver_plus --cert-file https/server_public_key.pem --key-file https/server_private_key.pem --keep-meta-shutdown 0.0.0.0:5000