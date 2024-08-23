import boto3

# Lista de parámetros a recuperar
PARAMETER_NAMES = [
    '/myapp/connectionLimit',
    '/myapp/host',
    '/myapp/user',
    '/myapp/password',
    '/myapp/port',
    '/myapp/database',
    '/myapp/debug'
]

def get_parameters():
    # Crear una sesión con AWS
    ssm_client = boto3.client('ssm', region_name='us-east-1')  # Cambia la región según tu necesidad

    # Recuperar los parámetros
    response = ssm_client.get_parameters(
        Names=PARAMETER_NAMES,
        #WithDecryption=True  # Si los parámetros están encriptados, se desencriptan
    )

    # Crear un diccionario con los parámetros recuperados
    parameters = {param['Name']: param['Value'] for param in response['Parameters']}

    return parameters
