#!/usr/bin/env python3
import os

import aws_cdk as cdk

from iac.iac_stack import IacStack


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")

if 'prod' in stack_name:
    stage = 'PROD'

elif 'homolog' in stack_name:
    stage = 'HOMOLOG'

elif 'dev' in stack_name:
    stage = 'DEV'

else:
    stage = 'TEST'

tags = {
    'project': 'AuthDev',
    'stage': stage,
    'stack': 'BACK'
}

IacStack(app, stack_name, env=cdk.Environment(account=aws_account_id, region=aws_region), tags=tags)
app.synth()
