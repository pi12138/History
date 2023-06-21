mysql -u root -p -e "create database if not exists blogv2 default character set = 'utf8';" &&

python manage.py makemigrations &&
python manage.py migrate