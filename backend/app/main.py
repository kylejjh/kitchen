from flask import Flask
from flask_restx import Api, Namespace, Resource

def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app, title="Kitchen API", version="0.1")

    health_ns = Namespace("health", description="Health check")

    @health_ns.route("")
    class Health(Resource):
        def get(self):
            return {"status": "ok"}, 200

    api.add_namespace(health_ns, path="/health")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
