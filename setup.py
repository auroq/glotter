from setuptools import setup, find_packages

setup(
    name='glotter',
    version='0.0.1',
    entry_points={'console_scripts': ['glotter = glotter.__main__:main']},
    packages=find_packages(exclude=('test',)),
    install_requires=[
        'docker>=3.7.0, <3.8',
        'Jinja2>=2.10.1, <2.11',
        'pytest>=4.3.1, <4.4',
        'PyYAML>=5.1, <5.2'
    ],
    python_requires='>=3.5',
)
