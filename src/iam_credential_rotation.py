import click
from utils import validate_outfile, validate_path, output_results
from provider_aws import rotate_credentials, validate_access

@click.version_option()
@click.command(no_args_is_help=True)
@click.option('-o','--outfile', help="Write results to TEXT file", callback=validate_outfile)
@click.argument('path', callback=validate_path)
def cli(outfile, path):
    """
    For machine account AWS IAM Users on PATH, perform credential rotation using
    CURRENT/LAST two-key pattern. Outputs list of updated users/credentials for
    processing and storage in secure location.
    """
    if validate_access(): output_results(rotate_credentials(path), outfile)
