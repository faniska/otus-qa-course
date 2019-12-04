from setuptools import setup, find_packages

setup(
    name='otus-qa-course',
    version='0.1',
    url='https://github.com/faniska/otus-qa-course/',
    license='MIT',
    author='XFanis',
    author_email='dev@xfanis.ru',
    description='Otus QA course code',
    packages=find_packages(exclude=['tests']),
    setup_requires=['pytest'],
    zip_safe=False,
)
