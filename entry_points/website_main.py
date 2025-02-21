import argparse
import logging
import os

import flask

from bhamon_orchestra_model.date_time_provider import DateTimeProvider
from bhamon_orchestra_model.serialization.json_serializer import JsonSerializer
from bhamon_orchestra_model.users.authorization_provider import AuthorizationProvider

import bhamon_orchestra_website
import bhamon_orchestra_website.website_setup as website_setup
from bhamon_orchestra_website.admin_controller import AdminController
from bhamon_orchestra_website.job_controller import JobController
from bhamon_orchestra_website.me_controller import MeController
from bhamon_orchestra_website.project_controller import ProjectController
from bhamon_orchestra_website.run_controller import RunController
from bhamon_orchestra_website.schedule_controller import ScheduleController
from bhamon_orchestra_website.service_client import ServiceClient
from bhamon_orchestra_website.user_controller import UserController
from bhamon_orchestra_website.website import Website
from bhamon_orchestra_website.worker_controller import WorkerController

import bhamon_orchestra_configuration
import bhamon_orchestra_configuration.website_extensions as website_extensions

import environment


logger = logging.getLogger("Main")


def main():
	arguments = parse_arguments()
	environment_instance = environment.load_environment()
	environment.configure_logging(environment_instance, arguments)

	application_title = bhamon_orchestra_website.__product__ + " " + "Website"
	application_version = bhamon_orchestra_website.__version__

	serializer_instance = JsonSerializer()
	configuration = serializer_instance.deserialize_from_file(arguments.configuration)

	environment.configure_log_file(environment_instance, configuration["orchestra_website_log_file_path"])

	development_options = {
		"debug": True,
		"address": configuration["orchestra_website_listen_address"],
		"port": configuration["orchestra_website_listen_port"],
	}

	logging.getLogger("Application").info("%s %s", application_title, application_version)

	application = create_application(configuration)
	application._application.config["WEBSITE_ANNOUNCEMENT"] = "Development Environment"
	application._application.config["WEBSITE_ANNOUNCEMENT_TYPE"] = "warning"
	application.run(**development_options)


def parse_arguments():
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument("--configuration", default = "orchestra.json", metavar = "<path>", help = "set the configuration file path")
	return argument_parser.parse_args()


def create_application(configuration):
	resource_paths = [
		os.path.dirname(bhamon_orchestra_configuration.__file__),
		os.path.dirname(bhamon_orchestra_website.__file__),
	]

	application = website_setup.create_application(
		flask_import_name = __name__,
		flask_secret_key = configuration["orchestra_website_secret"],
		orchestra_service_url = configuration["orchestra_service_url"],
		resource_paths = resource_paths)

	application._application.artifact_server_url = configuration["artifact_server_web_url"]
	application._application.python_package_repository_url = configuration["python_package_repository_web_url"]

	website_extensions.register_routes(application._application) # FIXME
	
	return application


if __name__ == "__main__":
	main()
