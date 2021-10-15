import argparse
import datetime
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--data_path', type=str, help='Path to the training data')
parser.add_argument('--ros_dist', type=str, help='Ros distribution')
args = parser.parse_args()

output_path = os.path.join(args.data_path, str(datetime.datetime.now().timestamp()))
os.makedirs(output_path, exist_ok=True)
print(output_path)

print(subprocess.check_output("which python", shell=True))

subprocess.call("/bin/bash -c '. /opt/ros/{0}/setup.bash;. ./devel/setup.bash; roslaunch mushr_sim server_collection.launch record_path:={1}'".format(args.ros_dist, output_path), shell=True)
