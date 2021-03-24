import json
import boto3

def lambda_handler(event, context):
    
    # Parse event variables
    ar = event.get('accessrole')
    fr = event.get('firecallrole')
    duration = event.get('duration')
    
    # Set out Clients
    iam = boto3.client('iam')
    events = boto3.client('events')

    # Read the IAM Access Role Trust Policy
    response = iam.get_role(RoleName=ar)

    policy = response['Role']['AssumeRolePolicyDocument'] 
    dump_policy = json.dumps(policy)

    # Modify the Firecall trust policy
    response2 = iam.update_assume_role_policy(
    RoleName=fr,
    PolicyDocument=dump_policy
    ) 

    # Create our timed cloudwatch event
    if response2.status_code == 200:
        event = events.put_rule(
            Name='RemoveFirecall',
            ScheduleExpression="rate(" + duration + "hour)"
        )
    else: 
        print(response2.status_code)

# Todo 
# SNS Message to notify user that was successful or failed. 