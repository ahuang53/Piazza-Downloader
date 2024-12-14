# Piazza-Downloader

## Setup:
Install Piazza API https://github.com/hfaran/piazza-api and any other missing libraries

## Use:
1. Navigate to the piazza course that you would like to download on your browser and go to the resources tab.
2. Inspect the page (right click -> inspect or F12). 
3. In the top-middle of the inspect dialog, click Sources
4. Download the resources file as an html file and save it into this folder
5. Run main.py and all files will be in the downloaded_resources folder
Make sure to choose the correct course that you are downloading as different courses will have different resources.html files. 

If you don't want to login in repeatedly, go to line 91 in the code (under main), and fill in your email and password.

When asked, "Which class are you downloading from:", input which number the class corresponds to not, not the title of the course.

Some of the section names may be named incorrectly so review the folders and modify to your liking. 

## Disclaimer for Unofficial Piazza Downloader
### Important Notice:

This tool is an unofficial downloader for Piazza, created for educational and personal use only. It is not affiliated with, endorsed by, or sponsored by Piazza or any of its associated organizations.

### Usage Guidelines:

The downloader is intended solely for the retrieval of content you have the right to access.
Users are responsible for ensuring compliance with Piazza's terms of service, community guidelines, and copyright regulations.
Downloading or distributing content without proper authorization may violate intellectual property laws or the rights of others.
Risks:

By using this tool, you acknowledge that there may be risks involved, including potential changes to Piazza's interface, functionality, or terms of service, which could affect the downloader's performance.
Use this tool at your own risk. The developers do not assume any liability for any damages or issues arising from its use.
Privacy and Security:

The downloader may require your Piazza credentials for authentication. Please use caution and ensure your information is secure.
The developers do not store or share any personal information or credentials.
By using this unofficial downloader, you agree to these terms and acknowledge your responsibility to use it appropriately.

