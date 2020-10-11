Thank you for your desire to contribute to Glotter!

If you haven't already, please first take a look through our [wiki].
Specifically, make sure you have a grasp on [general usage][wiki-general-usage] of glotter and [how glotter integrates with clients][wiki-integration].

Once you are familiar with the basics, see the sections below for how to contribute.

## Creating Issues

Before creating an issue, please use the search function to see if a related Bug or Feature Request exists.

If you are unable to find a relevant issue, please create a new one using either the Bug Request template or the Feature Request template as applicable


## Glotter Development Environment

### Dependencies

Before you can build Glotter, there a few things you will need.

- Docker: Glotter makes extensive use of docker. You will need to have docker installed on your machine and configured to use linux containers if you are windows (this is the default as of writing).
- Python and Pip: Glotter is written in Python.

### Structure

The file structure of glotter looks like the following (with omissions)

- glotter
- test
  - integration
  - unit
- requirements.txt
- setup.py

The `glotter` directory contains all source code for the project.

The `test` directory contains all tests for the project. It is split into two types: `unit` and `integration`.
The difference for the sake of this project is that the unit tests are written in such a way to abstract our all external dependencies (docker, the filesystem, etc...). The integration tests test the integration between the code and external dependencies (docker, the filesystem, etc...).

I will not explain `setup.py` or `requirements.txt` here.
If you are unfamiliar with those, please read official python documentation.
However, I do want to note that `setup.py` requires the same list of dependencies for testing, local development, and packaging.
The reason for that is the nature of this project.
This project uses pytest as its testing library, but it is also a wrapper around pytest.

### Local Development

The last thing to do before starting development is to install the requirements from `setup.py`.
This can be done by calling `pip install -r requirements.txt`.
> Note: I recommend doing so in a virtual environment.


## Running Tests

Tests can be run by passing either the unit or integration directory to pytest, for example `pytest test/integration`.


## Final Requirements for Contributing

- Please write tests for new functionality. No pull requests will be accepted without applicable new or existing unit or integration tests.
- After creating the pull request, ensure that all the test passed on travis. No pull requests will be merged without failing tests.
- If your changes are related to an existing issue, please reference that issue in your pull request.
- If your changes are not related to an existing issue, please either create a new issue and link to it.


[wiki]:https://github.com/auroq/glotter/wiki
[wiki-general-usage]:https://github.com/auroq/glotter/wiki/General-Usage
[wiki-integrating]:https://github.com/auroq/glotter/wiki/Integrating-With-Glotter
