import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="github_action_test",
    version="0.0.1",
    author="andysigler",
    author_email="andrewsigler1@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andysigler/github-action-test",
    project_urls={
        "Bug Tracker": "https://github.com/andysigler/github-action-test/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"github_action_test": "github_action_test"},
    packages=["github_action_test"],
    python_requires=">=3.7",
)