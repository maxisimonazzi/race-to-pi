"""Implementacion incremental de metodos numericos para aproximar pi."""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal

from utils import decimal_sqrt


class PiMethod(ABC):
    """Clase base para metodos de aproximacion de pi."""

    def __init__(self, name: str, color: str, pi_real: Decimal) -> None:
        self.name = name
        self.color = color
        self.pi_real = pi_real
        self._current_value = Decimal(0)
        self._error = abs(pi_real)
        self._iteration = 0

    def update(self) -> None:
        """Avanza una iteracion incremental del metodo."""
        self._current_value = self._compute_next_value()
        self._error = abs(self.pi_real - self._current_value)
        self._iteration += 1

    def get_current_value(self) -> Decimal:
        """Devuelve la aproximacion actual de pi."""
        return self._current_value

    def get_error(self) -> Decimal:
        """Devuelve el error absoluto actual."""
        return self._error

    @abstractmethod
    def _compute_next_value(self) -> Decimal:
        """Calcula el valor de pi para la siguiente iteracion."""


class LeibnizMethod(PiMethod):
    """Serie de Leibniz: pi = 4 * sum((-1)^n / (2n + 1))."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        super().__init__(name="Leibniz", color=color, pi_real=pi_real)
        self._n = 0
        self._partial_sum = Decimal(0)

    def _compute_next_value(self) -> Decimal:
        sign = Decimal(1) if self._n % 2 == 0 else Decimal(-1)
        term = sign / Decimal(2 * self._n + 1)
        self._partial_sum += term
        self._n += 1
        return Decimal(4) * self._partial_sum


class WallisMethod(PiMethod):
    """Producto de Wallis: pi/2 = prod((2n/(2n-1))*(2n/(2n+1)))."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        super().__init__(name="Wallis", color=color, pi_real=pi_real)
        self._n = 1
        self._product = Decimal(1)

    def _compute_next_value(self) -> Decimal:
        n = self._n
        two_n = Decimal(2 * n)
        factor = (two_n / Decimal(2 * n - 1)) * (two_n / Decimal(2 * n + 1))
        self._product *= factor
        self._n += 1
        return Decimal(2) * self._product


class EulerBaselMethod(PiMethod):
    """Serie de Euler (Basilea): pi = sqrt(6 * sum(1 / n^2))."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        super().__init__(name="Euler (Basilea)", color=color, pi_real=pi_real)
        self._n = 1
        self._partial_sum = Decimal(0)

    def _compute_next_value(self) -> Decimal:
        n_decimal = Decimal(self._n)
        self._partial_sum += Decimal(1) / (n_decimal * n_decimal)
        self._n += 1
        return decimal_sqrt(Decimal(6) * self._partial_sum)


class RamanujanMethod(PiMethod):
    """Serie de Ramanujan optimizada por recurrencia para evitar factoriales enormes."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        super().__init__(name="Ramanujan", color=color, pi_real=pi_real)
        self._n = 0
        self._sum_terms = Decimal(0)
        self._b_n = Decimal(1)
        self._pow_396_4 = Decimal(396) ** 4
        self._constant = (Decimal(2) * decimal_sqrt(Decimal(2))) / Decimal(9801)

    def _compute_next_value(self) -> Decimal:
        n = self._n
        coefficient = Decimal(1103 + 26390 * n)
        self._sum_terms += self._b_n * coefficient

        inv_pi = self._constant * self._sum_terms
        pi_value = Decimal(1) / inv_pi

        numerator = Decimal((4 * n + 1) * (4 * n + 2) * (4 * n + 3) * (4 * n + 4))
        denominator = Decimal((n + 1) ** 4) * self._pow_396_4
        self._b_n = self._b_n * numerator / denominator

        self._n += 1
        return pi_value
