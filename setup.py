from setuptools import setup, find_packages


setup(
    name='chaineripy',
    version='0.1.0',
    description='IPython integration of Chainer',
    url='https://github.com/grafi-tt/chaineripy',
    author='Shunsuke Shimizu',
    author_email='grafi@grafi.jp',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    install_requires=[
        'chainer>=1.11',
        'ipython>=4',
        'ipywidgets',
        'pandas',
    ])
