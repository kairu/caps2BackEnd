from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
    
# gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app