import re
from pathvalidate import ValidationError, validate_filename
import click

# Total machine-users in an account is expected to be a relatively low number. Because of that
# the tool limits the number of such users that can be changed at once to prevent unexpected damage.
MAX_SVC_ACCOUNTS=20

def validate_outfile(_ctx, _param, value):
    """Validate --outfile option parameter contents"""
    if value is None:
        return None
    try:
        validate_filename(value)
    except ValidationError as e:
        raise click.BadParameter(f"Invalid outfile filename: {e}")
    return value

def validate_path(_ctx, _param, value):
    """Validate PATH argument contents"""
    valid_path = re.compile(r"^[\x00-\x7F]{2,64}$")
    if re.fullmatch(valid_path, value):
        return f"/{value}/"
    raise click.BadParameter('invalid PATH for IAM Users')

def validate_user_count(user_count):
    """Validate user count is greater than 0 and less than MAX_SVC_ACCOUNTS"""
    if user_count == 0:
        raise click.UsageError("No IAM Users found on PATH")
    if user_count > MAX_SVC_ACCOUNTS:
        raise click.BadParameter(f"Error: Found {user_count} IAM Users. This is more than the max allowed of {MAX_SVC_ACCOUNTS}.")
    return user_count

def output_results(new_credentials, outfile):
    """write results to stdout or outfile"""
    if outfile:
        with open(outfile, "w", encoding="utf8") as file:
            file.write(new_credentials)
    else:
        click.echo(new_credentials)