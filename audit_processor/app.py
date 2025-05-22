import os
import json
from aws_clients import assume_role
from ebs_utils import find_unused_volumes, format_as_html_table
from email_utils import send_email

def lambda_handler(event, context):
    account_ids = os.getenv("ACCOUNT_IDS", "").split(",")
    regions = os.getenv("REGIONS", "").split(",")
    role_name = os.getenv("ROLE_NAME")
    sender_email = os.getenv("SENDER_EMAIL")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    if not (account_ids and regions and role_name and sender_email and recipient_email):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing required parameters"})
        }

    results = []

    for account_id in account_ids:
        try:
            session = assume_role(account_id, role_name)
            for region in regions:
                unused_volumes = find_unused_volumes(session, region)
                results.append({
                    "AccountId": account_id,
                    "Region": region,
                    "Volumes": unused_volumes
                })
        except Exception as e:
            results.append({
                "AccountId": account_id,
                "Region": "N/A",
                "Volumes": [],
                "Error": str(e)
            })

    html_body = format_as_html_table(results)

    send_email(sender_email, recipient_email, html_body)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Email sent successfully"})
    }
