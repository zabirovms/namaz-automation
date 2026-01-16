import os
import boto3

account_id = os.environ["R2_ACCOUNT_ID"]
access_key = os.environ["R2_ACCESS_KEY_ID"]
secret_key = os.environ["R2_SECRET_ACCESS_KEY"]
bucket_name = os.environ["R2_BUCKET_NAME"]

session = boto3.session.Session()
s3 = session.client(
    's3',
    region_name='auto',
    endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

output_dir = "output"
for file_name in os.listdir(output_dir):
    if file_name.endswith(".json"):
        file_path = os.path.join(output_dir, file_name)
        s3.upload_file(file_path, bucket_name, file_name)
        print(f"✅ Uploaded {file_name} to R2")
