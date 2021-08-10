import os
from setuptools import setup


def install_deps():
    default = open('requirements.txt', 'r').readlines()
    new_pkgs = []
    for resource in default:
        if 'git+ssh' in resource or 'git+https' in resource:
            pass
        else:
            new_pkgs.append(resource.strip())
    return new_pkgs


pkgs = install_deps()

setup(
    name='FootballManagerBot',
    version='0.1',
    description='Bot for coursework',
    url='https://github.com/MrFlava/footballamangerbot',
    author='MrFlava',
    author_email='thatelitemaili33t@gmail.com',
    license='GNU',
    packages=["src"],
    install_requires=pkgs,
    python_requires='>3.6.0',
)

if not os.path.exists('logs'):
    os.mkdir('logs')
