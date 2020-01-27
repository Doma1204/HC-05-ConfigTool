import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HC-05-ConfigTool",
    version="0.0.1",
    author="Joseph Lam",
    author_email="mhlamaf@connect.ust.hk",
    description="A terminal tool for configuring HC-05 with AT mode.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Doma1204/HC-05_Bluetooth_Tool",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires='>=3',
    keywords="bluetooth hc-05",
    install_requires=["pyserial"]
)