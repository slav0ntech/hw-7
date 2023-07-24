from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1.0',
    description='Clean Folder',
    url='https://github.com/slav0ntech/hw-7/tree/main/clean_folder',
    author='Viacheslav Trepov',
    author_email='slava.trepov@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean_folder=clean_folder.clean:start_script']}
)