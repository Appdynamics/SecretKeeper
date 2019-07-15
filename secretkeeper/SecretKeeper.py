import base64
import boto3
import json
from botocore.exceptions import ClientError

class SecretKeeper(object):

    def __init__(self, profile='default', region="us-west-2"):
        self.region = region
        session = boto3.Session(profile_name=profile)
        self.client = session.client(
            service_name='secretsmanager',
            region_name=self.region
        )
        self.secrets_cache = dict()

    def read_all_secrets(self):
        """
          1. Call list_secrets method on boto client interface
          2. Iterate through each secret and get its value
          3. Assign to the secrets_cache instance variable under secret name as key
        """
        pass

    def create_secret(self, kwargs):
        # if kwargs.get('KMSKeyId') and kwargs.get('')
        r = self.client.create_secret(**kwargs)
        return r

    def get_secret(self, secret_name):
        """
        Retrieving the Secrets manager from AWS Secret Store
        Args:
            secret_name (str): Name of secret we want to extract value
        Returns:
            Secret data as JSON value as defined for the Secret in AWS Secrets Manager
        """
        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
            print(get_secret_value_response)
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:

                secret = json.load(get_secret_value_response['SecretString'])
                # if settings.DEPLOYMENT_HOST in secret:
                #     return secret[settings.DEPLOYMENT_HOST]
                return secret['staging']
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided key.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                raise e
            else:
                raise e

# args = {
#     'Name': 'test',
#     'Description': 'desc',
#     'SecretString': 'test',
#     'Tags': [
#         {
#             'Key': 'account',
#             'Value': 'CVS'
#         },
#         {
#             'Key': 'controller',
#             'Value': 'name'
#         }
#     ]
# }
# client = AWSSecretsManager(profile='default', region='us-west-2')
# # r = client.create_secret(args)
# # print(r)
#
# client.get_secret(args['Name'])
#
# # figure out KMS integration in create secret
# # talk to sumeet about using client key etc...
