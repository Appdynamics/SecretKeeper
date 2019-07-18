import base64
import boto3
import json
import warnings
from botocore.exceptions import ClientError

class SecretKeeper(object):

    def __init__(self, profile='default', region="us-west-2"):
        self.region = region
        session = boto3.Session(profile_name=profile)
        self.client = session.client(
            service_name='secretsmanager',
            region_name=self.region
        )
        self.secrets = dict()

    def create_secret(self, name:str, desc:str, secret:str, key_id:str):
        """
        Creates AWS Secret in SecretsManager
        :param name: friendly name of Secret
        :param desc: Description of secret
        :param secret: Secret string to be encrypted and stored
        :param key_id: KMS Key ID to use for encryption
        :return: dict response
        ------------------------------
        Example Response:
        {
            'ARN': 'string',
            'Name': 'string',
            'VersionId': 'string'
        }
        """
        r = self.client.create_secret(Name=name,
                                      Description=desc,
                                      SecretString=secret,
                                      KmsKeyId=key_id)
        self.secrets[r['Name']] = r['ARN']
        return r

    def delete_secret(self, secret_id:str, recovery_days:int = 30, force=False):
        """
        Deletes an AWS Secret
        :param secret_id: Friendly Secret Name or Amazon Resource Name (ARN)
        :param recovery_days: Number of days secret can be recovered
        :param force: Force deletion of secret without recovery
        :return: dict Response
        ---------------------------
        Example Response:
        {
            'ARN': 'string',
            'Name': 'string',
            'DeletionDate': datetime(2015, 1, 1)
        }
        """
        recovery_days = 0 if force else recovery_days
        r = self.client.delete_secret(SecretId=secret_id,
                                      RecoveryWindowInDays=recovery_days,
                                      ForceDeleteWithoutRecovery=force)
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
        secret_response = self.client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in secret_response:
            secret = secret_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(secret_response['SecretBinary'])
            return decoded_binary_secret
        # try:
        #     get_secret_value_response = self.client.get_secret_value(SecretId=secret_name)
        #     if 'SecretString' in get_secret_value_response:
        #         secret = json.load(get_secret_value_response['SecretString'])
        #         return secret['staging']
        #     else:
        #         decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        #         return decoded_binary_secret
        # except ClientError as e:
        #     if e.response['Error']['Code'] == 'DecryptionFailureException':
        #         # Secrets Manager can't decrypt the protected secret text using the provided key.
        #         raise e
        #     elif e.response['Error']['Code'] == 'InternalServiceErrorException':
        #         # An error occurred on the server side.
        #         raise e
        #     elif e.response['Error']['Code'] == 'InvalidParameterException':
        #         # You provided an invalid value for a parameter.
        #         raise e
        #     elif e.response['Error']['Code'] == 'InvalidRequestException':
        #         # You provided a parameter value that is not valid for the current state of the resource.
        #         raise e
        #     elif e.response['Error']['Code'] == 'ResourceNotFoundException':
        #         # We can't find the resource that you asked for.
        #         raise e
        #     else:
        #         raise e

    def read_all_secrets(self):
        """
          1. Call list_secrets method on boto client interface
          2. Iterate through each secret and get its value
          3. Assign to the secrets_cache instance variable under secret name as key
        """
        pass