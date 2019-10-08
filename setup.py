from setuptools import setup, find_packages

setup(
    name='glotter',
    version='${VERSION}',
    entry_points={'console_scripts': ['glotter = glotter.__main__:main']},
    packages=find_packages(exclude=('test',)),
    install_requires=[
        'docker>=4.1.0, <4.2',
        'Jinja2>=2.10.1, <2.11',
        'pytest>=5.2.1, <5.3',
        'PyYAML>=5.1, <5.2'
    ],
    python_requires='>=3.5',
)
