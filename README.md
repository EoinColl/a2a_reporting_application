# A2A Reporting Application

A2A Reporting Application captures both Message Processing Logs and Integration Content from SAP CPI
and displays this data on a webpage where the user can search for specific Integration Flows and use various 
filters. The user can then export these results as a csv file.

## Installation 

A2A Reporting Application can be installed locally by the following the subsequent steps

Clone the repo
```bash
git clone https://github.com/amd-eaoleary/a2a_reporting_application.git
```

Enter the directory
```bash
cd a2a_reporting_application
```

Create and activate a virtual enviroment
```bash
python3 -m venv myenv

myenv\Scripts\Activate
```

Install the requirements
```bash
pip install -r requirements.txt
```
## Usage

When running the application locally, ensure connection to the Dublin gateway on Global Protect

Run the application
```bash
python3 app.py
```

Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

This is the home page.
Use the navbar to access either section

![image](https://github.com/user-attachments/assets/53754f34-43b5-4510-ae2f-bbfb5bc3da82)

This is the page to view execution history

![image](https://github.com/user-attachments/assets/e6578a48-f211-4dbb-b92d-6c5ea483c28f)

Here is an example where process name, execution status and date range are specified

![image](https://github.com/user-attachments/assets/5683287c-db30-41c8-bf24-2f963e96de43)

This is the page to view integration content

![image](https://github.com/user-attachments/assets/14036dc9-560d-44fd-a748-1b02be1259fc)