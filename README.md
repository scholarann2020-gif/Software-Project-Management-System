Software Project Management System (SPMS)
1. Overview

The Software Project Management System (SPMS) is a desktop-based application developed using Python (Tkinter) for the graphical user interface and SQL Server / MySQL for backend data management. The system is designed to assist software organizations in efficiently planning, executing, monitoring, and controlling software development projects.

SPMS enables project managers, employees, administrators, and clients to collaborate through a single application by tracking projects, tasks, financials, and reports in a structured and transparent manner. The system reduces manual effort, improves accountability, and enhances overall project visibility.

2. Key Features
2.1 User Authentication

Secure role-based login system

User roles include:

Admin

Project Manager

Employee

Client

Ensures controlled access to system functionalities

2.2 Dashboard

Centralized overview of:

Ongoing and completed projects

Task progress and workload distribution

Budget utilization

Recent activities and upcoming deadlines

Provides quick insights for decision-making

2.3 Project Management

Create and manage projects with detailed attributes:

Project title and description

Start and end dates

Assigned manager and client

Project budget

Status (Planned, In Progress, Completed, On Hold)

Monitor overall project progress in real time

2.4 Task Management

Divide projects into multiple tasks

Assign tasks to employees

Define deadlines and priorities

Track task status:

Pending

In Progress

Completed

Maintain task update history

2.5 Client Management

Store client information securely

Associate clients with multiple projects

Allow clients to view project progress and reports

Maintain professional transparency

2.6 Billing and Finance

Track project budgets

Generate invoices based on milestones or project phases

Record payments and outstanding balances

Provide financial summaries per project

2.7 Reports

Generate detailed reports for:

Project progress

Task completion

Financial transactions

Export reports in:

CSV format

PDF format

2.8 Recent Activity Monitoring

View tasks updated on the current day

Identify approaching deadlines

Highlight delayed or overdue tasks

Assist managers in proactive issue resolution

3. System Objectives

Automate software project management processes

Improve collaboration between stakeholders

Enhance transparency and accountability

Reduce project delays and budget overruns

Provide accurate reporting and documentation

4. Scope of the System

The SPMS covers:

User and role management

Project and task lifecycle management

Client and employee data handling

Financial tracking and reporting

Activity monitoring and reporting

The system is suitable for small to medium-sized software organizations and operates as a desktop application, making it effective in environments without continuous internet access.

5. User Roles and Responsibilities
Admin

Manage users and roles

View and control all system data

Generate system-wide reports

Project Manager

Create and manage projects

Assign tasks to employees

Track project timelines and budgets

Communicate with clients

Employee

View assigned tasks

Update task progress

Submit work-related remarks

Client

View assigned projects

Monitor progress

Access invoices and reports (read-only)

6. System Architecture

The SPMS follows a three-tier architecture:

Presentation Layer

Tkinter-based GUI

User interaction and navigation

Application Layer

Python business logic

Validation, workflows, and access control

Database Layer

SQL Server / MySQL

Secure data storage and retrieval

7. Database Design (High-Level)
Core Tables

Users

Roles

Projects

Tasks

Clients

Invoices

Payments

Activity_Log

Relationships

One project → multiple tasks

One client → multiple projects

One project → multiple invoices

8. Technologies Used
Component	Technology
Programming Language	Python 3.x
GUI Framework	Tkinter
Database	SQL Server / MySQL
Database Connector	pyodbc / mysql-connector-python
Reporting	CSV / PDF
Operating System	Windows
9. Installation and Setup
9.1 Prerequisites

Python 3.x

Tkinter (included with Python)

MySQL or SQL Server

Required Python libraries:

mysql-connector-python (for MySQL)

pyodbc (for SQL Server)

9.2 Installation Steps

Clone the repository:

git clone https://github.com/username/SPMS-Tkinter.git


Navigate to the project directory:

cd SPMS-Tkinter


Install required dependencies:

pip install -r requirements.txt


Configure the database connection:

Update database credentials in the configuration file

Import the provided SQL schema

Run the application:

python main.py

10. Non-Functional Requirements

User-friendly interface

Secure data access and storage

High performance and reliability

Scalable and maintainable architecture

Error handling and logging

11. Limitations

Desktop-based only

No real-time cloud synchronization

Requires local database setup

12. Future Enhancements

Web-based version (Django / Flask)

Mobile application support

Real-time notifications

Advanced analytics dashboards

Integration with Git and CI/CD tools

13. Conclusion

The Software Project Management System (SPMS) provides a comprehensive and efficient solution for managing software projects. By integrating project tracking, task management, billing, and reporting into a single desktop application, SPMS enhances productivity, transparency, and project success rates.