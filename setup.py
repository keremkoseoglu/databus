import setuptools
import databus

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
)