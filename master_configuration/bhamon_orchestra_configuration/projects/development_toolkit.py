repository = "https://github.com/BenjaminHamon/DevelopmentToolkit"

initialization_script = "bhamon_orchestra_worker_scripts.development_toolkit"

worker_configuration_path = "{environment[orchestra_worker_configuration]}"
worker_python_executable = "{environment[orchestra_worker_python_executable]}"


def configure_project(environment):
	return {
		"identifier": "development-toolkit",
		"display_name": "Development Toolkit",
		"jobs": [],
		"schedules": [],
		"services": configure_services(environment),
	}


def configure_services(environment):
	return {
		"artifact_repository": {
			"url": environment["artifact_server_url"] + "/" + "DevelopmentToolkit",
		},

		"python_package_repository": {
			"url": environment["python_package_repository_url"],
			"distribution_extension": "-py3-none-any.whl",
		},

		"revision_control": {
			"type": "github",
			"repository": "BenjaminHamon/DevelopmentToolkit",
			"references_for_status": [ "develop" ],
		},

		"job_provider": {
			"implementation": "github",
			"repository": "BenjaminHamon/DevelopmentToolkit",
			"file_path": ".orchestra/jobs.yaml",
			# "url": "https://raw.githubusercontent.com/BenjaminHamon/DevelopmentToolkit/feature/orchestra-configuration/.orchestra/jobs.yaml"
		},

		"status": {
			"interface": "FIXME",
			"type": "FIXME",
			"revision_control_service": "revision_control",
			"references": [ "master", "develop" ],
		},
	}
