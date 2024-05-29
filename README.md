# ArchivesSpace Data Auditor

## Overview
This script is designed to run on a server with access to an ArchivesSpace installation. It runs a series of checks 
in the ArchivesSpace database, accessing data through the API, and exporting and evaluating EAD.xml files for content 
and syntax errors. The script then generates an Excel spreadsheet detailing where there are any areas for data cleanup.
For more information about what data is checked, see the [Workflow](#workflow) section.

## Getting Started

### Dependencies

- [lxml](https://lxml.de/) - Used to parse XML files for evaluating any XML syntax errors and parsing data from 
downloaded XML files
- [mysql](https://dev.mysql.com/doc/connector-python/en/) - Used to import mysql-connector
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) - Used to connect and detect any connection 
errors to the ArchivesSpace MySQL database
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) - Used to create and write an Excel spreadsheet to document
data audit report
- [requests](https://docs.python-requests.org/en/latest/index.html) - Used to check URLs and get their status codes

### Installation

1. Download the repostiory via cloning to your local IDE or using GitHub's Code button and Download as ZIP
2. Run `pip install requirements.txt`
3. Create a secrets.py file with the following information:
   1. An ArchivesSpace admin username, password
   2. The URLs to your ArchivesSpace staging and production API instances
   3. Variables with their values set to user emails you want to send the report to
   4. The email server from which you send your email report
   5. Your ArchivesSpace's staging database credentials, including username, password, hostname, database name, and port
4. Run the script as `python3 ASpace_Data_Audit.py`

### Script Arguments
Open the console of your choice and navigate to the project directory. Type `python3 ASpace_Data_Audit.py` to run the 
script. If you want to run the audit without emailing users of the result, add -t or --test, so 
`python3 ASpace_Data_Audit.py -t`. The testing functionality is still being developed and may not function properly.

### Testing
There are a series of unittests that check various functions in ASpace_Data_Audit.py. They are still being developed and
any test should be run with the `-t` or `--test` argument as listed in # Script Arguments

## Workflow

1. Generate an Excel spreadsheet to use for our report
2. Begin running the audit. The audit checks for the following:
   1. Any new controlled vocabulary terms for the following and highlights the row in red:
      1. Subject_Term_Type
      2. Subject_Sources
      3. Finding_Aid_Status_Terms
      4. Name_Sources
      5. Instance_Types
      6. Extent_Types
      7. Digital_Object_Types
      8. Container_Types
      9. Accession_Resource_Types
   2. Any archival objects with component unique identifiers
   3. Any top containers without barcodes
   4. Any top containers without indicators
   5. A list of all current users
   6. Any archival objects with multiple top containers
   7. Any archival objects with multiple digital objects
   8. Any archival objects listed as level of description == collection
   9. Any resources with EAD IDs
   10. Any duplicate subjects
   11. Any duplicate agent-persons
   12. Any resources without Creator agents
   13. Any XML syntax errors in exported EAD.xml files
   14. Any broken URLs in EAD.xml exports
   15. Any top containers not linked to any resources or archival objects
   16. Any archival objects with "otherlevel" and "unspecified" level of description
3. Save the spreadsheet and send an email using email_users(). If an error is generated, send a message to specified 
user
4. Delete the spreadsheet and exported EAD.xml folder and files from the server - email if there is an error

## Author

- Corey Schmidt - Project Management Librarian/Archivist at the University of Georgia Libraries

## Acknowledgements

- Kevin Cottrell - GALILEO/Library Infrastructure Systems Architect at the University of Georgia Libraries
- ArchivesSpace Community
    

