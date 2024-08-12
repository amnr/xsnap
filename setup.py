# https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/

from setuptools import find_packages, setup

setup(
    name='xsnap',
    version='1.0.0',
    description='Create screenshot from emulator snapshot file',
    #long_description='',
    #long_description_content_type='text/markdown',
    author='Amun',
    author_email='amun@local.host',
    license='NCSA',
    keywords=[
        'emulation',
        'graphics',
        'screenshot'
    ],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: University of Illinois/NCSA Open Source License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
        'Topic :: Multimedia :: Graphics :: Capture :: Screen Capture',
        'Topic :: System :: Emulators'
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    #packages=find_packages(include=['src', 'src.*']),
    platforms='any',
    entry_points={
        'console_scripts': [
            # 'xsnap = src.xsnap:main'
        ]
    },
)

# vim: set sts=4 et sw=4:
