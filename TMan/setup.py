from setuptools import setup, find_packages

setup(
    name='tman',
    version='0.5',
    py_modules=['UserLib','DataLib','TaskLib', 'TaskCLI'],
    install_requires=[
        'Click'],
    entry_points='''
    [console_scripts]
    tman=TaskCLI:cli''')
