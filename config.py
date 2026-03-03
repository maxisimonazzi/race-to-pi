"""Configuracion global para la visualizacion de pi."""

import math
from decimal import Decimal

# Precision decimal minima para garantizar al menos 15 cifras correctas.
DECIMAL_PRECISION = 25

# Iteraciones maximas del proceso de convergencia.
MAX_ITERATIONS = 100

# Intervalo entre frames de la animacion (milisegundos).
ANIMATION_INTERVAL_MS = 10

# Escala Y logaritmica para visualizar el error absoluto.
USE_LOG_SCALE_Y_ERROR = True

# Piso numerico para poder mostrar errores en escala logaritmica.
MIN_PLOT_ERROR = Decimal("1e-24")

# Valor de referencia de pi convertido de forma segura a Decimal.
PI_REAL = Decimal(str(math.pi))

# Iteraciones maximas de calculo real por metodo (luego se congela el ultimo valor):
# - Ramanujan: convergencia extraordinariamente rapida; en ~10 terminos ya supera la precision usada.
RAMANUJAN_MAX_COMPUTE_ITERATIONS = 10
# - Chudnovsky: cada termino agrega muchas cifras correctas de pi, por eso 10 iteraciones son suficientes.
CHUDNOVSKY_MAX_COMPUTE_ITERATIONS = 10
# - Gauss-Legendre (AGM): convergencia cuadratica; con pocas iteraciones alcanza precision alta.
GAUSS_LEGENDRE_MAX_COMPUTE_ITERATIONS = 10
# - Machin: convergencia alta pero mas gradual que AGM/Ramanujan; se extiende a 20 iteraciones.
MACHIN_MAX_COMPUTE_ITERATIONS = 20

# Colores consistentes por metodo.
METHOD_COLORS = {
    "Serie de Ramanujan": "#d62728",
    "Serie de Leibniz": "#1f77b4",
    "Producto de Wallis": "#ff7f0e",
    "Serie de Euler (Problema de Basilea)": "#2ca02c",
    "Machin (Arcotangente)": "#9467bd",
    "Gauss-Legendre (AGM)": "#8c564b",
    "Nilakantha": "#e377c2",
    "Chudnovsky": "#17becf",
}
