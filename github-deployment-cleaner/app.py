from flask import Flask, render_template, jsonify, request
from github_deployments import list_deployments, mark_inactive, delete_deployment
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder="./frontend/build", static_url_path="/")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your_secret_key")


@app.route("/")
def serve():
    return app.send_static_file("index.html")


@app.route("/api/deployments", methods=["GET"])
def api_list_deployments():
    deployments = list_deployments()
    return jsonify(deployments)


@app.route("/api/deployments/<int:deployment_id>/mark_inactive", methods=["POST"])
def api_mark_inactive(deployment_id):
    success = mark_inactive(deployment_id)
    return jsonify({"success": success})


@app.route("/api/deployments/<int:deployment_id>", methods=["DELETE"])
def api_delete_deployment(deployment_id):
    success = delete_deployment(deployment_id)
    return jsonify({"success": success})


if __name__ == "__main__":
    app.run(debug=True)
