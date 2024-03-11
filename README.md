# BackEnd for Avida Track

# Creating from scratch
flask db init\
flask db migrate -m "Initial migration"\
flask db upgrade

# To update migration
`edit the model`\
flask db migrate -m "message"\
flask db upgrade

# Packages
`pip install` the following:\
alembic\
Flask\
Flask-Migrate\
Flask-RESTful\
FLASK-SQLAlchemy\
flask-cors\
PyMySQL\
SQLAlchemy\
sqlalchemy_utils\
\
avidatrack\
password