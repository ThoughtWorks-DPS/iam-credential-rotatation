<div align="center">
	<p>
		<img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=200 />
    <br />
		<img alt="DPS Title" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/EMPCPlatformStarterKitsImage.png?sanitize=true" width=350/>
	</p>
  <br />
  <h3>iam-credential-rotation</h3>
    <a href="https://app.circleci.com/pipelines/github/ThoughtWorks-DPS/iam-credential-rotation"><img src="https://circleci.com/gh/ThoughtWorks-DPS/iam-credential-rotation.svg?style=shield"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
</div>
<br />

Command line tool for automated rotation of AWS IAM machine-user credentials, following a CURRENT/LAST two-key pattern.  

A common practice for AWS infrastructure automation is the incorporated use of AWS IAM User accounts that represent Machine_users rather than humans. These are also commonly referred to as service-accounts. Humans may also have IAM User accounts, though it is quite common to create an Identity Federation within AWS that enables human to use their Corporate credentials (for example).

Regardsless, where IAM User accounts are used, it is an important practice to rotate the credentials frequently; every 30-90 days for example. For their own credentials, humans can just perform the rotation directly, saving the new credentials, without fear that any systems or services will be impaired.  

In the case of machine-user accounts, at any given point in time there may be an automated event taking place that uses the machine-user credentials. If I were to directly, or indirectly through another automation, invalidate the set of credentials in use by that automated event before it is completed it could fail. With extensive automation in place, it may be dificult to confidently chose a time to rotate credentials where there isn't some risk of causing currently running jobs to fail.  

However, if I maintain two sets of credentials, with the most recent set being the credentials available in my secrets store (which is where automated jobs fetch credentials when they start). Now I can confidently delete the older of the two credentials, generate new credentials, and update my secrets store with the new, with no fear of causing any system failure. Both the new credentials and the prior credentials used by any jobs still in flight will remain valid until the next time I perform a rotation.  

A common rotation window when using this pattern is every 15 days. In this case, any particular set of credentials will only be in valid for 30 days maximum, though in practice the credentials actual in use will be no older than 15 days plus their maxmimum time to complete.

Example: Suppose a weekly CIS AWS Foundation security scan takes 5-6 hours to complete. The IAM User machine-account used by the job has two sets of IAM User credentials at any given time, with the most recently created credentials being those stored in the secrets store and actually used by the job.  

Performing a safe CURRENT/LAST two-key rotation means deleteing the older of the two IAM User credentials from AWS. Those credentials are no longer in use since it is only the most recent keys that are stored in the secrets store and used by the job. Then, generate a new set of credentials and write these new credentials to the secrets store. 

In this way, if our CIS job is running when we perform this rotation, it can continue to rely upon the credentials it fetched from the secrets store when it launched since, though they are now the older of the two within AWS, they are still valid keys. The next time it runs, in this case next week, it will fetch its credentials from the secrets store and as these are now the newest keys, the job will run successfully.  

This will work well so long as these long-running jobs do not exist for longer than twice the length of our automatic key-rotation period. 30-day plus runtimes should not be considered a good idea.  

## Install

```bash
pip install iam-credential-rotation
```

## Usage

iam-credential-rotation [OPTIONS] PATH  

Where PATH is the IAM User path location of the IAM Users that represent machine-users (also referred to as service accounts) used in infrastructure pipelines and other automation.  

Options:  
-o, --outfile TEXT   # if desired, rather than piping results to a file you can directly provide a filename.  

### Development

1. setup venv
2. python setup.py develop
3. python -m build
4. python3 -m twine upload --repository testpypi dist/*  

