import setuptools

setuptools.setup(
    name='simple_ast_drawer',
    version='1.0.2',
    author='Anton Yermilov',
    description='Simple AST visualizer for python.',
    url='https://github.com/AntonYermilov/spring-2022-python',
    packages=['simple_ast_drawer'],
    python_requires='>=3.9',
    install_requires=['networkx==2.6.3', 'pydot==1.4.2'],
)
