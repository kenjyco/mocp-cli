from setuptools import setup, find_packages


with open('README.rst', 'r') as fp:
    long_description = fp.read()

with open('requirements.txt', 'r') as fp:
    requirements = fp.read().splitlines()

with open('requirements-extras.txt', 'r') as fp:
    requirements_extras = fp.read().splitlines()

setup(
    name='mocp-cli',
    version='0.1.20',
    description='CLI tools for finding, organizing, and playing audio files',
    long_description=long_description,
    author='Ken',
    author_email='kenjyco@gmail.com',
    license='MIT',
    url='https://github.com/kenjyco/mocp-cli',
    download_url='https://github.com/kenjyco/mocp-cli/tarball/v0.1.20',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'extras': requirements_extras,
    },
    include_package_data=True,
    package_dir={'': '.'},
    package_data={
        '': ['*.ini'],
    },
    entry_points={
        'console_scripts': [
            'mocplayer=mocp_cli.scripts.player:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Topic :: Software Development :: Libraries',
    ],
    keywords=['moc', 'mocp', 'cli', 'command-line', 'console audio', 'repl', 'mp3 player', 'kenjyco']
)
