    Revibe - Therapy Music

Setup:

python -m venv venv
venv\Scripts\activate (Windows) or source venv/bin/activate (mac/linux)

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Visit http://127.0.0.1:8000/
