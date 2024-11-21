# Daniel Eror - Lab 1

My program utilizes a login data file that contains all information necessary for users to login and access appropriate 
menus/systems. Subsequently, there is a menus folder with all menus for my program, which imitates a made-up coffee 
shop. Each menu csv contains access information regarding who can read and write to each menu. For now, only
the read function is implemented, and I hope to incorporate a write function in the future.

My program is set up in a way such that I can add as many menu csv files as I want, and the code will automatically read
through each file in that directory. This future-proofs the code so that adding more menus is as simple as creating the 
file. 

To use my program, simply view `login_data.csv` to see the four users I created, all with different levels of access. 
Running the program will initiate prompts, and all necessary directions are given to you through output in the console.
