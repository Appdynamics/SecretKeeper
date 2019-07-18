# Overview
Python client for AWS Secrets Manager. Use this to manage your AWS secrets as well as implement them in your code without hardcoding anything!
# Installation
<pre>pip install git+https://github.com/Appdynamics/SecretKeeper.git</pre>
Please note your Github account must have access to the AppDynamics Github repo in order to install.
# Quickstart
<pre>
from secretkeeper import SecretKeeper
sk = SecretKeeper.SecretKeeper()
sk.get_secret('your_secret')
</pre>