from setuptools import setup, find_packages


with open('README.rst', 'r') as fp:
    long_description = fp.read()

setup(
    name='mocp-cli',
    version='0.1.17',
    description='CLI tools for finding, organizing, and playing audio files',
    long_description=long_description,
    author='Ken',
    author_email='kenjyco@gmail.com',
    license='MIT',
    url='https://github.com/kenjyco/mocp-cli',
    download_url='https://github.com/kenjyco/mocp-cli/tarball/v0.1.17',
    packages=find_packages(),
    install_requires=[
        'bg-helper',
        'chloop',
        'click>=6.0',
        'fs-helper',
        'input-helper',
        'mocp',
        'parse-helper',
        'yt-helper',
    ],
    include_package_data=True,
    package_dir={'': '.'},
    package_data={
        '' : ['*.ini'],
    },
    entry_points={
        'console_scripts': [
            'mocplayer=mocp_cli.scripts.player:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Intended Audience :: Developers',
    ],
    keywords = ['moc', 'mocp', 'console audio', 'mp3 player']
)
