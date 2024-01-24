from setuptools import setup
import io


setup(name='variantbrowser',
      description='Variant Browser: A tool for interpretation of variants from Genexus.',
      long_description=io.open('README.md', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      version='0.0.1',
      author='Sigve Landa',
      author_email='',
      license='MIT',
      url='',
      packages=['variantbrowser', 'variantbrowser.db', 'variantbrowser.backend'],
      install_requires=['Flask>=3.0.1',
                        'Flask-Cors>=4.0.0',
                        'Flask-SQLAlchemy>=3.1.1',
                        'flask-jwt-extended>=4.4.4',
                        'SQLAlchemy>=2.0.25',
                        'MarkupSafe>=2.1.4',
                       ' Werkzeug>=3.0.1',
                        'numpy>=1.26.3',
                        'pandas>=2.2.0',
                        'uuid>=1.30',
                        'maskpass>=0.3.7',
                        'waitress>=2.1.2'],

      entry_points={'console_scripts': ['variantbrowser = variantbrowser.__main__:main',
                                        'variantbrowser-adduser = variantbrowser.db:add_user',
                                        'variantbrowser changepwd = variantbrowser.db:change_pwd',
                                        'variantbrowser generatedbs = variantbrowser.db:generate_dbs',
                                        'variantbrowser removesample = variantbrowser.db:remove_sample',
                                        'variantbrowser unlocksample = variantbrowser.db:unapprove_sample']},
      test_suite=None)
