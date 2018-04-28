from setuptools import setup, find_packages

setup(
    name='tman',
    version='0.4',
    py_modules=['DataLib','TaskLib','UserLib', 'TaskCLI'],
    install_requires=[
        'Click'],
    entry_points='''
    [console_scripts]
    tman=TaskCLI:cli''')
