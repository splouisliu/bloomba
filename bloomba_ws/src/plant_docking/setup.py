from setuptools import setup
import os
from glob import glob
package_name = 'plant_docking'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zhanger',
    maintainer_email='andrewzhang1000@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'plant_tf2_broadcaster = plant_docking.plant_docking_talker:main',
                'plant_docking_listener = plant_docking.plant_docking_listen:main',
                'plant_tf2_listener = plant_docking.plant_docking_tf_listen:main',
                'watering_arm = plant_docking.arm:main'
        ],
    },
)
