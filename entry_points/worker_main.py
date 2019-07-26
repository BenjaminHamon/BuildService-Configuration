import argparse
import json
import logging
import os

import filelock

import bhamon_build_worker.worker as worker

import environment


def main():
	environment.configure_logging(logging.INFO)
	arguments = parse_arguments()
	executor_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "executor_main.py"))

	with open(arguments.configuration, "r") as configuration_file:
		configuration = json.load(configuration_file)

	worker_path = configuration["build_workers"][arguments.identifier]["path"]
	os.makedirs(worker_path, exist_ok = True)

	with filelock.FileLock(os.path.join(worker_path, "build_worker.lock"), 5):
		configure_worker(configuration, worker_path)
		os.chdir(worker_path)
		worker.run(configuration["build_master_url"], arguments.identifier, executor_script)


def parse_arguments():
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument("--identifier", required = True, help = "set the identifier for this worker")
	argument_parser.add_argument("--configuration", default = "build_service.json", help = "set the configuration file path")
	return argument_parser.parse_args()


def configure_worker(global_configuration, worker_path):
	local_configuration = {
		"build_service_url": global_configuration["build_service_url"],
		"authentication_file_path": os.path.abspath(os.path.join(worker_path, "authentication.json")),
		"artifact_repository_path": os.path.abspath(global_configuration["artifact_repository_path"]),
		"python_package_repository_path": os.path.abspath(global_configuration["python_package_repository_path"]),
	}

	with open(os.path.join(worker_path, "build_worker.json"), "w") as configuration_file:
		json.dump(local_configuration, configuration_file, indent = 4)


if __name__ == "__main__":
	main()
