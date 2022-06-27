import os
from setuptools import setup, find_packages

version_dict: "dict[str, str]" = {}
version_path = os.path.join(os.path.dirname(__file__), "dep_builder", "_version.py")
with open(version_path, "r", encoding="utf-8") as f:
    exec(f.read(), version_dict)

readme_path = os.path.join(os.path.dirname(__file__), "README.rst")
with open(readme_path, "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="Dependency Builder",
    version=version_dict["__version__"],
    description="Scripts for building nano-qmflows C/C++ dependencies.",
    long_description=f"{readme}\n\n",
    long_description_content_type="text/x-rst",
    author="Bas van Beek",
    author_email="bas.vanbeek@hotmail.com",
    url="https://github.com/nlesc-nano/nano-qmflows-manylinux",
    packages=find_packages(),
    package_data={"dep_builder": ["py.typed"]},
    include_package_data=True,
    license="GNU Lesser General Public License v3 or later",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Build Tools",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "packaging",
    ],
    extras_require={
        "doc": ["sphinx>=4.1", "sphinx_rtd_theme"],
    }
)
