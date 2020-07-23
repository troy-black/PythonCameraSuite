import setuptools

with open('README.md', 'r') as file:
    readme = file.read()

with open('requirements.txt', 'r') as file:
    requirements = file.read().splitlines()

setuptools.setup(
    name='troydblack-PythonCameraSuite',
    description='A Python Camera Software Suite',

    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/troy-black/PythonCameraSuite',

    author='Troy D Black',
    author_email='troydblack@gmail.com',

    version='0.0.1',

    packages=setuptools.find_packages(),

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    python_requires='>=3.6',

    install_requires=requirements,

)
