from uvicorn.workers import UvicornWorker
import os

class WUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"reload": bool(os.environ.get("RELOAD", False)), "log_level": os.environ.get("LOG_LEVEL", "info")}