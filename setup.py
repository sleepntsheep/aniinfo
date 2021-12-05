from setuptools import setup

def read_requirements():
    requirements = """
    requests>=2.26.0
    rich>=10.6.0
    urllib3>=1.26.6
    """
    return requirements.splitlines()

setup(
        name='aniinfo',
        version='0.4.6',
        packages=['aniinfo', 'aniinfo/data'],
        data_files=[('config', ['aniinfo/data/config.json'])],
        include_package_data=True,
        install_requires=read_requirements(),
        entry_points='''
        [console_scripts]
        aniinfo=aniinfo.main:help
    '''
)
