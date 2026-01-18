"""Utilidades numericas para calculo de pi con alta precision."""

from decimal import Decimal, getcontext


def configure_decimal_context(precision: int) -> None:
    """Configura la precision global de Decimal."""
    getcontext().prec = precision


def to_decimal(value: int | float | str | Decimal) -> Decimal:
    """Convierte de forma segura un valor a Decimal."""
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def decimal_sqrt(value: Decimal) -> Decimal:
    """Calcula raiz cuadrada de Decimal usando el contexto actual."""
    if value < 0:
        raise ValueError("No se puede calcular la raiz cuadrada de un valor negativo.")
    if value == 0:
        return Decimal(0)
    return value.sqrt()


class FactorialCache:
    """Cache incremental de factoriales para enteros no negativos."""

    def __init__(self) -> None:
        """Inicializa el almacenamiento interno de factoriales."""
        self._values = [1]

    def factorial(self, n: int) -> int:
        """Devuelve n! reutilizando resultados previos."""
        if n < 0:
            raise ValueError("El factorial no esta definido para enteros negativos.")

        while len(self._values) <= n:
            k = len(self._values)
            self._values.append(self._values[-1] * k)
        return self._values[n]


def format_decimal(value: Decimal, significant_digits: int = 15) -> str:
    """Formatea Decimal para mostrar en tabla sin perder legibilidad."""
    if value == 0:
        return "0"
    return format(value, f".{significant_digits}g")
