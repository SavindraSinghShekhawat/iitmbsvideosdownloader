IITM BS Videos Downloader
===============
Python Bot Library to download IITM BS videos.

visit for latest versions

GitHub - https://github.com/SavindraSinghShekhawat/iitmbsvideosdownloader

PyPI - https://pypi.org/project/iitmbsvideosdownloader/



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



# Installation help for Windows



#### 1) Download Brave browser 

**Why?**	We require brave because it removes ads and pop-ups, hence helps download videos from third party sites like y2mate.

If brave is already installed on your system skip to next step

else download from [here](https://brave.com/).



#### 2)  Make sure you are logged in to any of the course in your Brave browser

![image-20230211173744426](C:\Users\Shekh\AppData\Roaming\Typora\typora-user-images\image-20230211173744426.png)





#### 3) Install python in your system.

​	If python is already installed on your system find it's path and skip to next step

​	otherwise install from Microsoft store [here](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5).

​	Python should be installed in this location if installed from Microsoft store. This path will be used in

​	upcoming Steps.

```
C:\Users\<user-name>\AppData\Local\Microsoft\WindowsApps\python3.10.exe
```

**Note** - Make sure to replace <user-name> with your folder name.



#### 4) Install PyCharm.

You can use other IDE like Spyder too, But if you don't know much about what is going on, we recommend you to download PyCharm to  follow all the steps easily. 

Download **Community Version** and not the Professional version.

![Screenshot 2023-02-20 081450](D:\document_imgs\Screenshot 2023-02-20 081450.png)

Can be downloaded based on system from [here](https://www.jetbrains.com/pycharm/download) and install with default options.

if already installed skip to next step otherwise download and install with default options.



#### 5) Open PyCharm and create a new project

![Screenshot 2023-02-11 174524](D:\document_imgs\Screenshot 2023-02-11 174524.png)

![Screenshot 2023-02-11 174802](D:\document_imgs\Screenshot 2023-02-11 174802.png)



#### 6) Remove all the code from main.py and replace with this below code.

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



#### 7)  Install Package iitmbsvideosdownloader

hover mouse on iitmbsvideosdownloader and click on **install package iitmbsvideosdownloader** 

![Screenshot 2023-02-20 085939](D:\document_imgs\Screenshot 2023-02-20 085939.png)



#### 8) Know your executable_path and profile_path

![Screenshot 2023-02-20 060014](D:\document_imgs\Screenshot 2023-02-20 060014.png)





#### 9) Change the arguments based on your system and browser. 

**Note** - We have used **r** before string in paths arguments, in python it's called raw string and it's helpful while providing paths, so make sure your paths have this **r** before string

```python
r"this is an example of raw string"
```

**executable_path**: path of the browser (can be found in Step 8)

**profile_path**: browsers save user's data at a specific location, please provide that here. (can be found in Step 8)

**download_path**: where you want to save all the bot's downloaded videos, set the directory location here.

**subjects**: use SUBJECTS module to provide a list of your subjects

**year**: current year

**term**: one digit integer that tells current term (1 for Jan Term, 2 for May Term, 3 for Sep Term)

**week**: current week, so bot knows which week to download



#### 10) close your brave browser

It's required to make sure the brave browser is closed before you run code.



#### 10) Run the program and let the bot do it's work

![Screenshot 2023-02-20 090204](D:\document_imgs\Screenshot 2023-02-20 090204.png)





## How to update?

Go to **File -> Settings** from top Left in PyCharm (make sure project is opened)

Then select your **Project -> Python Interpreter** from left side

![Screenshot_20230227_082129](D:\document_imgs\Screenshot_20230227_082129.png)





## Common Issues

1) **Site y2mate.com is not working** 

   Change site to Y2meta by setting optional parameter **download_site** to **SITES.Y2META**

   new code will look like this.

   ```python
   from iitmbsvideosdownloader import SUBJECTS, SITES, iitmbsvideosdownloader
   
   mySmartBot = iitmbsvideosdownloader.SmartBot(
       executable_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
       profile_path=r"C:\Users\Shekh\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default",
       download_path=r"D:\Term 7",
       subjects=[
           SUBJECTS.AI_SEARCH_METHODS_FOR_PROBLEM_SOLVING,
           SUBJECTS.DEEP_LEARNING,
           SUBJECTS.SOFTWARE_ENGINEERING,
           SUBJECTS.STRATEGIES_FOR_PROFESSIONAL_GROWTH
       ],
       year=2023,
       term=1,
       week=6,
       download_site=SITES.Y2META
   )
   
   mySmartBot.start()
   ```

   



## Installation help for Linux

If you are already using Linux you most probably know all this 

Please visit [iitmbsvideosdownloader](https://github.com/SavindraSinghShekhawat/iitmbsvideosdownloader) to know how to install using pip



### Feedback Form

https://forms.gle/JDhu8jASp4N7XBMy8



### Contact

Did this package helped you save some time? or any suggestions? or still facing issues?

Contact  -  Savindra Singh Shekhawat

[Whatsapp me](https://wa.me/919983231619) <img src="https://cdn3.iconfinder.com/data/icons/social-media-logos-flat-colorful/2048/5302_-_Whatsapp-512.png" style="zoom:5%;" />

[Mail me](mailto:shekhawatsavindra@gmail.com) <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOYspkAWJY74CUU5acHxefxmP49bUMqhcbbw&usqp=CAU" style="zoom:10%;" />
