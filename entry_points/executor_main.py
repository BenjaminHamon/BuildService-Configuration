import argparse
import logging
import os
import sys

import filelock

import bhamon_orchestra_worker.executor as executor

import environment


def main():
	arguments = parse_arguments()
	environment.configure_logging(logging.INFO)

	environment_instance = environment.load_environment()
	environment_instance["orchestra_worker_configuration"] = os.path.join(os.getcwd(), "worker.json").replace("\\", "/")
	environment_instance["orchestra_worker_python_executable"] = sys.executable.replace("\\", "/")

	executor_run_directory = os.path.join("runs", arguments.job_identifier + "_" + arguments.run_identifier)

	with filelock.FileLock(os.path.join(executor_run_directory, "executor.lock"), 5):
		executor.run(arguments.job_identifier, arguments.run_identifier, environment_instance)


def parse_arguments():
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument("job_identifier", help = "set the job identifier")
	argument_parser.add_argument("run_identifier", help = "set the run identifier")
	return argument_parser.parse_args()


if __name__ == "__main__":
	main()
