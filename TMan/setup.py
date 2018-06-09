from setuptools import setup

setup(
    name='tman',
    version='0.6',
    py_modules=['console', 'task_manager_library'],
    install_requires=[
        'Click'],
    entry_points={
        'console_scripts':
            ['tman = console.task_cli:cli']
    })
