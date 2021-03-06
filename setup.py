from setuptools import setup, find_packages
from codecs import open
from os import path


def readme():
    with open("README.md", "r") as infile:
        return infile.read()


classifiers = [
    # Pick your license as you wish (should match "license" above)
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]
setup(
    name="drf-permission-rules",
    version="0.1.0",
    description="Declarative access policies/permissions modeled after AWS' IAM policies.",
    author="Pavel Maltsev",
    author_email="pavel@speechki.org",
    packages=find_packages(exclude=["tests*"]),
    url="https://github.com/speechki-book/drf-permission-rules",
    license="MIT",
    keywords="django restframework drf access policy authorization declaritive",
    long_description=readme(),
    classifiers=classifiers,
    long_description_content_type="text/markdown",
    install_requires=[  # I get to this in a second
        "django>=2.2.13",
        "djangorestframework>=3.11.0",
        "drf-access-policy>=0.6.1",
        "redis",
        "django-model-utils==4.0.0"
    ],
    include_package_data=True,
)
