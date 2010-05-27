import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "jsoninspector",
    version = "1.2",
    packages = find_packages(),
    scripts = ['jsoninspector.py'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.glade'],
    },

    # metadata for upload to PyPI
    author = "Jose Carlos Cuevas",
    author_email = "reset.reboot@gmail.com",
    description = "JSON Inspector is a simple application to study JSON code",
    license = "GPLv3",
    keywords = "json inspect gtk gnome",
    url = "",   # project home page, if any
)
