import mysql
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='brunoferreirabrum'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `volt_instrumentos`;")

cursor.execute("CREATE DATABASE `volt_instrumentos`;")

cursor.execute("USE `volt_instrumentos`;")

# criando tabelas
TABLES = {}
TABLES['Instrumentos'] = ('''
      CREATE TABLE `instrumentos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `tag` varchar(20) NOT NULL,
      `nome` varchar(50) NOT NULL,
      `temperatura` varchar(5) NOT NULL,
      `umidade` varchar(10) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Bruno Brum", "brum", generate_password_hash("papai").decode('utf-8')),
      ("Isabella Aguiar", "bella", generate_password_hash("mamae").decode('utf-8')),
      ("Helena Brum", "Lena", generate_password_hash("amopapaiemamae").decode('utf-8')),
      ("Francisco Brum", "Cisco", generate_password_hash("amopapaiemamae").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from volt_instrumentos.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo instrumentos
instrumentos_sql = 'INSERT INTO instrumentos (tag, nome, temperatura, umidade) VALUES (%s, %s, %s, %s)'
instrumentos = [
      ('ESTSP01', 'Estacao Meteorologica', '15', '0.1'),
      ('COMPMG01', 'Compressor', '15', '0.1'),
      ('CORPRJ01', 'Corrente Aerea', '15','0.1'),

]
cursor.executemany(instrumentos_sql, instrumentos)

cursor.execute('select * from volt_instrumentos.instrumentos')
print(' -------------  Instrumentos:  -------------')
for instrumento in cursor.fetchall():
    print(instrumento[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()