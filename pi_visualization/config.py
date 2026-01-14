"""Configuracion global para la visualizacion de pi."""

import math
from decimal import Decimal

# Precision decimal minima para garantizar al menos 15 cifras correctas.
DECIMAL_PRECISION = 25

# Iteraciones maximas del proceso de convergencia.
MAX_ITERATIONS = 1000

# Intervalo entre frames de la animacion (milisegundos).
ANIMATION_INTERVAL_MS = 10

# Escala Y logaritmica para visualizar el error absoluto.
USE_LOG_SCALE_Y_ERROR = True

# Piso numerico para poder mostrar errores en escala logaritmica.
MIN_PLOT_ERROR = Decimal("1e-24")

# Valor de referencia de pi convertido de forma segura a Decimal.
PI_REAL = Decimal(str(math.pi))

# Colores consistentes por metodo.
METHOD_COLORS = {
    "Leibniz": "#1f77b4",
    "Wallis": "#ff7f0e",
    "Euler (Basilea)": "#2ca02c",
    "Ramanujan": "#d62728",
}
