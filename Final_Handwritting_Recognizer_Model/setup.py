from setuptools import setup, find_packages

setup(
    name="handwriting_recognizer",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={"handwriting_recognizer": ["*.json", "*.pth"]},
    install_requires=[
        "fastapi",
        "uvicorn",
        "torch",
        "opencv-python",
        "numpy",
    ],
)
