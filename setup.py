from setuptools import find_packages, setup

setup(
    name='django_e2e_runner',
    packages=find_packages(),
    version='0.1.0',
    license='Proprietary',  # TODO
    description='Integrate any e2e test framework with Django, easily.',
    author='Olaf Lobozewicz',
    author_email='o.lobozewicz@lekseek.com',
    url='https://github.com/olafik/django-e2e-runner',
    download_url='https://github.com/olafik/django-e2e-runner/archive/v_010.tar.gz',
    keywords=['DJANGO', 'E2E', 'CYPRESS', 'TESTCAFE', 'TEST'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: Other/Proprietary License',  # TODO
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
