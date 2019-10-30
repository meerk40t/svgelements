import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="svg.elements",
    version="0.0.1",
    author="Tatarize",
    author_email="tatarize@gmail.com",
    description="Svg Elements Parsing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meerk40t/svg.elements",
    packages=setuptools.find_packages(),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
)