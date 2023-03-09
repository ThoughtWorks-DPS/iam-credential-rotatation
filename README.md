<div align="center">
	<p>
		<img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=200 />
    <br />
		<img alt="DPS Title" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/EMPCPlatformStarterKitsImage.png?sanitize=true" width=350/>
	</p>
  <br />
  <h3>iam-credential-rotation</h3>
    <a href="https://app.circleci.com/pipelines/github/ThoughtWorks-DPS/iam-credential-rotation"><img src="https://dl.circleci.com/status-badge/img/gh/ThoughtWorks-DPS/iam-credential-rotatation/tree/main.svg?style=shield"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
</div>
<br />

Command line tool for automated rotation of AWS IAM machine-user credentials, following a CURRENT/LAST two-key pattern.  

Rotating credentials usually means deleting the existing credentials and then generating new ones. But what happens if you delete an existing set of credentials while there is a current automated job or pipeline running?

When the machine account has two sets of credentials, with the most recent set being the credentials available in the secrets store (which is where automated jobs fetch credentials when they start). You can confidently delete the older of the two credentials, generate new credentials, and update the secrets store with the new, with no fear of causing any system failure. Both the new credentials and the prior credentials used by any jobs still in flight will remain valid until the next rotation. By setting a rotation window at 1/2 (or less) the desired time period then both keys are replaced within the period. Additional [discussion](discussion.md).  

## Install

```bash
pip install iam-credential-rotation
```

## Usage
```
Usage: iam-credential-rotation [OPTIONS] PATH

  For machine account AWS IAM Users on PATH, perform credential rotation using
  CURRENT/LAST two-key pattern. Outputs list of updated users/credentials for
  processing and storage in secure location.

Options:
  -o, --outfile TEXT  Write results to TEXT file
  --version           Show the version and exit.
  --help              Show this message and exit.
```

For example:  

If machine users are stored on the path `users/PSKServiceAccounts/` then the following will rotate each of the IAM Users on that path. _Note that the actual output does not obfuscate the credential information. In normal use, a pipeline or other automated job that performs this rotation would parse the output and write the new credentials into a Secrets store._  

```
$ iam-credential-rotation PSKServiceAccounts
{
  "PSKNonprodServiceAccount": {
    "AccessKeyId": "AKIARKL**************",
    "SecretAccessKey": "bCFqIBZUo****************************"
  },
  "PSKProdServiceAccount": {
    "AccessKeyId": "AKIARKLI**************",
    "SecretAccessKey": "cVSkOhunYxS****************************"
  }
}
```

### Development

The pipeline uses `requirements.txt` but there is also a Pipfile if you prefer pipenv for local development.  

**Pipenv setup**  
```
$ pipenv --python 3.10  
$ pipenv shell  
$ pipenv install --dev  
```
**Run unit tests**  
```
$ PYTHONPATH=.:./src coverage run -m pytest -vv -l  
$ coverage report  
```
