#!/usr/bin/env python3
"""
MiroFish - A fish tank monitoring and automation system.
Main entry point for the application.
"""

import os
import logging
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def get_config() -> dict:
    """Load and validate configuration from environment variables."""
    config = {
        "host": os.getenv("APP_HOST", "0.0.0.0"),
        "port": int(os.getenv("APP_PORT", "8080")),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "database_url": os.getenv("DATABASE_URL", ""),
        "mqtt_broker": os.getenv("MQTT_BROKER", ""),
        "mqtt_port": int(os.getenv("MQTT_PORT", "1883")),
        "mqtt_topic_prefix": os.getenv("MQTT_TOPIC_PREFIX", "mirofish"),
        "sensor_poll_interval": int(os.getenv("SENSOR_POLL_INTERVAL", "60")),
    }

    # Validate required configuration
    missing = []
    if not config["database_url"]:
        missing.append("DATABASE_URL")
    if not config["mqtt_broker"]:
        missing.append("MQTT_BROKER")

    if missing:
        logger.warning(
            "Missing recommended environment variables: %s", ", ".join(missing)
        )

    return config


async def main():
    """Main async entry point for MiroFish application."""
    logger.info("Starting MiroFish...")

    config = get_config()
    logger.info(
        "Configuration loaded — host: %s, port: %d, debug: %s",
        config["host"],
        config["port"],
        config["debug"],
    )

    # Placeholder for future service initialization
    # from app.server import create_app
    # from app.mqtt import MQTTClient
    # from app.database import init_db

    logger.info("MiroFish initialized successfully.")
    logger.info(
        "Sensor polling interval: %d seconds", config["sensor_poll_interval"]
    )

    # Keep the application running
    try:
        while True:
            await asyncio.sleep(config["sensor_poll_interval"])
            logger.debug("Heartbeat — application is running.")
    except asyncio.CancelledError:
        logger.info("Shutdown signal received.")
    finally:
        logger.info("MiroFish stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Exiting.")
