import os

from constructs import Construct

from aws_cdk import (
    aws_cognito, RemovalPolicy,
    aws_lambda as lambda_,
    Duration, CfnOutput
)

class CognitoStack(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        github_ref = os.environ.get("GITHUB_REF")

        self.user_pool = aws_cognito.UserPool(self, f"auth_dev_user_pool_{github_ref}",
                                              removal_policy=RemovalPolicy.DESTROY,
                                              self_sign_up_enabled=True,
                                              auto_verify=aws_cognito.AutoVerifiedAttrs(email=True),
                                              user_verification=aws_cognito.UserVerificationConfig(
                                                  email_subject="Bem Vindo ao Sistema de Autenticação da Dev. Community Mauá",
                                                  email_body="Olá!\nSeja bem vindo ao sistema de autenticação da Dev. Community Mauá. Seu código de cadastro é: {####}",
                                                  email_style=aws_cognito.VerificationEmailStyle.CODE),
                                              standard_attributes=aws_cognito.StandardAttributes(
                                                  email=aws_cognito.StandardAttribute(
                                                      required=True,
                                                      mutable=True
                                                  ),
                                                  fullname=aws_cognito.StandardAttribute(
                                                        required=True,
                                                        mutable=True
                                                  ),
                                              ),
                                              sign_in_aliases=aws_cognito.SignInAliases(
                                                  email=True
                                              ),
                                              )

        self.client = self.user_pool.add_client(f"auth_dev_client_{github_ref}",
                                                auth_flows=aws_cognito.AuthFlow(
                                                    admin_user_password=True,
                                                    custom=True,
                                                    user_password=True,
                                                    user_srp=True
                                                ),
                                                generate_secret=False,
                                                o_auth=aws_cognito.OAuthSettings(
                                                    flows=aws_cognito.OAuthFlows(
                                                        implicit_code_grant=True
                                                    ),
                                                    scopes=[
                                                        aws_cognito.OAuthScope.EMAIL,
                                                        aws_cognito.OAuthScope.OPENID,
                                                        aws_cognito.OAuthScope.PROFILE,
                                                        aws_cognito.OAuthScope.COGNITO_ADMIN
                                                    ],
                                                    callback_urls=[
                                                        "https://devmaua.com"
                                                    ]
                                                ),
                                                )

        self.domain = self.user_pool.add_domain(f"authdevmaua-{github_ref}",
                                                cognito_domain=aws_cognito.CognitoDomainOptions(
                                                    domain_prefix="authdevmaua"
                                                )
                                                )
