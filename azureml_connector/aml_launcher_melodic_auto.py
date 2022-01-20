import os
import time

from azureml.core import (
    Environment, Experiment, ScriptRunConfig, Workspace, Datastore, Dataset
)

from azureml.data import OutputFileDatasetConfig

import compute_manager

ws = Workspace.from_config()
root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

env = None
with open("ros_melodic.Dockerfile", "r") as f:
    dockerfile=f.read()

env = Environment(name='ros-melodic-env')
env.docker.base_image = None
env.docker.base_dockerfile = dockerfile
env.docker.enabled = True
env.python.user_managed_dependencies = True
env.python.interpreter_path = "xvfb-run -s '-screen 0 640x480x16 -ac +extension GLX +render' python"
env.register(ws)

installation_cmds = ("mkdir -p catkin_ws/src && " +                    
                     "mv mushr/* catkin_ws/src/ && cd catkin_ws/src/ && " +
                     "vcs import < repos.yaml && " +
                     "git clone -b melodic-devel https://github.com/ros/robot_state_publisher.git && " +
                     "git clone -b melodic-devel https://github.com/rogeriobonatti/geometry.git && " +
                     "git clone -b melodic-devel https://github.com/ros/geometry2 && " +
                     "git clone -b melodic-devel https://github.com/rogeriobonatti/ros_comm.git && " +
                     "mv mushr/mushr_hardware/realsense/realsense2_description mushr/mushr_hardware/realsense2_description && " +
                     "rm -rf mushr/mushr_hardware/realsense && " +
                     "cd ./range_libc/pywrapper && " +
                     "python setup.py install && " +
                     "cd ../../ && " +
                     "rm -rf range_libc && " +
                     "wget https://github.com/wjwwood/serial-release/archive/release/melodic/serial/1.2.1.tar.gz && tar -xvf *.gz && rm *.gz &&" +
                     "cd .. && " +
                     "/bin/bash -c '. /opt/ros/melodic/setup.bash; catkin_make --cmake-args -DCMAKE_BUILD_TYPE=Debug -DPYTHON_EXECUTABLE=/opt/miniconda/bin/python -DPYTHON_INCLUDE_DIR=/opt/miniconda/include/python3.7m -DPYTHON_LIBRARY=/opt/miniconda/lib/libpython3.7m.so' && " +
                     "/bin/bash -c '. /opt/ros/melodic/setup.bash; . ./devel/setup.bash; ' && ")  

datastore = ws.get_default_datastore()
output = OutputFileDatasetConfig(destination=(datastore, 'hackathon_data_slow'))

script_run_config = ScriptRunConfig(
    source_directory=os.path.join(root_dir), 
    command=[installation_cmds + "python ./src/main.py", "--data_path", output.as_mount(), "--ros_dist", "melodic"],
    compute_target=compute_manager.create_compute_target(ws, 'd12v2'),
    # compute_target=compute_manager.create_compute_target(ws, 'f8'),
    environment=env)

exp = Experiment(workspace=ws, name='mushr-datacollection_0')

for i in range(3):
    exp.submit(config=script_run_config, tags={'ros': 'melodic'})
    time.sleep(1)
