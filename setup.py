from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
print(find_packages(where="src"))
setup(
    name="testspace",
    version="0.0.1",
    author="ddmonster.wei",
    author_email="ddmonster.wei@outlook.com",
    description="used for test job",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "toml",
        "environs",
    ],
)