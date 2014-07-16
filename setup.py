import ez_setup, sys, shutil, os, os.path, subprocess
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
                os.mkdir("/usr/local/share/jsoninspector", 0755)

            except:
                if not os.path.exists("/usr/local/share/jsoninspector"):
                    print "Warning: Couldn't create /usr/local/share/jsoninspector"

            # Copy the translations
            try:
                print "Installing translations..."
                copy_tree('locale/po/', '/usr/share/locale/')

            except:
                print "Warning: error copying translation files."

            # Generate the icons
            try:
                result = subprocess.call(['./res/get_sizes.sh'])

            except:
                result = 1

            if result != 0:
                print "Warning: Error generating icons"
    
            # Copy the icons
            print "Installing application icons..."
            for icon_size in ['{sz}x{sz}'.format(sz = x) for x in ['16', '22','24', '32', '36', '48', '64', '72', '96', '128', '192']]:
                try:
                    shutil.copyfile('res/jsoninspector' + icon_size + ".png", 
                                    '/usr/share/icons/hicolor/' + icon_size + "/apps/jsoninspector.png")

                except:
                    print "Warning: error copying icon {size}.".format(size = icon_size)

            try:
                shutil.copyfile('res/jsoninspector48x48.png', '/usr/share/pixmaps/jsoninspector.png')

            except:
                print "Warning: error copying icon to pixmaps directory."

            try:
                shutil.copyfile('res/jsoninspector.svg' ,'/usr/share/icons/hicolor/scalable/apps/jsoninspector.svg')

            except:
                print "Warning: error copying svg to scalable."

            print "Updating icon cache..."

            try:
                result = subprocess.call(['/usr/bin/gtk-update-icon-cache /usr/share/icons/hicolor/'])

            except:
                result = 1
            
            if result != 0:
                print "Warning: Error updating hicolor icon cache."

            try:
                print "Installing glade file..."
                shutil.copyfile('res/jsoninspector.glade', '/usr/local/share/jsoninspector/jsoninspector.glade')

            except:
                    print "Warning: error copying .glade file."

            try:
                print "Installing desktop entry..."
                shutil.copyfile('res/jsoninspector.desktop', '/usr/share/applications/jsoninspector.desktop')

            except:
                print "Warning: error copying .desktop entry."

setup(
    name = "Jsoninspector",
    version = "2.0",
    packages = find_packages('src', exclude = ['ez_setup']),
    entry_points = { 'gui_scripts' : [ 'jsoninspector = jsoninspector:main_start' ] },
    package_dir = { '' : 'src' },
    # metadata for upload to PyPI
    author = "Jose Carlos Cuevas",
    author_email = "reset.reboot@gmail.com",
    description = "JSON Inspector is a simple application to study JSON code",
    license = "GPLv3",
    keywords = "json inspect gtk gnome",
    url = "https://github.com/resetreboot/jsoninspector",   # project home page, if any
    cmdclass = { 'install' : CustomInstall }
)
