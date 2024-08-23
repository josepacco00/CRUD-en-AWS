import pymysql
import json
from credentials import get_parameters

def RDScreate(event, context):
    # Recuperar las credenciales y configuraciones de SSM Parameter Store
    params = get_parameters()

    connection_config = {
        'host': params.get('/myapp/host'),
        'user': params.get('/myapp/user'),
        'password': params.get('/myapp/password'),
        'port': int(params.get('/myapp/port')),
        'database': params.get('/myapp/database')
    }

    # Extraer el cuerpo de la solicitud POST
    try:
        body = json.loads(event['body'])
        sql_create = {
            'USUARIO': body.get('usuario'),
            'NOMBRE': body.get('nombre')
        }

        sql = "INSERT INTO usuarios (USUARIO, NOMBRE) VALUES (%s, %s);"

        # Crear una conexión a la base de datos
        connection = pymysql.connect(**connection_config)
        with connection.cursor() as cursor:
            # Ejecutar la consulta de inserción
            cursor.execute(sql, (sql_create['USUARIO'], sql_create['NOMBRE']))
            connection.commit()
            result = cursor.fetchall()
        
        # Cerrar la conexión
        connection.close()

        # Devolver la respuesta
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': True,
                'message': '¡Éxito al insertar!',
                'data': result
            })
        }

    except pymysql.MySQLError as e:
        # Manejar errores de conexión o SQL
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'message': str(e)
            })
        }
    except json.JSONDecodeError as e:
        # Manejar errores en el formato del cuerpo de la solicitud
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'message': 'Error en el formato del cuerpo de la solicitud: ' + str(e)
            })
        }
