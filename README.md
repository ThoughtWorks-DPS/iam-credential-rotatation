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

A common practice for AWS infrastructure automation is the use of AWS IAM User accounts that represent machine-users rather than humans, also commonly referred to as service-accounts. Typically, these machine-user accounts do not have any permissions per se, apart from being able to assume specific roles when performing automated tasks, such as within the context of an infrastructure pipeline.  

When using such service account, it is an important practice to rotate the credentials frequently; usually every 30-90 days.  

Rotating credentials usually means deleting the existing credentials and then generating new ones. But what happens if you delete an existing set of credentials while there is a current automated job or pipeline running?

It may be dificult to confidently chose a time to rotate credentials where there isn't some risk of causing currently running jobs to fail.  

However, if I maintain two sets of credentials, with the most recent set being the credentials available in my secrets store (which is where automated jobs fetch credentials when they start). Now I can confidently delete the older of the two credentials, generate new credentials, and update my secrets store with the new, with no fear of causing any system failure. Both the new credentials and the prior credentials used by any jobs still in flight will remain valid until the next time I perform a rotation. And if I set my rotation window to 1/2 my desired time period then I know that all keys are completely replaced within the period.    

Example: Suppose a weekly CIS AWS Foundation security scan takes 5-6 hours to complete. The IAM User machine-account used by the job has two sets of IAM User credentials at any given time, with the most recently created credentials being those stored in the secrets store and actually used by the job.  

Performing a CURRENT/LAST two-key rotation means deleteing the older of the two IAM User credentials from AWS. Those credentials are no longer in use since it is only the most recent keys that are stored in the secrets store and used by the job. Then, generate a new set of credentials and write these new credentials to the secrets store. 

In this way, if our CIS job is running when we perform this rotation, it can continue to rely upon the credentials it fetched from the secrets store when it launched since, though they are now the older of the two within AWS, they are still valid keys. The next time the job runs it will fetch its credentials from the secrets store and as these are now the newest keys, the job will run successfully.  

## Install

```bash
pip install iam-credential-rotation
```

## Usage

iam-credential-rotation [OPTIONS] PATH  

Where PATH is the IAM User path location of the IAM Users that represent machine-users. For each user in PATH, their oldest credentials are deleted and a new set of credentials is created. By default, the new key-pairs are written to stdout.   

Options:  

-o, --outfile TEXT   # if desired, rather than piping results to a file you can directly provide a filename.  

### Development
