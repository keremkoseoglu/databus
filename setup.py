""" Databus setup module """
import os
import setuptools
import databus


def get_databus_requirements() -> []:
    """ Returns a list of requirements """
    output = []
    lib_folder = os.path.dirname(os.path.realpath(__file__))
    requirement_path = lib_folder + '/requirements.txt'

    if os.path.isfile(requirement_path):
        with open(requirement_path) as f:
            output = f.read().splitlines()

    return output


setuptools.setup(
    name="databus-keremkoseoglu",
    version=databus.__version__,
    author=databus.AUTHOR,
    author_email=databus.EMAIL,
    description=databus.DESCRIPTION,
    long_description="A framework to transfer data between systems",
    long_description_content_type="text/markdown",
    url="https://github.com/keremkoseoglu/databus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=databus.PYTHON_VERSION,
    install_requires=[
        "cython",
        "flask",
        "pyodbc",
        "urlextract",
        "vibhaga-keremkoseoglu",
        "waitress"
    ],
    include_package_data=True
)
