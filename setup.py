from setuptools import setup

setup(
   name='SecretKeeper',
   version='1.0',
   description='AWS Secrets Manager Client',
   author='Joseph Wibowo',
   author_email='joseph.wibowo@appdynamics.com',
   packages=['secretkeeper'],
   install_requires=['boto3'], #external packages as dependencies
)