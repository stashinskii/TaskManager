from setuptools import setup

setup(
    name='tman',
    version='0.5',
    py_modules=['UserLib','DataLib','TaskLib', 'TaskCLI', 'ConsoleLib', 'Synchronizer'],
    install_requires=[
        'Click'],
    entry_points='''
    [console_scripts]
    tman=TaskCLI:cli''')
