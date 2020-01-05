import os
import json

parent_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(parent_dir, 'dev.env.json')) as env_file:
    env_variables = json.load(env_file)

start = env_variables['start']
end = env_variables['end']
base_url = env_variables['base_url']
# image_path = env_variables['image_path']
# POSTGRES_CONN_LINK = env_variables['POSTGRES_CONN_LINK']
bucket = env_variables['s3_bucket_name']