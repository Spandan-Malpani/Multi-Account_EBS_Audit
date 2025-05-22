def find_unused_volumes(session, region):
    ec2 = session.client("ec2", region_name=region)
    volumes = ec2.describe_volumes()["Volumes"]
    return [v for v in volumes if not v.get("Attachments")]

def format_as_html_table(results):
    html = "<h3>Unused EBS Volumes Report</h3>"
    html += "<table border='1'><tr><th>Account ID</th><th>Region</th><th>Volume ID</th><th>Size (GiB)</th><th>AZ</th><th>State</th></tr>"
    for item in results:
        for vol in item.get("Volumes", []):
            html += f"<tr><td>{item['AccountId']}</td><td>{item['Region']}</td><td>{vol['VolumeId']}</td><td>{vol['Size']}</td><td>{vol['AvailabilityZone']}</td><td>{vol['State']}</td></tr>"
    html += "</table>"
    return html
