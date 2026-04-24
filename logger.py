# -*- coding: utf-8 -*-
import os
import logging
from logging.handlers import RotatingFileHandler
from rag_backend.config.settings import settings

log_file = settings.get("logging.log_file", "./logs/app.log")
log_level = getattr(logging, settings.get("logging.log_level", "INFO"), logging.INFO)

log_dir = os.path.dirname(log_file)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)

root_logger = logging.getLogger()
root_logger.setLevel(log_level)

for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10 * 1024 * 1024,
    backupCount=5
)
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)
