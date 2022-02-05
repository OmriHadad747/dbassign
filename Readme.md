# D&B Home Assignment
#### Assignment Goal
Create a command-line application that, given a list of website URLs as input, visits them and finds, extracts and outputs the websites’ logo image URLs and all phone numbers (e.g. mobile phones, land lines, fax numbers) present on the websites.

## Running The Application
- Download the repository zip file and extract the folder named "dbassign-master" to your desktop.
- Open the Command Prompt\PowerShell\Bash and navigate to the "dbassign-master" folder.
-  Build the docker image using the following command `docker build -t dnb .`
#### Using Windows Command Prompt
- Run the docker image using the following command `docker run -i dnb < [PATH_TO_TXT_FILE]`
#### Using Powershell or Bash
- Run the docker image using the following command `cat [PATH_TO_TXT_FILE] | docker run -i dnb`
## Application Overview
#### Application arguments
The application support two arguments:
- `-v, --verbose` - Print logs to std.err during application run.
	#### example
	`docker run -i [IMAGE_NAME] -v < [PATH_TO_TXT_FILE]`
	
- `-t, --threads` - Specifying how many threads to use. Default is 16.
	#### example
	`docker run -i [IMAGE_NAME] -t [NUM_OF_THREADS] < [PATH_TO_TXT_FILE]`