
# D&B Home Assignment
#### Assignment Goal
Create a command-line application that, given a list of website URLs as input, visits them and finds, extracts and outputs the websites’ logo image URLs and all phone numbers (e.g. mobile phones, land lines, fax numbers) present on the websites.

## Running The Application
- Download the repository zip file and extract the folder named "dbassign-master" to your desktop.
- Open the Command Prompt\PowerShell\Bash and navigate to the "dbassign-master" folder.
- Build the docker image using the following command `docker build -t dnb .`

#### Using Windows Command Prompt
- Run the docker image using the following command `docker run -i dnb < [PATH_TO_TXT_FILE]`

#### Using Powershell or Bash
- Run the docker image using the following command `cat [PATH_TO_TXT_FILE] | docker run -i dnb`

## Application Overview
#### Application arguments
The application support two arguments:

-  `-v, --verbose` - Print logs to std.err during application run. **For example**
`docker run -i [IMAGE_NAME] -v < [PATH_TO_TXT_FILE]`

-  `-t, --threads` - Specifying how many threads to use. Default is 16. **For example**
`docker run -i [IMAGE_NAME] -t [NUM_OF_THREADS] < [PATH_TO_TXT_FILE]`

#### Website's logo extraction method
After research during the assignment, I found two main methods to extract the website's logo. 
1. Search the `<link>` tag that stores the favicon inside the `<head>` tag and extracts the website's logo.
2. Search the first `<img>` or `<svg>` tags that appear inside the `<body>` tag while assuming that, in absolute most cases, the first image is the website's logo.

After quite long consideration, I decided to use method number two while comparing my results to the example result you attached to the assignment description.