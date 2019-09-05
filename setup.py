from setuptools import setup

with open('requirements.txt') as f:
    require = f.readlines()
install_requires = [r.strip() for r in require]

setup(
    name='hydrocomp',
    version='0.1.1',
    url='https://github.com/clebsonpy/HydroComp',
    license='MIT License',
    author='Clebson Farias',
    author_email='clebson2007.farias@gmail.com',
    keywords='hydrology statistic iha flow',
    description=u'Desenvolvido para estudos hidrológicos',
    packages=['comparasion', 'files', 'graphics', 'iha', 'series', 'statistic'],
    install_requires=install_requires,
)