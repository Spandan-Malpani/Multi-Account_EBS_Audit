import boto3

def send_email(sender_email, recipient_email, html_body, region="us-east-1"):
    ses = boto3.client("ses", region_name=region)
    ses.send_email(
        Source=sender_email,
        Destination={"ToAddresses": [recipient_email]},
        Message={
            "Subject": {"Data": "Unused EBS Volumes Report"},
            "Body": {"Html": {"Data": html_body}}
        }
    )
