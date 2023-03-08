import boto3
from moto import mock_iam, mock_sts
import pytest 
import click
from provider_aws import validate_access, list_keys, create_key, delete_key, rotate_credentials

@mock_sts
def test_validate_access():
    validate_access()

@mock_iam
def test_create_key():
    iam = boto3.client('iam')
    _ = iam.create_user(
        Path='testuserpath',
        UserName='testuser',
    )

    access_key = create_key(iam, 'testuser')
    assert "AccessKey" in access_key

@mock_iam
def test_create_key_exception():
    iam = boto3.client('iam')
    _ = iam.create_user(
        Path='testuserpath',
        UserName='testuser',
    )

    with pytest.raises(click.UsageError) as _:
        _ = create_key(iam, 'invaliduser')

@mock_iam
def test_list_keys():
    iam = boto3.client('iam')
    _ = iam.create_user(
        Path='testuserpath',
        UserName='testuser',
    )

    _ = create_key(iam, 'testuser')
    access_keys = list_keys(iam, 'testuser')
    assert "AccessKeyId" in access_keys[0]
    assert len(access_keys) == 1
    _ = create_key(iam, 'testuser')
    access_keys = list_keys(iam, 'testuser')
    assert len(access_keys) == 2

@mock_iam
def test_list_keys_exception():
    iam = boto3.client('iam')
    _ = iam.create_user(
        Path='testuserpath',
        UserName='testuser',
    )

    with pytest.raises(click.UsageError) as _:
        _ = list_keys(iam, 'invaliduser')

@mock_iam
def test_delete_key():
    iam = boto3.client('iam')
    _ = iam.create_user(
        Path='testuserpath',
        UserName='testuser',
    )

    access_key = create_key(iam, 'testuser')
    access_keys = list_keys(iam, 'testuser')
    assert len(access_keys) == 1
    delete_key(iam, 'testuser', access_key['AccessKey']['AccessKeyId'])
    access_keys = list_keys(iam, 'testuser')
    assert len(access_keys) == 0

@mock_iam
def test_delete_key_exceptions():
    iam = boto3.client('iam')
    _ = iam.create_user(
        Path='testuserpath',
        UserName='testuser',
    )

    access_key = create_key(iam, 'testuser')
    with pytest.raises(click.UsageError) as _:
        delete_key(iam, 'invaliduser', access_key['AccessKey']['AccessKeyId'])
    with pytest.raises(click.UsageError) as _:
        delete_key(iam, 'testuser', 'invalidaccesskeyid')

@mock_iam
def test_rotate_credentials():
    iam = boto3.client('iam')

    _ = iam.create_user(
        Path='testpath',
        UserName='testuser',
    )

    _ = iam.create_access_key(UserName='testuser')
    _ = iam.create_access_key(UserName='testuser')
    results = rotate_credentials('testpath')
    assert "AccessKeyId" in results

@mock_iam
def test_greater_than_max_svc_accounts():
    iam = boto3.client('iam')

    for i in range(1,21):
      _ = iam.create_user(Path='testuserpath', UserName=f"testuser{i}",)

    with pytest.raises(click.UsageError) as _:
      _ = rotate_credentials('testpath')

