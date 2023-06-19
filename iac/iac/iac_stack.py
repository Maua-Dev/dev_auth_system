import os

from aws_cdk import (
    Stack,
    aws_lambda as lambda_, Duration,
    aws_cognito
)
from constructs import Construct

from .cognito_stack import CognitoStack


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        github_ref = os.environ.get("GITHUB_REF_NAME")

        self.cognito_stack = CognitoStack(self, f'auth_dev_cognito_stack_{github_ref}')

        custom_message_function = lambda_.Function(
            self, "custom_message_function",
            code=lambda_.Code.from_asset(f"../cognito_triggers/send_email"),
            memory_size=128,
            handler=f"send_email.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(15),
        )

        self.cognito_stack.user_pool.add_trigger(
            aws_cognito.UserPoolOperation.CUSTOM_MESSAGE,
            custom_message_function
        )
