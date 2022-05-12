from setuptools import setup

setup(
    name='minipyg',
    version='0.0.3',
    packages=['minipyg'],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'minipyg = minipyg.minipyg:entry',
        ]
    }
)
