# personal customizable data

MY_TERM = 7  # the folder will be renamed to "Term {MYTERM}"
WEEK = 3  # current week, helps in getting the right week videos from portal and creating folders
YEAR = 23  # current Year last 2 digits, helps in getting right url of iitm portal
TERM = 1  # current term of the year (1 for Jan, 2 for May, 3 for Sep)

# browser's location to run (prefer Brave)
BROWSER_LOCATION = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

# if more than 1 profile in browser, enter its location and profile folder name
# usually it's "Profile 1" for a second profile
USER_DATA_DIRECTORY = "C:\\Users\\Shekh\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"
PROFILE = "Default"  # leave it to "Default" if only one profile

# sleeps help in waiting for page to load, if your internet speed is good 2 is fine, try increasing if you face errors
SLEEP_TIME = 2

# Directory of current term
MAIN_DIRECTORY = f"D:\\Term {MY_TERM}"

# subjects with their subject_code, helps in creating folders for each subjects in MAIN_DIRECTORY and subject code
# allows to load iitm portal of the subject
SELECTED_SUBJECTS = {
    "AI - Search Methods for Problem Solving": "cs3003",
    "Deep Learning": "cs3004",
    "Software Engineering": "cs3001",
    "Strategies for Professional Growth": "gn3001",
    "comment a subject if you don't want to download": "cs3002"
}

# sets logging to True, if you want to find out where something went wrong
DEBUG = True
VERBOSE = 4
