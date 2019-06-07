repository = "https://github.com/BenjaminHamon/MyWebsite"


def configure_services():
	return {
		"revision_control": {
			"service": "github",
			"parameters": {
				"owner": "BenjaminHamon",
				"repository": "MyWebsite",
			},
		}
	}


def configure_jobs():
	return [
		check(),
		distribute(),
	]


def check():
	job = {
		"identifier": "my-website_check",
		"description": "Run checks for the MyWebsite project.",
		"workspace": "my-website",

		"properties": {
			"project": "my-website",
			"operating_system": [ "linux", "windows" ],
			"is_controller": False,
		},

		"parameters": [
			{ "key": "revision", "description": "Revision for the source repository" },
		],
	}

	initialization_script = [ "{environment[python3_executable]}", "-u", "{environment[script_root]}/my_website.py", "--results", "{result_file_path}" ]
	project_script = [ ".venv/scripts/python", "-u", "scripts/main.py", "--verbosity", "debug", "--results", "{result_file_path}" ]

	job["steps"] = [
		{ "name": "initialize", "command": initialization_script + [ "--repository", repository, "--revision", "{parameters[revision]}" ]},
		{ "name": "clean", "command": project_script + [ "clean" ] },
		{ "name": "develop", "command": project_script + [ "develop" ] },
		{ "name": "lint", "command": project_script + [ "lint" ] },
	]

	return job


def distribute():
	job = {
		"identifier": "my-website_distribute",
		"description": "Generate and upload distribution packages for the MyWebsite project.",
		"workspace": "my-website",

		"properties": {
			"project": "my-website",
			"operating_system": [ "linux", "windows" ],
			"is_controller": False,
		},

		"parameters": [
			{ "key": "revision", "description": "Revision for the source repository" },
		],
	}

	initialization_script = [ "{environment[python3_executable]}", "-u", "{environment[script_root]}/my_website.py", "--results", "{result_file_path}" ]
	project_script = [ ".venv/scripts/python", "-u", "scripts/main.py", "--verbosity", "debug", "--results", "{result_file_path}" ]

	job["steps"] = [
		{ "name": "initialize", "command": initialization_script + [ "--repository", repository, "--revision", "{parameters[revision]}" ]},
		{ "name": "clean", "command": project_script + [ "clean" ] },
		{ "name": "develop", "command": project_script + [ "develop" ] },
		{ "name": "lint", "command": project_script + [ "lint" ] },
		{ "name": "package", "command": project_script + [ "distribute", "--command", "package"] },
		{ "name": "upload", "command": project_script + [ "distribute", "--command", "upload"] },
	]

	return job
