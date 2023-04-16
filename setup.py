from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='0.1.1',
    description='scripts clean folder and normalize file name',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
      ],
    author='woody',
    author_email='woody0740@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=[],
    python_requires='>=3.5',
    include_package_data=True,
    entry_points = {'console_scripts': ['clean_folder = clean_folder:clean.py']}
)