import os
from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='restservice',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app to conduct Web-based polls.',
    long_description='',
    url='https://www.example.com/',
    author='Your Name',
    author_email='yourname@example.com',
    classifiers=[],
    install_requires=[
        'requests',
    ],
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', 'mock', ],
)
