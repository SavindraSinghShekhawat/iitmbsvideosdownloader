from iitmbsvideosdownloader import SUBJECTS, SITES, iitmbsvideosdownloader

mySmartBot = iitmbsvideosdownloader.SmartBot(
    executable_path=r"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    profile_path=r"/Users/savi/Library/Application Support/BraveSoftware/Brave-Browser/Profile 1",
    download_path=r"/Users/savi/Education/IITM",
    subjects=[
        SUBJECTS.INTRODUCTION_TO_BIG_DATA,
        SUBJECTS.MATHEMATICAL_THINKING,
        SUBJECTS.SPECIAL_TOPICS_IN_MACHINE_LEARNING_REINFORCEMENT_LEARNING
    ],
    year=2024,
    term=2,
    week=1,
    download_site=SITES.Y2MATE
)

mySmartBot.start()
