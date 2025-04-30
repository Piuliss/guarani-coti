from setuptools import setup, find_packages

with open("VERSION") as f:
    version = f.read().strip()

setup(
    name="guarani-coti",
    version=version,
    description="CLI para cotizaciones del guaraní paraguayo y otras monedas",
    author="Raul B. Netto",
    author_email="raulbeni@email.com",
    url="https://github.com/Piuliss/guarani-coti",
    packages=find_packages(),
    install_requires=[
        "requests",
        "rich",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "guarani-coti=guarani_coti.main:main",
        ],
    },
    python_requires=">=3.7",
)