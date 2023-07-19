from distutils.core import setup
setup(
    name='YahooRequest',
    packages=['YahooRequests'],
    version='0.1.1',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description='A simple Python library for getting stock prices and company names from Yahoo Finance.',
    author='Theodor Gajhede',
    author_email='theodorgajhede@gmail.com',
    url='https://github.com/TheodorGajhede/YahooRequests',
    download_url='https://github.com/TheodorGajhede/YahooRequests/archive/refs/tags/BETA.tar.gz',
    keywords=['Stocks', 'Ticker', 'Yahoo'],
    install_requires=[
          'requests'
          ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',
            ],
)
