import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sql_tools",
    version="0.0.2",
    author="Félix Motot",
    author_email="felix@motot.fr",
    description="Data processing toolkit for Keolis Ile-de-France",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    # package_data={"static": ["theapp/static/swagger.json"]},
    # data_files=[("static", ["kidfapp/static/swagger.json"])],
    install_requires=[
        # production deployment
        # "wheel",
        # "waitress",
        # "flask",
        # "flask-swagger-ui",
        # "requests",
        # "psycopg2-binary",
        # "psycopg2",
        # "pytz",
        # "python-dotenv",
        # "pyproj",
        # "unidecode",
        # ### timetables
        # "pandas==1.4.1",
        # "numpy==1.22.1",
        # "openpyxl==3.0.9",
        # "sqlalchemy",
        # # "gdal",
        # # "geopandas",
        # # linter
        # "pylint",
        # "pylint-flask",
        # "pylint-flask-sqlalchemy",
        # # testing
        # "pytest",
        # "pytest-cov",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
