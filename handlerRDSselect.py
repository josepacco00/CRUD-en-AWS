import pymysql
import json
from credentials import get_parameters

def RDSselect(event, context):
    # Recuperar las credenciales y configuraciones de SSM Parameter Store
    params = get_parameters()

    connection_config = {
        'host': params.get('/myapp/host'),
        'user': params.get('/myapp/user'),
        'password': params.get('/myapp/password'),
        'port': int(params.get('/myapp/port')),
        'database': params.get('/myapp/database')
    }

    # Extraer el ID del parámetro de la ruta
    try:
        usuario_id = int(event['pathParameters']['id'])

        # Crear una conexión a la base de datos
        connection = pymysql.connect(**connection_config)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Crear la consulta SELECT
            sql = "SELECT ID, USUARIO, NOMBRE FROM usuarios WHERE ID = %s;"
            # Ejecutar la consulta SELECT
            cursor.execute(sql, (usuario_id,))
            result = cursor.fetchone()
        
        # Cerrar la conexión
        connection.close()

        # Devolver la respuesta
        if result:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': True,
                    'message': '¡Éxito al consultar!',
                    'data': result
                })
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': False,
                    'message': 'No se encontró el registro.'
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
    except ValueError as e:
        # Manejar errores en la conversión del ID
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'message': 'Error en el ID proporcionado: ' + str(e)
            })
        }
