import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()    

setuptools.setup(
    name="Syslogging",
    version="0.0.1",
    author="Nguyen Dinh Manh",
    author_email="manhnd1112@gmail.com",
    description="A module allow you log information to console, file or mail",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/manhnd1112/-Python-syslogging.git",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)