import pymysql
import json
from credentials import get_parameters

def RDSupdate(event, context):
    # Recuperar las credenciales y configuraciones de SSM Parameter Store
    params = get_parameters()

    connection_config = {
        'host': params.get('/myapp/host'),
        'user': params.get('/myapp/user'),
        'password': params.get('/myapp/password'),
        'port': int(params.get('/myapp/port')),
        'database': params.get('/myapp/database')
    }

    # Extraer el ID del parámetro de la ruta y el cuerpo de la solicitud PUT
    try:
        usuario_id = event['pathParameters']['id']
        body = json.loads(event['body'])
        sql_update = {
            'USUARIO': body.get('usuario'),
            'NOMBRE': body.get('nombre')
        }

        # Crear una conexión a la base de datos
        connection = pymysql.connect(**connection_config)
        with connection.cursor() as cursor:
            # Crear la consulta de actualización
            sql = "UPDATE usuarios SET USUARIO = %s, NOMBRE = %s WHERE ID = %s;"
            # Ejecutar la consulta de actualización
            cursor.execute(sql, (sql_update['USUARIO'], sql_update['NOMBRE'], usuario_id))
            connection.commit()
            result = cursor.rowcount
        
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
                'message': '¡Éxito al actualizar!',
                'data': {'rowsAffected': result}
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
