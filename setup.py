from setuptools import setup, find_packages

package_name = 'launch_tf2_ros'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Marcel Zeilinger',
    maintainer_email='marcel.zeilinger@ait.ac.at',
    description='launch extensions to react to tf2 events',
    license='Apache License 2.0',
    tests_require=['pytest'],
)
