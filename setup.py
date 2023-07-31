from setuptools import setup

setup(
    name='YahooRequests',
    packages=['YahooRequests'],
    version='0.1.5.5',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description='A simple Python library for getting stock prices and company names from Yahoo Finance.',
    author='Theodor Gajhede',
    author_email='theodorgajhede@gmail.com',
    url='https://github.com/TheodorGajhede/YahooRequests',
    download_url='https://github.com/TheodorGajhede/YahooRequests/archive/refs/tags/FIXED.tar.gz',
    keywords=['Stocks', 'Ticker', 'Yahoo'],
    install_requires=[
          'requests'
          ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'yahoorequests=YahooRequests.yahoorequests:main',
        ],
    },
)
