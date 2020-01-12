import importlib

from bhamon_orchestra_model_extensions.project import Project

import bhamon_orchestra_configuration.projects.build_service as project_build_service
import bhamon_orchestra_configuration.projects.build_service_configuration as project_build_service_configuration
import bhamon_orchestra_configuration.projects.development_toolkit as project_development_toolkit
import bhamon_orchestra_configuration.projects.example as project_example
import bhamon_orchestra_configuration.projects.image_manager as project_image_manager
import bhamon_orchestra_configuration.projects.my_website as project_my_website
import bhamon_orchestra_configuration.projects.solitaire as project_solitaire
import bhamon_orchestra_configuration.worker_selector as worker_selector


def reload_modules():
	importlib.reload(project_build_service)
	importlib.reload(project_build_service_configuration)
	importlib.reload(project_development_toolkit)
	importlib.reload(project_example)
	importlib.reload(project_image_manager)
	importlib.reload(project_my_website)
	importlib.reload(project_solitaire)
	importlib.reload(worker_selector)


def configure(environment):
	all_projects = [
		{ "identifier": "build-service", "services": project_build_service.configure_services(environment) },
		{ "identifier": "build-service-configuration", "services": project_build_service_configuration.configure_services(environment) },
		{ "identifier": "development-toolkit", "services": project_development_toolkit.configure_services(environment) },
		{ "identifier": "example", "services": project_example.configure_services(environment) },
		{ "identifier": "image-manager", "services": project_image_manager.configure_services(environment) },
		{ "identifier": "my-website", "services": project_my_website.configure_services(environment) },
		{ "identifier": "solitaire", "services": project_solitaire.configure_services(environment) },
	]

	all_jobs = []
	all_jobs += project_build_service.configure_jobs()
	all_jobs += project_build_service_configuration.configure_jobs()
	all_jobs += project_development_toolkit.configure_jobs()
	all_jobs += project_example.configure_jobs()
	all_jobs += project_image_manager.configure_jobs()
	all_jobs += project_my_website.configure_jobs()
	all_jobs += project_solitaire.configure_jobs()

	return {
		"projects": all_projects,
		"jobs": all_jobs,
	}


def configure_projects(environment):
	return {
		"build-service": Project(project_build_service.configure_services(environment)),
		"build-service-configuration": Project(project_build_service_configuration.configure_services(environment)),
		"development-toolkit": Project(project_development_toolkit.configure_services(environment)),
		"example": Project(project_example.configure_services(environment)),
		"image-manager": Project(project_image_manager.configure_services(environment)),
		"my-website": Project(project_my_website.configure_services(environment)),
		"solitaire": Project(project_solitaire.configure_services(environment)),
	}
