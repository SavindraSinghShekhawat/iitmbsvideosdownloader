from setuptools import find_packages, setup
setup(
    name='iitmbsvideosdownloader',
    packages=find_packages(include=['iitmbsvideosdownloader']),
    version='3.7.4',
    description='Python Bot Library to download IITM BS videos.',
    author='Savi',
    license='MIT',
    install_requires=['selenium==4.10.0', 'chromedriver-autoinstaller-fix==1.0.2', 'requests==2.31.0'],
    setup_requires=['pytest-runner', 'wheel'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)