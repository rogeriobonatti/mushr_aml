import os

from azureml.core import (
    Environment, Experiment, ScriptRunConfig, Workspace,
)

import compute_manager

ws = Workspace("964a24a8-8835-43c1-9633-7d78841facf1", "robothackathon", "robothackathon")
root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)

env = None
with open("Dockerfile", "r") as f:
    dockerfile=f.read()

env = Environment(name='mushr-env')
env.docker.base_image = None
env.docker.base_dockerfile = dockerfile
env.docker.enabled = True
env.python.user_managed_dependencies = True
env.python.interpreter_path = "xvfb-run -s '-screen 0 640x480x16 -ac +extension GLX +render' python"
env.register(ws)

installation_cmds = ("vcs import < repos.yaml && \
                      mv mushr/mushr_hardware/realsense/realsense2_description mushr/mushr_hardware/realsense2_description && \
                      rm -rf mushr/mushr_hardware/realsense && \
                      cd ./range_libc/pywrapper && \
                      python setup.py install && \
                      cd ../../ && \
                      rm -rf range_libc && \
                      cd .. && \
                      ./opt/ros/melodic/setup.bash && \
                      catkin_make && \
                      echo 'source /ros_entrypoint.sh' >> /root/.bashrc && \
                      echo 'source /project/catkin_ws/devel/setup.bash' >> /root/.bashrc && ")

script_run_config = ScriptRunConfig(
    source_directory=os.path.join(root_dir), 
    command=[installation_cmds + 'roslaunch mushr_sim server_collection.launch'],
    compute_target=compute_manager.create_compute_target(ws, 'd12v2'),
    environment=env)

exp = Experiment(workspace=ws, name='mushr-datacollection')
exp.submit(config=script_run_config)
