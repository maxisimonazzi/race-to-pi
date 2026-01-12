"""Punto de entrada de la aplicacion de visualizacion de pi."""

from config import (
    ANIMATION_INTERVAL_MS,
    DECIMAL_PRECISION,
    MAX_ITERATIONS,
    METHOD_COLORS,
    MIN_PLOT_ERROR,
    PI_REAL,
    USE_LOG_SCALE_Y_ERROR,
)
from methods import EulerBaselMethod, LeibnizMethod, RamanujanMethod, WallisMethod
from utils import configure_decimal_context
from visualization import PiVisualizationApp


def build_methods():
    """Crea las instancias de metodos numericos con sus colores."""
    return [
        LeibnizMethod(color=METHOD_COLORS["Leibniz"], pi_real=PI_REAL),
        WallisMethod(color=METHOD_COLORS["Wallis"], pi_real=PI_REAL),
        EulerBaselMethod(color=METHOD_COLORS["Euler (Basilea)"], pi_real=PI_REAL),
        RamanujanMethod(color=METHOD_COLORS["Ramanujan"], pi_real=PI_REAL),
    ]


def main() -> None:
    """Configura la app y abre la ventana interactiva."""
    configure_decimal_context(DECIMAL_PRECISION)

    app = PiVisualizationApp(
        methods=build_methods(),
        pi_real=PI_REAL,
        max_iterations=MAX_ITERATIONS,
        animation_interval_ms=ANIMATION_INTERVAL_MS,
        use_log_scale_y_error=USE_LOG_SCALE_Y_ERROR,
        min_plot_error=MIN_PLOT_ERROR,
    )
    app.show()


if __name__ == "__main__":
    main()
