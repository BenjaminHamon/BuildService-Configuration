import hashlib
import hmac
from typing import Any

import flask


def handle_event(project_identifier: str) -> Any:
	database_client = flask.request.database_client()
	project = flask.current_app.project_provider.get(database_client, project_identifier)

	if project["services"]["revision_control"]["type"] == "github":
		if "X-GitHub-Delivery" not in flask.request.headers:
			flask.abort(400)

		secret = flask.current_app.config["GITHUB_WEBHOOKS_SECRET"]
		signature = flask.request.headers["X-Hub-Signature-256"]
		is_authorized = authorize_for_github(secret, signature, flask.request.data)
		if not is_authorized:
			flask.abort(403)

		process_event(project_identifier, flask.request.headers["X-GitHub-Event"], flask.request.get_json())
		return ""

	flask.abort(400)
	return ""


def authorize_for_github(secret: str, signature: str, payload: bytes) -> bool:
	function, signature_actual = signature.split("=")

	if function == "sha256":
		signature_expected = hmac.new(key = secret.encode("utf-8"), msg = payload, digestmod = hashlib.sha256).hexdigest()
		return hmac.compare_digest(signature_actual, signature_expected)

	raise ValueError("Unsupported signature function '%s'" % function)


def process_event(project_identifier: str, event: str, payload: dict) -> None:
	if project_identifier == "job-orchestra" and event == "push":
		database_client = flask.request.database_client()
		source = { "type": "webhook" }

		if payload["ref"] == "develop":
			flask.current_app.run_provider.create(database_client, project_identifier, "development_pipeline", { "revision": payload["after"] }, source)
		if payload["ref"].startswith("feature/") or payload["ref"].startswith("fix/"):
			flask.current_app.run_provider.create(database_client, project_identifier, "development_pipeline", { "revision": payload["after"] }, source)
