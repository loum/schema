import os
import glob
import fnmatch
import shutil
from distutils.core import setup

VERSION = '0.01'


def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)


def find_data_files(srcdir, *wildcards, **kw):
    """Get a list of all files under the *srcdir* matching *wildcards*,
    returned in a format to be used for install_data.

    """

    def walk_helper(arg, dirname, files):
        names = []
        lst, wildcards = arg
        for wc in wildcards:
            wc_name = opj(dirname, wc)
            for f in files:
                filename = opj(dirname, f)

                if (fnmatch.fnmatch(filename, wc_name) and
                    not os.path.isdir(filename)):
                    if kw.get('version') is None:
                        names.append(filename)
                    else:
                        versioned_file = '%s.%s' % (filename,
                                                    kw.get('version'))
                        shutil.copyfile(filename, versioned_file)
                        names.append('%s.%s' % (filename,
                                                kw.get('version')))

        if names:
            if kw.get('target_dir') is None:
                lst.append(('', names))
            else:
                lst.append((kw.get('target_dir'), names))

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.path.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards),
                    srcdir,
                    [os.path.basename(f) for f in glob.glob(opj(srcdir, '*'))])
    return file_list

files = find_data_files('doc/build/',
                        '*.html',
                        '*.png',
                        '*.js',
                        '*.css',
                        recursive=True,
                        target_dir='doc/build')

url = ('%s://%s:%s/%s' % ('http',
                          'ip-172-31-2-156.ap-southeast-2.compute.internal',
                          '8090',
                          'display/JDT/Geospatial+DISH+Team'))
setup(name='python-oct-schema',
      version=VERSION,
      description='OCT Schema',
      author='Lou Markovski',
      author_email='lou.markovski@gmail.com',
      url=url,
      packages=['oct_schema',
                'oct_schema.models'],
      package_dir={'oct_schema': 'oct_schema'},
      data_files=files)
