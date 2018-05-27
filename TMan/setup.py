from setuptools import setup

setup(
    name='tman',
    version='0.6',
    py_modules=['user_actions','data_storage','task_info', 'task_cli', 'console_lib', 'event_actions'],
    install_requires=[
        'Click'],
    entry_points='''
    [console_scripts]
    tman=task_cli:cli''')
