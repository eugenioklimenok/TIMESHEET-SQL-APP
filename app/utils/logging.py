"""Utilidades de logging centralizado."""
from __future__ import annotations

import logging
import sys
from typing import Optional


DEFAULT_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup_logging(level: int = logging.INFO, fmt: str = DEFAULT_FORMAT) -> None:
    """Configura el logging de la aplicación.

    Se configura solo una vez usando ``basicConfig`` para evitar configurar
    múltiples handlers al importar el módulo.
    """

    if logging.getLogger().handlers:
        return

    logging.basicConfig(
        level=level,
        format=fmt,
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Obtiene un logger con la configuración global."""

    return logging.getLogger(name)
