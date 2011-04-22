from setuptools import setup, find_packages
 
setup(
    name='django-stats',
    version='0.1',
    description='An app for keeping stats about anything within your django project',
    author='Chris Drackett',
    author_email='chris@shelfworthy.com',
    url = "https://github.com/shelfworthy/django-stats",
    packages=find_packages(),
    install_requires = [
        'django-celery>=2.0.2',
        'celery>=2.1.1'
    ],
    classifiers = [
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)