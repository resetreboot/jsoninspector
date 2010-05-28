import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "jsoninspector",
    version = "1.3",
    packages = find_packages('src', exclude=['distribute_setup']),
    scripts = ['src/jsoninspector.py'],
    entry_points = {
        'gui_scripts': [
            'jsoninspector = jsoninspector:MainApp.start',
        ]
    },
    package_data = {
        # If any package contains *.glade files, include them:
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
