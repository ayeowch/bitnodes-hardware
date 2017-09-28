#
# Copyright (c) Addy Yeow Chin Heng <ayeowch@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from setuptools import setup, find_packages


setup(
    name='bitnodes-hardware',
    version='0.1.0',
    url='https://github.com/ayeowch/bitnodes-hardware',
    author='Addy Yeow Chin Heng',
    author_email='ayeowch@gmail.com',
    description=('Django project for Bitnodes Hardware, a low footprint '
                 'quad-core single-board computer built and configured to '
                 'operate as a dedicated Bitcoin full node.'),
    long_description='See https://github.com/ayeowch/bitnodes-hardware/blob/master/README.md',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Celery',
        'Django',
        'django-debug-toolbar',
        'django-supervisor',
        'djangorestframework',
        'gunicorn',
        'psycopg2',
        'redis',
        'requests',
        'tornado',
    ],
    keywords=[
        'bitcoin network',
        'full node',
        'bitnodes hardware',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Hardware',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
)
