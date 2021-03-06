from setuptools import setup

setup(
    name = 'ldrprocessorserver',
    version = '1.0.0',
    author = "Tyler Danstrom",
    author_email = ["tdanstrom@uchicago.edu"],
    packages = ['ldrprocessorserver'],
    description = "An application providing access to the contents of the ldr via restful requests",
    keywords = ["uchicago","repository","content retrieval"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ]
    )
