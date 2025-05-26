import os
import importlib
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

def init_plugin(app):
    """
    Adds a health check endpoint ("/") with detailed, user-readable output about
    the application's state, database, plugins, environment, and core files.
    """

    try:
        from lib.database import get_db
    except ImportError:
        def get_db():
            yield None

    def get_available_plugins():
        plugins_dir = os.path.join(os.path.dirname(__file__), "..")
        plugins = []
        for entry in os.listdir(plugins_dir):
            plugin_path = os.path.join(plugins_dir, entry)
            if (
                os.path.isdir(plugin_path)
                and os.path.isfile(os.path.join(plugin_path, "__main__.py"))
            ):
                plugins.append(entry)
        return plugins

    def check_env_vars(required_vars=None):
        if required_vars is None:
            required_vars = [
                "DATABASE_URL",  # Example - add more as needed
            ]
        missing = [v for v in required_vars if not os.environ.get(v)]
        details = {}
        for v in required_vars:
            value = os.environ.get(v)
            details[v] = value if value else "NOT SET"
        return {
            "summary": 
                "All required environment variables are set."
                if not missing else
                f"Missing environment variables: {', '.join(missing)}",
            "status": "ok" if not missing else "missing",
            "details": details,
        }

    def check_imports(module_names):
        status = {}
        summary = []
        for name in module_names:
            try:
                importlib.import_module(name)
                status[name] = "ok"
                summary.append(f"Module '{name}' imported successfully.")
            except Exception as e:
                status[name] = f"error: {str(e)}"
                summary.append(f"Module '{name}' import failed: {str(e)}")
        return {
            "summary": "\n".join(summary),
            "status": "ok" if all(v == "ok" for v in status.values()) else "error",
            "details": status,
        }

    def check_database(db):
        try:
            if db is not None:
                db.execute(text("SELECT 1"))
                return {
                    "summary": "Database connection successful.",
                    "status": "ok"
                }
            else:
                return {
                    "summary": "No database session available.",
                    "status": "no-db"
                }
        except Exception as e:
            return {
                "summary": f"Database connection failed: {str(e)}",
                "status": "error",
                "detail": str(e)
            }

    def check_models(db, model_classes):
        result = {}
        summary = []
        for model in model_classes:
            table = getattr(model, "__tablename__", None)
            if not table:
                continue
            try:
                db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                result[table] = "ok"
                summary.append(f"Table '{table}' accessible.")
            except Exception as e:
                result[table] = f"error: {str(e)}"
                summary.append(f"Table '{table}' inaccessible: {str(e)}")
        return {
            "summary": "\n".join(summary) if summary else "No model checks performed.",
            "status": "ok" if all(v == "ok" for v in result.values()) else "error",
            "details": result,
        }

    def check_plugins_importable(plugin_names):
        result = {}
        summary = []
        for plugin in plugin_names:
            try:
                importlib.import_module(f"plugins.{plugin}.__main__")
                result[plugin] = "ok"
                summary.append(f"Plugin '{plugin}' imported successfully.")
            except Exception as e:
                result[plugin] = f"error: {str(e)}"
                summary.append(f"Plugin '{plugin}' import failed: {str(e)}")
        return {
            "summary": "\n".join(summary) if summary else "No plugins found.",
            "status": "ok" if all(v == "ok" for v in result.values()) else "error",
            "details": result,
        }

    @app.get("/", tags=["health"])
    async def health_check(db: Session = Depends(get_db)):
        # Plugins
        plugins = get_available_plugins()
        # Env vars
        env_check = check_env_vars(["DATABASE_URL"])
        # Imports
        imports_check = check_imports([
            "lib.models",
            "lib.schemas",
            "lib.crud",
            "lib.database",
            "lib.auth",
        ])
        # Database
        db_check = check_database(db)
        # Models
        try:
            from lib import models
            model_classes = []
            for attr in dir(models):
                obj = getattr(models, attr)
                if hasattr(obj, "__tablename__"):
                    model_classes.append(obj)
            models_check = check_models(db, model_classes)
        except Exception as e:
            models_check = {
                "summary": f"Could not import models: {str(e)}",
                "status": "error",
                "details": {}
            }
        # Plugins import
        plugins_import_check = check_plugins_importable(plugins)
        # Endpoints
        endpoints = [
            {
                "path": route.path,
                "name": route.name,
                "methods": list(route.methods)
            }
            for route in app.routes
        ]
        endpoint_summary = f"{len(endpoints)} endpoints registered."
        # Files
        essential_files = [
            "lib/models.py",
            "lib/schemas.py",
            "lib/crud.py",
            "lib/database.py",
            "lib/auth.py"
        ]
        files_check = {f: os.path.exists(f) for f in essential_files}
        files_summary = []
        for f, exists in files_check.items():
            if exists:
                files_summary.append(f"File '{f}' found.")
            else:
                files_summary.append(f"File '{f}' NOT FOUND.")
        # Python and packages
        import sys
        import pkg_resources
        python_version = sys.version
        required_pkgs = ["fastapi", "sqlalchemy", "psycopg2"]
        pkgs = {}
        pkgs_summary = []
        for pkg in required_pkgs:
            try:
                version = pkg_resources.get_distribution(pkg).version
                pkgs[pkg] = version
                pkgs_summary.append(f"Package '{pkg}' version {version} installed.")
            except Exception as e:
                pkgs[pkg] = f"missing ({str(e)})"
                pkgs_summary.append(f"Package '{pkg}' NOT FOUND: {str(e)}")

        # Compose a verbose, user-friendly summary
        verbose = {
            "Database": db_check["summary"],
            "Models": models_check["summary"],
            "Environment": env_check["summary"],
            "Core modules": imports_check["summary"],
            "Plugins found": f"{', '.join(plugins) if plugins else 'None'}",
            "Plugins import": plugins_import_check["summary"],
            "Essential files": "\n".join(files_summary),
            "Endpoints": endpoint_summary,
            "Python version": python_version,
            "Core packages": "\n".join(pkgs_summary),
        }

        return {
            "overall_status": "ok" if all([
                db_check.get("status") == "ok",
                models_check.get("status") == "ok",
                env_check.get("status") == "ok",
                imports_check.get("status") == "ok",
                plugins_import_check.get("status") == "ok",
                all(files_check.values()),
            ]) else "error",
            "verbose": verbose,
            "checks": {
                "database": db_check,
                "models": models_check,
                "env_vars": env_check,
                "imports": imports_check,
                "plugins_found": plugins,
                "plugins_import": plugins_import_check,
                "essential_files": files_check,
                "endpoints": endpoints,
                "python_version": python_version,
                "core_packages": pkgs,
            }
        }
