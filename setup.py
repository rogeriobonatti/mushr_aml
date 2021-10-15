
# setup.py: install script for mushr
'''
to install mushr and its dependencies for development work,
run this cmd from the root directory:
    pip install -e .
'''
import setuptools

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()

setuptools.setup(
    name='mushr_aml',
    version='0.1',
    url = "https://github.com/rbonatti/mushr_aml",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=requirements
)