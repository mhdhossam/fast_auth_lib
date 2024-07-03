from setuptools import setup, find_packages

setup(
    name='fast_auth_lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        'djangorestframework',
        'djangorestframework-simplejwt',
        'redis',
        'django-redis',
        'celery',
        'cryptography',
    ],
    include_package_data=True,
    description='custom authentication library for Django',
    url='https://github.com/mhdhossam/fast_auth_lib',
    author='mhd',
    author_email='mohamedhossamabdelraham@gmail.com',
    license='MIT',
)
