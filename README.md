IITM BS Videos Downloader
===============
Python Bot Library to download IITM BS videos.

Installing
============

```bash
pip install iitmbsvideosdownloader
```

Usage
=====

Example for Windows

```python
from iitmbsvideosdownloader import SUBJECTS, iitmbsvideosdownloader

mySmartBot = iitmbsvideosdownloader.SmartBot(
    browser_path="C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
    download_path="D:\\Term 7",
    user_data_path="C:\\Users\\Shekh\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data",
    profile_name="Default",
    subjects=[
        SUBJECTS.AI_SEARCH_METHODS_FOR_PROBLEM_SOLVING,
        SUBJECTS.DEEP_LEARNING,
        SUBJECTS.SOFTWARE_ENGINEERING,
        SUBJECTS.STRATEGIES_FOR_PROFESSIONAL_GROWTH
    ],
    year=23,
    term=1,
    week=4,
)

mySmartBot.start()
```

In the Code:

**browser_path**: path of the browser

**download_path**: where you want to save all the bot's work, huh?

**user_data_path**: browsers save user's data at a specific location, please provide that here.

**profile_name**: in the user_data_path you will have folders dedicated to your profiles, if you have only one profile in browser setting it to "Default"  works

**subjects**: use SUBJECTS module to provide a list of your subjects

**year**: two digit integer that tells current year

**term**: one digit integer that tells current term (1 for Jan Term, 2 for May Term, 3 for Sep Term)

**week**: current week, so bot knows which week to download



## Essential Steps

1) make sure you are logged in to your browser(Brave recommended) on any of the course (on seek portal) and if already logged in then close the browser
2) install the library using pip
3) paste the code above in Python Environment (PyCharm recommended)
4) change the code as per your system and needs
5) Run it and let the bot do it's work.



### Recommended for best results

Brave Browser - download from [here](https://brave.com/)

PyCharm - download from [here](https://www.jetbrains.com/pycharm/)



### Tip

Put all your current subjects in subjects argument and when you don't need to download any of them just comment out that subject.



### Contact

Did this package helped you save some time? or any suggestions?

Contact - 

Savindra Singh Shekhawat

shekhawatsavindra@gmail.com
