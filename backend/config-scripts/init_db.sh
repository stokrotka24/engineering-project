mongo voyager --eval "db.dropDatabase()"
rm -r ../authorization/migrations
rm -r ../hotels/migrations

python ../manage.py makemigrations authorization
python ../manage.py makemigrations hotels
python ../manage.py migrate