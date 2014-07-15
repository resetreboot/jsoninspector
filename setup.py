import ez_setup, sys, shutil, os, os.path
ez_setup.use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.install import install
from distutils.dir_util import copy_tree

class CustomInstall(install):
    """
    We subclass the install command to add some more mojo
    """
    def run(self):
        install.run(self)       # Do the usual setuptools magic
        # Now we do our own magic
        if sys.platform != 'win32' and sys.platform != 'darwin':
            try:
                print "Creating shared directory..."
                os.mkdir("/usr/local/share/jsoninspector", mode = 0755)

            except:
                if not os.path.exists("/usr/local/share/jsoninspector"):
                    print "Warning: Couldn't create /usr/local/share/jsoninspector"

            # Copy the translations
            try:
                print "Installing translations..."
                copy_tree('locale/po/', '/usr/share/locale/')

            except:
                print "Warning: error copying translation files."
    
            # Copy the icons
            print "Installing application icons..."
            for icon_size in ['16x16', '32x32', '48x48', '64x64', '128x128']:
                try:
                    shutil.copyfile('res/jsoninspector' + icon_size + ".png", 
                                    '/usr/share/icons/hicolor/' + icon_size + "/apps/jsoninspector.png")

                except:
                    print "Warning: error copying icon {size}.".format(icon_size)

            try:
                shutil.copyfile('res/jsoninspector48x48.png', '/usr/share/pixmaps/jsoninspector.png')

            except:
                print "Warning: error copying icon to pixmaps directory."

            try:
                print "Installing glade file..."
                shutil.copyfile('res/jsoninspector.glade', '/usr/local/share/jsoninspector/jsoninspector.desktop')

            except:
                    print "Warning: error copying .glade file."

            try:
                print "Installing desktop entry..."
                shutil.copyfile('res/jsoninspector.desktop', '/usr/share/applications/jsoninspector.desktop')

            except:
                print "Warning: error copying .desktop entry."


setup(
    name = "jsoninspector",
    version = "2.0",
    packages = find_packages('src', exclude=['ez_setup']),
    scripts = ['src/jsoninspector.py'],
    include_package_data = True,
    package_data = {
        # If any package contains *.glade files, include them:
        'src': ['*.glade'],
    },

    # metadata for upload to PyPI
    author = "Jose Carlos Cuevas",
    author_email = "reset.reboot@gmail.com",
    description = "JSON Inspector is a simple application to study JSON code",
    license = "GPLv3",
    keywords = "json inspect gtk gnome",
    url = "https://github.com/resetreboot/jsoninspector",   # project home page, if any
    cmdclass = { 'install' : CustomInstall }
)
