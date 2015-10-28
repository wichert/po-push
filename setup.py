from setuptools import setup

version = '1.0.0'

install_requires = [
        'click',
        'polib',
        'beautifulsoup4',
        'html5lib',
        ]


setup(name='po-push',
      version=version,
      description='Various PO-related utilities',
      long_description='',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: DFSG approved',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='translation po gettext Babel',
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='https://github.com/wichert/popush',
      license='BSD',
      packages=['popush'],
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      entry_points='''
      [console_scripts]
      po-push = popush.cli:main
      '''
      )
