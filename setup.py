from setuptools import setup, find_packages
import os

rootpath = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return open(os.path.join(rootpath, *parts), 'r').read()


long_description = '{}'.format(read('README.md'))

with open('requirements.txt') as f:
    require = f.readlines()
install_requires = [r.strip() for r in require]

setup(
    name='hidrocomp',
    version='1.1.9',
    include_package_data=True,
    long_description=long_description,
    classifiers=['Development Status :: 1 - Planning',
                 'Environment :: Console',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Education',
                 ],
    url='https://github.com/clebsonpy/HidroComp',
    license='MIT License',
    author='Clebson Farias',
    author_email='clebson2007.farias@gmail.com',
    keywords='hydrology statistic eflow flow',
    description='Developed for hydrological studies',
    install_requires=install_requires,
    packages=['hidrocomp'],
)
