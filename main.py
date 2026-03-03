"""Punto de entrada de la aplicacion de visualizacion de pi."""

from config import (
    ANIMATION_INTERVAL_MS,
    DECIMAL_PRECISION,
    ENABLE_BLIT,
    MAX_ITERATIONS,
    METHOD_COLORS,
    MIN_PLOT_ERROR,
    PI_REAL,
    REDRAW_AXES_EVERY_N_FRAMES,
    REDRAW_TABLE_EVERY_N_FRAMES,
    USE_LOG_SCALE_Y_ERROR,
)
from methods import (
    ChudnovskyMethod,
    EulerBaselMethod,
    GaussLegendreMethod,
    LeibnizMethod,
    MachinMethod,
    NilakanthaMethod,
    RamanujanMethod,
    WallisMethod,
)
from utils import configure_decimal_context
from visualization import PiVisualizationApp


def build_methods():
    """Crea las instancias de metodos numericos con sus colores."""
    return [
        RamanujanMethod(color=METHOD_COLORS["Serie de Ramanujan"], pi_real=PI_REAL),
        LeibnizMethod(color=METHOD_COLORS["Serie de Leibniz"], pi_real=PI_REAL),
        WallisMethod(color=METHOD_COLORS["Producto de Wallis"], pi_real=PI_REAL),
        EulerBaselMethod(color=METHOD_COLORS["Serie de Euler (Problema de Basilea)"], pi_real=PI_REAL),
        MachinMethod(color=METHOD_COLORS["Machin (Arcotangente)"], pi_real=PI_REAL),
        GaussLegendreMethod(color=METHOD_COLORS["Gauss-Legendre (AGM)"], pi_real=PI_REAL),
        NilakanthaMethod(color=METHOD_COLORS["Nilakantha"], pi_real=PI_REAL),
        ChudnovskyMethod(color=METHOD_COLORS["Chudnovsky"], pi_real=PI_REAL),
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
        enable_blit=ENABLE_BLIT,
        redraw_axes_every_n_frames=REDRAW_AXES_EVERY_N_FRAMES,
        redraw_table_every_n_frames=REDRAW_TABLE_EVERY_N_FRAMES,
    )
    app.show()


if __name__ == "__main__":
    main()
