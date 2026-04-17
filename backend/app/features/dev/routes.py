from flask_restx import Namespace, Resource
import os

dev_ns = Namespace("dev", description="Developer endpoints")

LOG_DIR = "/var/log"  # you can change this if needed


@dev_ns.route("/logs")
class Logs(Resource):
    def get(self):
        try:
            files = os.listdir(LOG_DIR)

            return {
                "log_files": files
            }, 200

        except Exception as e:
            return {
                "error": str(e)
            }, 500
