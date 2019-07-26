
from setuptools import setup

setup(
    name='topostl',
    version='0.0.1',
    packages=['topostl'],
    python_requires='>=3.6,<4.0',
    install_requires=['numpy>=1.16,<2', 'pyproj>=2.2,<3', 'scipy>=1.3,<2'],
    entry_points={
        'console_scripts': [
            'topostl=topostl.main:main',
        ],
    }
)
