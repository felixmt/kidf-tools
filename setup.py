"""module imports
"""
from setuptools import setup, find_packages

VERSION = '0.1.9'
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
            "python-dotenv",
            "pandas",
            "shapely",
            "psycopg2",
            "geopandas",
            "sqlalchemy<2",
            "openpyxl",
            "requests",
            "pyyaml"
        ], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'fm tools package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)