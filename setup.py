import os
from setuptools import setup, find_packages

STATUS_PROD = 'Development Status :: 5 - Production/Stable'
STATUS_BETA = 'Development Status :: 4 - Beta'
STATUS_ALPHA = 'Development Status :: 3 - Alpha'

version = '0.2.1'
README = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(README).read()
setup(
    name='django-simple-audit',
    version=version,
    description="Simple audit for model instances in Django.",
    long_description=long_description,
    classifiers=[
        STATUS_PROD,
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'],
    keywords='revisions versioning history audit',
    author='Leandro Souza',
    author_email='lsouzarj@gmail.com',
    url='https://github.com/leandrosouza/django-simple-audit',
    license='BSD',
    packages=find_packages('.', exclude=('testproject*',)),
    include_package_data=True,
)
