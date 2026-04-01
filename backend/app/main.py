from flask import Flask, request
from flask_restx import Api, Namespace, Resource

from backend.app.db import ping_mongo
from backend.app.features.recipes.routes import recipes_ns
from backend.app.features.cuisines.routes import cuisines_ns
from backend.app.features.ingredients.routes import ingredients_ns

from flask_cors import CORS


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    api = Api(app, title="Kitchen API", version="0.1")
    
    
    # -----------------------------
    # Demo endpoints (for React HW)
    # -----------------------------

    @app.get("/demo/one")
    def demo_one():
        return {"endpoint": "one", "ok": True}

    @app.get("/demo/two")
    def demo_two():
        return {"endpoint": "two", "ok": True}

    @app.get("/demo/three")
    def demo_three():
        return {"endpoint": "three", "ok": True}

    # -----------------------
    # Health namespace
    # -----------------------
    health_ns = Namespace("health", description="Health check")

    @health_ns.route("")
    class Health(Resource):
        def get(self):
            return {"status": "ok"}, 200

    # -----------------------
    # DB namespace
    # -----------------------
    db_ns = Namespace("db", description="Database check")
    
    @db_ns.route("/health")
    class DbHealth(Resource):
        def get(self):
            ok = ping_mongo()
            return {"mongo": "ok" if ok else "down"}, 200 if ok else 500
            
    # -----------------------
    # Register namespaces
    # -----------------------
    api.add_namespace(db_ns, path="/db")
    api.add_namespace(health_ns, path="/health")
    api.add_namespace(recipes_ns, path="/recipes")
    api.add_namespace(cuisines_ns, path="/cuisines")
    api.add_namespace(ingredients_ns, path="/ingredients")

    # -----------------------
    # HATEOAS form endpoint
    # -----------------------
    @app.get("/form")
    def form_descriptor():
        return {
            "title": "Kitchen Form",
            "fields": [
                {
                    "name": "cuisine",
                    "label": "Choose a cuisine",
                    "type": "select",
                    "options_url": f"{request.host_url.rstrip('/')}/cuisines",
                },
                {
                    "name": "ingredient",
                    "label": "Choose an ingredient",
                    "type": "select",
                    "options_url": f"{request.host_url.rstrip('/')}/ingredients",
                },
            ],
            "_links": {
                "self": {"href": f"{request.host_url.rstrip('/')}/form"},
                "cuisines": {"href": f"{request.host_url.rstrip('/')}/cuisines"},
                "ingredients": {"href": f"{request.host_url.rstrip('/')}/ingredients"},
            },
        }, 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
