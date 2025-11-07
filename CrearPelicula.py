import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Evento recibido correctamente",
                "event": event
            }
        }))

        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada correctamente",
                "pelicula": pelicula,
                "response": response
            }
        }))

        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error al crear la película",
                "error": str(e)
            }
        }))

        return {
            'statusCode': 500,
            'error': str(e)
        }
