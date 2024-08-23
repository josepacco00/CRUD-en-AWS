import pymysql
import json
from credentials import get_parameters

def RDSTestconnection(event, context):
    # Recuperar las credenciales y configuraciones de SSM Parameter Store
    params = get_parameters()
    
    connection_config = {
        'host': params.get('/myapp/host'),
        'user': params.get('/myapp/user'),
        'password': params.get('/myapp/password'),
        'port': int(params.get('/myapp/port')),
        'database': params.get('/myapp/database')
    }
    
    # Crear una conexión a la base de datos
    try:
        connection = pymysql.connect(**connection_config)
        with connection.cursor() as cursor:
            # Ejecutar una consulta simple
            cursor.execute("SELECT 1+1")
            result = cursor.fetchone()
        
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
                'message': '¡Éxito!',
                'data': result
            })
        }
    
    except pymysql.MySQLError as e:
        # Manejar errores de conexión
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
