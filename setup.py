from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()


setup(
    name="cart_service",
    version="0.1",
    packages=find_packages(),
    install_requires=read_requirements(),
    description="Cart Service example",
    author="Hernán Bernal",
    author_email="bernalhd18@gmail.com",
    url="https://github.com/bernalhd/cart_service",
    license="MIT",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "cart_service=cart_service.app.infrastructure.grpc.server:serve",
        ],
    },
)
