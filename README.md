

IITM BS Videos Downloader
===============
Python Bot Library to download IITM BS videos.


Installing
============
[Visit step by step guide to installation](https://drive.google.com/file/d/17R6Jt01sYyVlmPfkB0dUMLwxjYnHKzTs/view?usp=sharing)

```bash
pip install iitmbsvideosdownloader
```

## How it Works?

The bot is basically a Python Package. It opens the browser then gets videos links from portal and goes to third party sites like Y2mate and downloads videos one by one.

So just one click and all the boring stuff regarding downloading videos bot can handle.



## Features

- Auto Retries if failed to download a video
- Skips videos if already downloaded
- Renames videos to the names written on Portal (ex: L1.2 - )
- Other tasks can be done on PC while it's running



### Tools required

- Python Setup
- IDE for Python (PyCharm, Spyder etc)
- Brave Browser


### Example for Windows

```python
from iitmbsvideosdownloader import SUBJECTS, SITES, iitmbsvideosdownloader

mySmartBot = iitmbsvideosdownloader.SmartBot(
    executable_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    profile_path=r"C:\Users\Shekh\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default",
    download_path=r"D:\Term 8",
    subjects=[
        SUBJECTS.AI_SEARCH_METHODS_FOR_PROBLEM_SOLVING,
        SUBJECTS.DEEP_LEARNING,
        SUBJECTS.SOFTWARE_ENGINEERING,
        SUBJECTS.STRATEGIES_FOR_PROFESSIONAL_GROWTH
    ],
    year=2023,
    term=2,
    week=1,
)

mySmartBot.start()
```

In the Code:

**executable_path**: path of the browser

**profile_path**: browsers save user's data at a specific location, please provide that here.

**download_path**: where you want to save all the bot's downloaded videos, set the directory location here.

**subjects**: use SUBJECTS module to provide a list of your subjects

**year**: current year

**term**: one digit integer that tells current term (1 for Jan Term, 2 for May Term, 3 for Sep Term)

**week**: current week, so bot knows which week to download



## Install using pip

1) make sure you are logged in to your Brave browser on any of the course (on seek portal) and if already logged in then close the browser
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

