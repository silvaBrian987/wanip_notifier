#!/usr/bin/env python3

import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="wanip_notifier",
    version="0.0.1",
    author="Brian Silva",
    author_email="silva.brian.987@gmail.com",
    description="Utilitario que informa sobre cambios de la ip expuesta al internet, generalmente por el ISP",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/silvaBrian987/wanip_notifier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
