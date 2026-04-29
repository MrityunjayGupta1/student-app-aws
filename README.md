# Student Management App on AWS

Simple student management app deployed on AWS EC2.roject is built to demonstrate core DevOps concepts including cloud deployment,
database management, file storage, and server monitoring.

The application allows users to add students with their name, roll number and marks.
All student data is permanently stored in a cloud database and automatically backed 
up to cloud storage after every entry.

AWS Services Used

| Service | Purpose |
|---------|---------|
| EC2 | Cloud server that runs the Flask application |
| RDS MariaDB | Managed database that stores student data permanently |
| S3 | Cloud storage for automatic student data backups |
| IAM | Manages permissions and roles securely |
| CloudWatch | Monitors EC2 server CPU and sends alerts |
| Security Groups | Controls inbound and outbound traffic to EC2 and RDS |

What This Project Demonstrates
- Deploying a Python Flask app on AWS EC2
- Connecting EC2 to a managed RDS MariaDB database
- Automatically backing up data to S3 on every transaction
- Securing infrastructure using IAM roles and Security Groups
- Monitoring server health using CloudWatch dashboard

#Project Architecture:
<img width="551" height="447" alt="Screenshot 2026-04-28 at 11 57 57 PM" src="https://github.com/user-attachments/assets/9fd20801-4bf8-4125-b97f-713b4afa3fd7" />


## How to Run
pip install flask
python app.py

## Project Structure
app.py - main Flask application

requirements.txt - python dependencies
