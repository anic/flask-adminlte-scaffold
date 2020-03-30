find ./ -name *.pyc | xargs rm -rf
find ./ -name __pycache__ | xargs rm -rf
nohup python3 ./manage.py runserver 2>&1 &