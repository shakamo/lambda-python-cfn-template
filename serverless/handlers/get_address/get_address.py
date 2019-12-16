import logging
import rds_config
import json
import boto3
from cerberus import Validator

# aurora serverless settings
database_name = rds_config.database_name
db_cluster_arn = rds_config.db_cluster_arn
db_credentials_secrets_store_arn = rds_config.db_credentials_secrets_store_arn

rds_client = boto3.client('rds-data')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

post_code_query = """
SELECT `addresses`.`id`,
    `addresses`.`post_code`,
    `addresses`.`prefecture`,
    `addresses`.`city`,
    `addresses`.`street`
FROM `rec_digi`.`addresses`
WHERE
    `addresses`.`deleted_at` IS NULL
    AND `addresses`.`post_code` = :post_code;
"""


# validation rule
schema = {
    'post_code': {'required': True, 'type': 'string', 'regex': '^[0-9]{7}$'}
}


def lambda_handler(event, context):
    logger.info(event)

    if 'queryStringParameters' not in event:
        return respond(400, "Missing queryStringParameters")

    params = event['queryStringParameters']

    if params is None:
        return respond(400, 'Missing queryStringParameters')

    v = Validator(schema)
    if not v.validate(params):
        return respond(400, v.errors)

    post_code = params.get('post_code')

    sql = ''
    sql_parameters = []

    sql = post_code_query
    sql_parameters = [
        {'name': 'post_code',
            'value': {'stringValue': f'{post_code}'}}
    ]

    try:
        response = execute_statement(sql, sql_parameters)
    except Exception as e:
        return respond(500, e)

    data = mapping(response['columnMetadata'], response['records'])
    res = {'count': len(data), 'results': data}
    return respond(200, None, res)


def execute_statement(sql, sql_parameters=[]):
    response = rds_client.execute_statement(
        secretArn=db_credentials_secrets_store_arn,
        database=database_name,
        resourceArn=db_cluster_arn,
        includeResultMetadata=True,
        sql=sql,
        parameters=sql_parameters
    )
    return response


def mapping(column, records):
    result = []
    for record in records:
        obj = {}
        for i, data in enumerate(record):
            for key, value in data.items():
                obj[column[i]['name']] = value
        result.append(obj)

    return result


def respond(code, err, res=None):
    message = {"message": err}
    return {
        'statusCode': code,
        'body': json.dumps(message) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }
