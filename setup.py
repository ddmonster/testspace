from setuptools import setup, find_packages
import pathlib
path = pathlib.Path(__file__).parent
with open(path.joinpath("README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
requirements = []
print(path.joinpath("requirements.txt"))
# with open(path.joinpath("requirements.txt")) as f:
#     requirements = f.readlines()
    

print(find_packages(where="src"))
setup(
    name="testspace",
    author="ddmonster.wei",
    author_email="ddmonster.wei@outlook.com",
    description="simple your test work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddmonster/testspace",
    project_urls={
        "Bug Tracker": "https://github.com/ddmonster/testspace/issues",
    },
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
    install_requires = requirements,
)