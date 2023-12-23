from setuptools import setup, find_packages

setup(name='clean_folder',
      version='0.1',
      entry_points = {'console_scripts':['clean-folder=clean_folder.clean:main',
                                         'generate-files=clean_folder.generator:file_generator']
                      },
      
      description ='Cleaning and sorting script',
      url = 'http://github.com/*',
      author = 'FyntikUA',
      author_email ='gr.fyntik@gmail.com',
      license = 'MIT',
      packages = find_packages(),
      install_requers = ['numpy', 'Pillow'],
      zip_safe = False)