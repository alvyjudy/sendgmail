from setuptools import find_packages, setup
import os
import re

#########################
NAME = "sendgmail"
PACKAGES = find_packages(where="src")
META_PATH = os.path.join("src", "sendgmail", "__init__.py")
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

###############################################3
HERE = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """Build an absolute path from *parts* and return the content of the 
    resulting file. Assume UTF-8 encoding"""
    with open(os.path.join(HERE, *parts), mode = "rt", encoding = "utf-8") as f:
        return f.read()

META_FILE = read(META_PATH) 

def find_meta(meta): 
    """Extract __*meta*__ from META_FILE""" 
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M 
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("url"),
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        long_description=read("README.rst"),
        long_description_content_type="text/x-rst",
        packages=PACKAGES,
        package_dir={"": "src"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        options={"bdist_wheel": {"universal": "1"}},
        python_requires='>=3.6',
        install_requires=[
            'Click',
            'google-api-python-client',
            'google-auth-httplib2',
            'google-auth-oauthlib'
        ],
        entry_points='''
            [console_scripts]
            sendgmail=sendgmail.sendgmail:sendgmail
        ''',
    )
