import os

NUM_LEVELS_ACCESS = 4


def read_menus_into_dict():
    menus = {}
    for menu_filename in os.listdir('menus'):  # iterates through every menu file in the menu directory
        menu_file = open('menus/' + menu_filename, "r")
        menu_name = menu_file.readline().strip()
        menus[menu_name] = {}
        menus[menu_name]["access"] = {}  # creates dict with all access types
        for level in range(NUM_LEVELS_ACCESS):
            data = menu_file.readline().strip().split(',')
            menus[menu_name]["access"][data[0]] = data[1].split(' ')  # adds list that contains 'r', 'w', or both

    return menus


def main():
    login_data = open("login_data.csv", "r")
    user_info = {}  # creates empty dict
    for line in login_data:
        line = line.strip()  # gets rid of \n
        pieces = line.split(',')
        user_info[pieces[0]] = {}  # assigns an empty dict to the username
        user_info[pieces[0]]["password"] = pieces[1]
        user_info[pieces[0]]["access"] = pieces[2]

    # attempts to read menu data. If unsuccessful, this boolean is set to false and the rest of the program does not run
    read_menus_successful = True
    try:
        menus = read_menus_into_dict()
    except IOError:
        print("Error reading menu files... program unable to run and will now terminate.")
        read_menus_successful = False

    if read_menus_successful:
        print("Welcome to Dan's Coffee Shop! Please enter your username: ")
        username = input()
        while username not in user_info:  # repeatedly asks for a username until one has been found
            username = input("Username not found, please try again: ")
        password = input("Hi " + username + ", please enter your password: ")
        while password != user_info[username]["password"]:  # asks for password until the correct one is entered
            password = input("Incorrect password, please try again: ")
        print("Login successful... see menu options below:")
        for option in menus:
            print(option)
        print()  # line for spacing
        menu_selected = input("Please enter a menu you'd like to access: ")
        valid_input = False
        while not valid_input:
            if menu_selected not in menus:  # event in which user enters a menu that does not exist
                menu_selected = input("Input does not match menu options, please try again: ")
            elif 'r' not in menus[menu_selected]['access'][user_info[username]['access']]:  # user does not have access
                menu_selected = input("You are not authorized to access this menu.\n"
                                      "Please select a different one or contact your administrator:")
            else:
                valid_input = True  # user has selected a menu that exists and has proper access to, so the loop terminates
        print("You have successfully accessed the " + menu_selected + " menu. This program will now terminate...")


if __name__ == '__main__':
    main()
