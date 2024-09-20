class _Subject:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code


COMPUTATIONAL_THINKING = _Subject("Computational Thinking", "cs1001")
PROGRAMMING_IN_PYTHON = _Subject("Programming in Python", "cs1002")
ENGLISH_I = _Subject("English I", "hs1001")
ENGLISH_II = _Subject("English II", "hs1002")
MATHEMATICS_FOR_DATA_SCIENCE_I = _Subject("Mathematics for Data Science I", "ma1001")
STATISTICS_FOR_DATA_SCIENCE_I = _Subject("Statistics for Data Science I", "ma1002")
MATHEMATICS_FOR_DATA_SCIENCE_II = _Subject("Mathematics for Data Science II", "ma1003")
STATISTICS_FOR_DATA_SCIENCE_II = _Subject("Statistics for Data Science II", "ma1004")

DATABASE_MANAGEMENT_SYSTEMS = _Subject("Database Management Systems", "cs2001")
PROGRAMMING_DATA_STRUCTURES_AND_ALGORITHMS_USING_PYTHON = _Subject(
    "Programming Data Structures and Algorithms using Python", "cs2002")
MODERN_APPLICATION_DEVELOPMENT_I = _Subject("Modern Application Development I", "cs2003")
# MODERN_APPLICATION_DEVELOPMENT_I = _Subject("Modern Application Development I", "cs2003p")
MACHINE_LEARNING_FOUNDATIONS = _Subject("Machine Learning Foundations", "cs2004")
PROGRAMMING_CONCEPTS_USING_JAVA = _Subject("Programming Concepts using Java", "cs2005")
MODERN_APPLICATION_DEVELOPMENT_II = _Subject("Modern Application Development II", "cs2006")
# MODERN_APPLICATION_DEVELOPMENT_II___PROJECT = _Subject("Modern Application Development II - Project", "cs2006p")
MACHINE_LEARNING_TECHNIQUES = _Subject("Machine Learning Techniques", "cs2007")
MACHINE_LEARNING_PRACTICE = _Subject("Machine Learning Practice", "cs2008")
# MACHINE_LEARNING_PRACTICE___PROJECT = _Subject("Machine Learning Practice - Project", "cs2008p")
BUSINESS_DATA_MANAGEMENT = _Subject("Business Data Management", "ms2001")
# BUSINESS_DATA_MANAGEMENT___PROJECT = _Subject("Business Data Management - Project", "ms2001p")
BUSINESS_ANALYTICS = _Subject("Business Analytics", "ms2002")
SYSTEM_COMMANDS = _Subject("System Commands", "se2001")
TOOLS_IN_DATA_SCIENCE = _Subject("Tools in Data Science", "se2002")

ALGORITHMIC_THINKING_IN_BIOINFORMATICS = _Subject("Algorithmic Thinking in Bioinformatics", "bt4001")
BIG_DATA_AND_BIOLOGICAL_NETWORKS = _Subject("Big Data and Biological Networks", "bt4002")
SOFTWARE_ENGINEERING = _Subject("Software Engineering", "cs3001")
SOFTWARE_TESTING = _Subject("Software Testing", "cs3002")
AI_SEARCH_METHODS_FOR_PROBLEM_SOLVING = _Subject("AI - Search Methods for Problem Solving", "cs3003")
DEEP_LEARNING = _Subject("Deep Learning", "cs3004")
INTRODUCTION_TO_CRYPTOGRAPHY_AND_CYBER_SECURITY = _Subject("Introduction to Cryptography and Cyber Security", "cs3005")
INTRODUCTION_TO_BIG_DATA = _Subject("Introduction to Big Data", "cs3006")
PRIVACY_SECURITY_IN_ONLINE_SOCIAL_MEDIA = _Subject("Privacy and Security in Online Social Media", "cs3007")
DATA_VISUALIZATION_DESIGN = _Subject("Data Visualization Design", "cs4001")
SPECIAL_TOPICS_IN_MACHINE_LEARNING_REINFORCEMENT_LEARNING = _Subject(
    "Special topics in Machine Learning (Reinforcement Learning)", "cs4002")
THEMATIC_IDEAS_IN_DATA_SCIENCE = _Subject("Thematic Ideas in Data Science", "cs4003")
SEQUENTIAL_DECISION_MAKING = _Subject("Sequential Decision Making", "cs4004")
SPEECH_TECHNOLOGY = _Subject("Speech Technology", "ee4001")
STRATEGIES_FOR_PROFESSIONAL_GROWTH = _Subject("Strategies for Professional Growth", "gn3001")
FINANCIAL_FORENSICS = _Subject("Financial Forensics", "gn3002")
LINEAR_STATISTICAL_MODELS = _Subject("Linear Statistical Models", "ma2001")
DESIGN_THINKING_FOR_DATA_DRIVEN_APP_DEVELOPMENT = _Subject("Design Thinking for Data-Driven App Development", "ms3001")
MARKET_RESEARCH = _Subject("Market Research", "ms3002")
INDUSTRY_4_0 = _Subject("Industry 4_0", "ms4001")
