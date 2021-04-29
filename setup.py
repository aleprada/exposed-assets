from setuptools import setup

setup(
    name='exposed_assets',
    version='0.1.0',
    packages=['config', 'misp_alerts', 'search_engines'],
    url='',
    license='MIT',
    author='alejandro.prada',
    author_email='alejandro.prada86@gmail.com',
    description='Tool for discovering exposed IT/OT exposed assets on the Internet  using Shodan and ZoomEye API\'s. '
                'The alerts can be sent to MISP for additional analysis.'
)
