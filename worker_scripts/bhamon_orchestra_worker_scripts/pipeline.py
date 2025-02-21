# import argparse
# import json
# import logging

# from bhamon_orchestra_worker.pipeline import Pipeline
# from bhamon_orchestra_worker.service_client import ServiceClient

# import bhamon_orchestra_worker_scripts.environment as environment

# logger = logging.getLogger("Main")


# def main():
# 	arguments = parse_arguments()
# 	environment_instance = environment.load_environment()
# 	environment.configure_logging(environment_instance, None)

# 	# eval ?
# 	# "elements["editor-for-linux"]["status"] in [ "failed", "succeeded" ]"

# 	# Need explicit job links
# 	# "element": { "after": [ "element": "...", "require_success": True ] }

# 	pipeline_definition = {
# 		"elements": [
# 			{
# 				"identifier": "empty-1",
# 				"project": "example",
# 				"job": "empty",
# 			},
# 			{
# 				"identifier": "empty-2",
# 				"project": "example",
# 				"job": "empty",
# 			},
# 			{
# 				"identifier": "empty-3",
# 				"project": "example",
# 				"job": "empty",
# 			},
# 		]
# 	}

# 	# pipeline_definition = {
# 	# 	"elements": [
# 	# 		{
# 	# 			"identifier": "check",
# 	# 			"job": "check",
# 	# 		},
# 	# 		{
# 	# 			"identifier": "editor-for-linux",
# 	# 			"job": "editor-for-linux",

# 	# 			"after": [
# 	# 				{ "element": "check", "status": [ "succeeded" ] },
# 	# 			],
# 	# 		},
# 	# 		{
# 	# 			"identifier": "editor-for-windows",
# 	# 			"job": "editor-for-windows",

# 	# 			"after": [
# 	# 				{ "element": "check", "status": [ "succeeded" ] },
# 	# 			],
# 	# 		},
# 	# 		{
# 	# 			"identifier": "package-for-linux",
# 	# 			"job": "package-for-linux",

# 	# 			"after": [
# 	# 				{ "element": "editor-for-linux", "status": [ "succeeded" ] },
# 	# 			],
# 	# 		},
# 	# 		{
# 	# 			"identifier": "package-for-windows",
# 	# 			"job": "package-for-windows",

# 	# 			"after": [
# 	# 				{ "element": "editor-for-windows", "status": [ "succeeded" ] },
# 	# 			],
# 	# 		},
# 	# 		{
# 	# 			"identifier": "test-for-linux",
# 	# 			"job": "test-for-linux",

# 	# 			"after": [
# 	# 				{ "element": "package-for-linux", "status": [ "succeeded" ] },
# 	# 			],
# 	# 		},
# 	# 		{
# 	# 			"identifier": "test-for-windows",
# 	# 			"job": "test-for-windows",

# 	# 			"after": [
# 	# 				{ "element": "package-for-windows", "status": [ "succeeded" ] },
# 	# 			],
# 	# 		},
# 	# 		{
# 	# 			"identifier": "upload-on-steam",
# 	# 			"job": "upload-on-steam",

# 	# 			"after": [
# 	# 				{ "element": "test-for-linux", "status": [ "succeeded" ] },
# 	# 				{ "element": "test-for-windows", "status": [ "succeeded" ] },
# 	# 			],
# 	# 		},
# 	# 	],
# 	# }

# 	with open(arguments.configuration, mode = "r", encoding = "utf-8") as configuration_file:
# 		configuration = json.load(configuration_file)
# 	with open(configuration["authentication_file_path"], mode = "r", encoding = "utf-8") as authentication_file:
# 		authentication = json.load(authentication_file)

# 	service_client_instance = ServiceClient(configuration["orchestra_service_url"], (authentication["user"], authentication["secret"]))
# 	pipeline_instance = Pipeline(service_client_instance, pipeline_definition["elements"], arguments.project, arguments.run, arguments.results)

# 	pipeline_instance.initialize()
# 	pipeline_instance.run()


# def parse_arguments():
# 	parser = argparse.ArgumentParser()
# 	parser.add_argument("--configuration", required = True, metavar = "<path>", help = "set the worker configuration file path")
# 	parser.add_argument("--project", required = True, metavar = "<project_identifier>", help = "set the pipeline project identifier")
# 	parser.add_argument("--run", required = True, metavar = "<run_identifier>", help = "set the pipeline run identifier")
# 	parser.add_argument("--results", required = True, metavar = "<path>", help = "set the file path where to store the run results")
# 	return parser.parse_args()


# if __name__ == "__main__":
# 	main()
