from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Félix Motot python dependencies to deal with data'
LONG_DESCRIPTION = 'Félix Motot python dependencies to deal with data'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="tools", 
        version=VERSION,
        author="Félix Motot",
        author_email="<felix@motot.fr>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            "os",
            "dotenv",
            "pandas",
            # "shapely",
            # "psycopg2",
            # "geopandas",
            # "sqlalchemy",
        ], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)