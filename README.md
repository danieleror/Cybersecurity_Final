# Daniel Eror - Final Lab

### Brief Overview

This program is an advanced spinoff of my original lab in this class. It's an extremely simple mockup of a website for a
coffee shop. Users can register with a username and password, and if they have the right access level, they can view 
certain data. All users can view the coffee shop's menu, regardless of their access level. If a user tries to manually 
access a page by entering its name into the search bar (such as /admin), my flask app automatically re-routes the user 
to the unauthorized page, assuring that only those with the right level can access certain pages.

As for security, all passwords are salted and hashed. Additionally, I prevent SQL injection the same way we did in the 
lab, by avoiding a sql statement from executing if the variable entered by the user contains quotes. 

When registering, users are required to have a strong password. My registration page contains a suggested password 
function that you can refresh as many times as you'd like to generate a strong password that meets all requirements.

I use sqlite to interact with my database, which allows me to save data long-term. Currently, my online shop does not 
allow for modification of data (other than the addition of a new user when registering)

### Setup - How to Run

To run my program, be sure that after unzipping the compressed file, all contents are in the same directories they were 
originally in. Then, simply run `coffee_shop_runner.py` either in an IDE or through the command line. This will run the
flask app, and all subsequent instructions are given in the web page. 

For login info, there is a file named `login_data.csv` with plaintext usernames and passwords of users with different 
access levels. This file is only included because this is a small project and this database has no sensitive data. In 
the real world, I would not have this information in a file like this as it is a serious vulnerability and would make
hashing the passwords irrelevant. You can use this login data to test different access levels, and see how my program
reacts to users with lower access trying to access admin level data.