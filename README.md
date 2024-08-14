# A2A Reporting Application

A2A Reporting Application captures both Message Processing Logs and Integration Content from SAP CPI
and displays this data on a webpage where the user can search for specific Integration Flows and use various 
filters. The user can hen export these resulsts as a csv file.

## Installation 

A2A Reporting Application can be installed locally by the following the subsequent steps

```bash
git clone https://github.com/amd-eaoleary/a2a_reporting_application.git

cd a2a_reporting_application

python3 -m venv myenv

myenv\Scripts\Activate

pip install -r requirements.txt
```