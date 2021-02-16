# -*- coding: utf-8 -*-
"""Installer for the trackyourcircle.portal package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="trackyourcircle.portal",
    version="1.0a1.dev0",
    description="",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Laurent Lasudry",
    author_email="lasudry@gmail.com",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["trackyourcircle"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires="==3.7",
    install_requires=[
        "setuptools",
        "embeddify",
        "plone.api",
        "plone.app.imagecropping",
        "plone.app.mosaic",
        "plone.app.standardtiles",
        "collective.anysurfer",
        "collective.behavior.banner",
        "collective.cookiecuttr",
        "collective.easyform",
        "collective.geolocationbehavior",
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
