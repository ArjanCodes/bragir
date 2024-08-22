# Vulnerability Disclosure
If you believe you have identified a security vulnerability in Bragir, please reach out directly to the project maintainers. Do not open a public issue or disclose the vulnerability in any public forum.

## Contact Information
Please contact the core maintainers directly for any security-related concerns.

## Non-English Reports
If English is not your first language, please do your best to describe the issue and its potential impact. If more comfortable, you may provide details in your native language.

## Required Information
When reporting a vulnerability, please include:

A detailed description of the problem and its potential impact.
The code you used to discover the problem.
The minimal amount of code necessary to reproduce the issue.

**Please do not disclose this vulnerability to anyone else**. We will manage the disclosure process, including obtaining a CVE identifier if necessary, and will credit you as the discoverer under your chosen name or alias.

You will only be mentioned publicly with your permission.

## Process
### Initial Response
When you report a vulnerability, a project member will respond within two days, usually much faster. The initial response will confirm receipt of the report and may also include confirmation of the issue if it has been quickly reproduced. If not, we might ask for additional information.

### Fix Timeline
The goal is to release a fix within two weeks of the initial disclosure. This might involve shipping an interim release that temporarily disables the affected functionality while a more permanent fix is developed. You will be informed throughout this process and may ask for your assistance in verifying the fix.

### Release Preparation
Once a fix is ready, we will:

1. Notify you that we believe the issue has been resolved.

2. Coordinate with major downstream packagers to inform them of the upcoming security patch and provide them with the patch in advance.

## Contacts:

Andreas Bergman, ArjanCodes (@ABDreos)

If you believe you should be included in this notification list, please contact the maintainers.

On the planned release date (always on a weekday):

* Push the patch to our public repository.
* Issue a new release on PyPI.
* Public Announcement
* After the release, we will publicize the patch through all available channels, including mailing lists and social media. We will also specify which commits contain the fix, to make it easier for others to apply the patch if upgrading is not immediately feasible.