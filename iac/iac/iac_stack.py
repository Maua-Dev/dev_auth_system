import os

from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

from .cognito_stack import CognitoStack


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        github_ref = os.environ.get("GITHUB_REF_NAME")

        self.cognito = CognitoStack(self, f'auth_dev_cognito_stack_{github_ref}')
