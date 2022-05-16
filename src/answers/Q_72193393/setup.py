import pathlib
from setuptools import setup, find_packages

README_FILENAME: str = "Q_72193393.md"
REQUIREMENTS_FILE_NAME: str = "requirements.txt"
README: str = pathlib.Path(README_FILENAME).read_text()
REQUIREMENTS = pathlib.Path(REQUIREMENTS_FILE_NAME).read_text()

base_packages = []
if REQUIREMENTS:
    base_packages += REQUIREMENTS.splitlines()

docs_packages = [
    "mkdocs>=1.2.3",
    "mkdocs-material==8.1.3",
    "mkdocstrings>=0.17.0",
    "mktestdocs==0.1.2",
    "pygments>=2.10",
    "pymdown-extensions>=9.0",
]

test_packages = [
    "interrogate>=1.5.0",
    "flake8>=4.0.1",
    "pytest>=6.2.5",
    "black>=21.12b0",
    "isort>=5.10.1",
    "pre-commit>=2.16.0",
    "pre-commit-hooks>=4.0.0" "flake8-print>=4.0.0",
    "flake8-black>=0.2.3",
]

build_packages = [
    "twine",
    "setuptools",
    "build",
    "pkginfo>=1.8.2",
]

all_packages = base_packages
dev_packages = all_packages + docs_packages + test_packages + build_packages


setup(
    name="solution-SOQ-72193393",
    version="0.0.1",
    author="Sugato Ray",
    author_email="sugatoray.dev@gmail.com",
    python_requires=">=3.7",
    keywords="",
    packages=find_packages(
        include=["solution", README_FILENAME, REQUIREMENTS_FILE_NAME], 
        exclude=["notebooks", "docs", "test*"]
    ),
    description="A library with the solution to Stackoverflow question #72193393.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sugatoray/stackoverflow/src/answers/Q_72193393/",
    project_urls={
        "Documentation": "https://sugatoray.github.io/stackoverflow/",
        "Source Code": "https://github.com/sugatoray/stackoverflow/src/answers/Q_72193393/",
        "Issue Tracker": "https://github.com/sugatoray/stackoverflow/issues",
    },
    install_requires=base_packages,
    extras_require={"dev": dev_packages},
    tests_require=test_packages,
    test_suite="tests",
    license_files=("LICENSE",),
    classifiers=[
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
    ],
)
