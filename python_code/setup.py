from setuptools import setup, find_packages

setup(
    name="python_code",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "pyserial==3.5",
        "GitPython==3.1.27",
        "pyinstaller==4.10"
    ],
)
