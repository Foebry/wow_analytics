from setuptools import setup
setup(
    name = 'Wow_Analytics',
    version = 1.1,
    packages = ['Wow_Analytics'],
    install_requires = [
        'Databases @ git+https://github.com/Foebry/Databases.git#egg=Databases',
        'Logger @ git+https://github.com/Foebry/Databases.git#egg=Logger',
        'requires',
        'mysql-connector'
    ],
    url = 'https://github.com/Foebry/Wow_Analytics',
    author = 'Foebry',
    author_email = 'rain_fabry@hotmail.com',
    description = ''
)
