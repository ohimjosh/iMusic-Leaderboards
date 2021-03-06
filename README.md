# iMusic Leaderboards

# Overview 
Data set: https://www.kaggle.com/leonardopena/top50spotify2019
- Will be using SQLite and SQLAlchemy
- Users should be able to create an account and add music to their follow list.
- Must be able to remove music they are following and Close Account
- Must be able to Update their information

# Specification/Requirement

**Objective: The purpose of this project is to implement databases into a Full stack application.**

**I. Application** 
1. Must be able to create, read, update, delete in the application. 
2. Create a login and register page that asks for user to login and access the
application. Ability for the user to logout from the session.

**II. Documentation**<br/>
Form a group of 2 – 4 people this report must consist of the following:
1. The team member's names and emails. 
2. The team name. 

Describe the software in roughly three paragraphs. Address the following questions:<br/>
- What is the purpose of the software? 
- Why is the software interesting? 
- What existing product is like the project you are proposing? 
Create a complete diagram of the application and how it will work. 

The schemas for the database the software will be using. Anywhere between 7-12 is
typical for a small project, you may have more. 

The software application must include a “manual” or “tutorial” of some sort which
explains the software’s use and features. 
- The documentation clearly describes the purpose and design of the software.
- The database must be creatable from SQL scripts, and the schemas must be
documented and accompanied by ER diagrams. (Hand drawn and
photographed is fine.)
- The schemas are in normal form; they should be in third normal form.
- I should be able use the software to create, update, and delete records
describe how you did it in the documentation. 

> While the software does not have to be “bug free", I should not encounter bugs while
performing the documented operations, or variations thereof. 
# Cloning The Project
    On vscode, click on clone repository on the main explorer page 
    and input the repository URL into the pop-up box.
# Installing SQLite
    - Go to SQLite download page, and download precompiled binaries from Windows(or whatever your OS is) section.
    - Download bundled zipped files.
    - Create a folder C:\>sqlite and unzip above two zipped files in this folder, which will give you sqlite3.def, sqlite3.dll and sqlite3.exe files.
    - Add C:\>sqlite in your PATH environment variable and finally go to the command prompt and issue sqlite3 command, which should display your sqlite version
# Working on Virtual Environment with Flask
    - Need to install pip 
    - Upgrade pip by $ py -m pip install --upgrade pip
    - $ python3 -m venv venv (For VSC, you need to click yes for Python extension pop-up)
    - $ source venv/bin/activate
# Set-Up the program
    - $ pip install -r requirements.txt  //install all packages needed
# Run the Program 
    - $ flask run
