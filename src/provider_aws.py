import json
import boto3
import botocore.exceptions
import click
from utils import validate_user_count

def validate_access():
  sts = boto3.client('sts')
  try:
      sts.get_caller_identity()
  except botocore.exceptions.ClientError as e:
      raise click.BadParameter(f"Invalid AWS credentials: {e}")
  return True

def list_keys(iam, user):
    """exception checking for boto3.iam.list_access_keys """
    try:
        access_keys = iam.list_access_keys(UserName=user)["AccessKeyMetadata"]
    except iam.exceptions.NoSuchEntityException as e:
        raise click.UsageError(f"Specified user not found: {e}")
    return access_keys

def delete_key(iam, user, access_key_id):
    """exception checking for boto3.iam.delete_access_key """
    try:
        _ = iam.delete_access_key(UserName=user,AccessKeyId=access_key_id)
    except iam.exceptions.NoSuchEntityException as e:
        raise click.UsageError(f"Specified user not found: {e}")

def create_key(iam, user):
    """exception checking for boto3.iam.create_access_key """
    try:
        new_access_key = iam.create_access_key(UserName=user)
    except iam.exceptions.NoSuchEntityException as e:
        raise click.UsageError(f"Specified user not found: {e}")
    return new_access_key

def rotate_credentials(user_path):
    """rotate keys for all iam users in path"""
    iam = boto3.client('iam')

    svc_accounts = iam.list_users(PathPrefix=user_path)
    _ = validate_user_count(len(svc_accounts['Users']))
    new_credentials = {}

    for user in svc_accounts['Users']:
        access_keys = list_keys(iam, user['UserName'])

        # delete the oldest key if there is more than one
        if len(access_keys) > 1:
            # sort by creation date to find oldest key (by convention, automation always use the newest key)
            access_keys.sort(key=lambda x: x["CreateDate"])
            delete_key(iam, user['UserName'], access_keys[0]['AccessKeyId'])

        # generate new key, add details to list of new keys
        new_access_key = create_key(iam, user['UserName'])
        new_credentials[user['UserName']] = {}
        new_credentials[user['UserName']]['AccessKeyId'] = new_access_key['AccessKey']['AccessKeyId']
        new_credentials[user['UserName']]['SecretAccessKey'] = new_access_key['AccessKey']['SecretAccessKey']

    return json.dumps(new_credentials, indent=2)
