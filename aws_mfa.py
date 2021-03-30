from configparser import ConfigParser
import boto3
import sys

# Check if user entered the code from device
if len(sys.argv) < 2:
    print('Missing code!')
    sys.exit()

# Get AWS credentials and device serial number from config file
try:
    config = ConfigParser()
    config.read('config.ini')
    key = config.get('aws', 'key')
    secret = config.get('aws', 'secret')
    region = config.get('aws', 'region')
    serial = config.get('aws', 'serial')
except BaseException as e:
    print(e)
    sys.exit()


# Get temporary credentials
try:
    mfa_otp = sys.argv[1]
    client = boto3.client('sts', aws_access_key_id=key, aws_secret_access_key=secret, region_name=region)
    mfa_creds = client.get_session_token(
        DurationSeconds=36000,
        SerialNumber=serial,
        TokenCode=mfa_otp
    )
    print(f'AWS_ACCESS_KEY_ID={mfa_creds["Credentials"]["AccessKeyId"]}')
    print(f'AWS_SECRET_ACCESS_KEY={mfa_creds["Credentials"]["SecretAccessKey"]}')
    print(f'AWS_TOKEN={mfa_creds["Credentials"]["SessionToken"]}')
except BaseException as e:
    print(e)