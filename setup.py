from distutils.core import setup

setup(
    name='csc-cascading-config',
    version='0.1',
    packages=['csc'],

    url='https://github.com/ygrosu/csc-cascading-config',
    license='',
    author='ygrosu',
    author_email='yair.grosu@gmail.com',
    description='cascading configuration',
    install_requires=['yaml'],
    requires=["PyYAML (>=3.11)"],
    classifiers=['Development Status :: 2 - Pre-Alpha']
)
