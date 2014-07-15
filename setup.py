import ez_setup, sys, shutils
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "jsoninspector",
    version = "2.0",
    packages = find_packages('src', exclude=['distribute_setup']),
    scripts = ['jsoninspector.py'],
    include_package_data = True,
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
    url = "https://github.com/resetreboot/jsoninspector",   # project home page, if any
)

# if sys.path != 'win32' and sys.path != 'darwin':
#     shutils.copytree('locale/po/', '/usr/share/locale/')
