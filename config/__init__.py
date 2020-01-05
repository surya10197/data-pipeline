# from config.Config import POSTGRES_CONN_LINK

# from sqlalchemy import create_engine

import boto3

s3 = boto3.client('s3')

# PSQL Object creation
# conn = create_engine(POSTGRES_CONN_LINK, encoding='utf8',
#                      convert_unicode=True, client_encoding='utf8').connect()
