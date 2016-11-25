from setuptools import setup

setup(
    name='The Deployer',
    version='0.1',
    py_modules=['thedeployer'],
    include_package_data=True,
    install_requires=[
        'click',
        'fabric'
    ],
    entry_points='''
        [console_scripts]
        thedeployer=thedeployer:cli
    ''',
)
