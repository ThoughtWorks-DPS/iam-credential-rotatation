from click.testing import CliRunner
from iam_credential_rotation import cli

def test_iam_credential_rotation_invalid_filename():
  runner = CliRunner()
  result = runner.invoke(cli, ['-o', 'invalid:filename'])
  assert result.exit_code == 2
  assert "Invalid outfile filename" in result.output

def test_iam_credential_rotation_no_path_provided():
  runner = CliRunner()
  result = runner.invoke(cli)
  assert "Usage:" in result.output

def test_iam_credential_rotation_invalid_path():
  runner = CliRunner()
  result = runner.invoke(cli, ['+'])
  assert "invalid PATH" in result.output

# def test_iam_credential_rotation_version():
#   runner = CliRunner()
#   result = runner.invoke(cli, ['--version'])
#   assert "version" in result.output

def test_iam_credential_rotation_invalid_flag():
  runner = CliRunner()
  result = runner.invoke(cli, ['--invalidflag'])
  assert "No such option:" in result.output
