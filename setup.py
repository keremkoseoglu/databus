import setuptools

setuptools.setup(
    name="databus-keremkoseoglu",
    version="0.1.3",
    author="Kerem Koseoglu",
    author_email="kerem@keremkoseoglu.com",
    description="A framework to transfer data between systems",
    long_description="A framework to transfer data between systems",
    long_description_content_type="text/markdown",
    url="https://github.com/keremkoseoglu/databus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)