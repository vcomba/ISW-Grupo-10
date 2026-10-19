"""Punto de entrada de la demo web (local y Vercel)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from inscripcion_actividades.web import crear_app  # noqa: E402

app = crear_app()

if __name__ == "__main__":
    app.run(debug=True)
