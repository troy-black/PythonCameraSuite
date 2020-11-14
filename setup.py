import platform
import setuptools


with open('README.md', 'r') as file:
    long_description = file.read()

with open('install_requires.txt', 'r') as file:
    install_requires = file.read().splitlines()

if platform.machine() == "armv7l" and platform.system() == "Linux":
    install_requires.append('picamera @ git+https://github.com/troy-black/picamera.git')
    install_requires.append('numpy')

extras_require = {
    'picamera': ['picamera @ git+https://github.com/troy-black/picamera.git', 'numpy'],
    'test': ['coverage']
}

extras_require['all'] = [
    pip
    for pips in extras_require.values()
    for pip in pips
]

setuptools.setup(
    name='troydblack-PythonCameraSuite',
    description='A Python Camera Software Suite',

    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/troy-black/PythonCameraSuite',

    author='Troy D Black',
    author_email='troydblack@gmail.com',

    version='0.1.0',

    packages=setuptools.find_packages(),

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    python_requires='>=3.7,<4',

    install_requires=install_requires,

    extras_require=extras_require,
)
