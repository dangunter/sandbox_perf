from setuptools import setup, find_packages
import glob

setup(
    name='sbxperf',
    version='0.0.1',
    packages=find_packages(),
    url='',
    license='MIT',
    author='Dan Gunter',
    author_email='dkgunter@lbl.gov',
    description='Sandbox performance tests',
    scripts=glob.glob('scripts/*.py')
)
