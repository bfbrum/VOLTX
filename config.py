import os

SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'brunoferreirabrum',
        servidor = 'localhost',
        database = 'volt_instrumentos'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'