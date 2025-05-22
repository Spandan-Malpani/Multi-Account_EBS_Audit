import boto3

def assume_role(account_id, role_name):
    sts = boto3.client("sts")
    response = sts.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/{role_name}",
        RoleSessionName="CrossAccountEBSCheck"
    )
    creds = response['Credentials']
    return boto3.Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )
