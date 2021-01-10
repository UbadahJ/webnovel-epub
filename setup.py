import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webnovel-epub-ubadahj",
    version="1.0",
    author="Ubadah Jafry",
    author_email="ubadahjafry@gmail.com",
    description="A simple package that downloads book from given webnovel link and save a epub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UbadahJ/webnovel-epub",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)