"""Implementacion incremental de metodos numericos para aproximar pi."""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal

from utils import decimal_sqrt


class PiMethod(ABC):
    """Clase base para metodos de aproximacion de pi."""

    def __init__(self, name: str, color: str, pi_real: Decimal) -> None:
        """Inicializa propiedades comunes de un metodo numerico."""
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
        """Prepara el estado incremental de la serie de Leibniz."""
        super().__init__(name="Serie de Leibniz", color=color, pi_real=pi_real)
        self._n = 0
        self._partial_sum = Decimal(0)

    def _compute_next_value(self) -> Decimal:
        """Actualiza un termino de Leibniz y devuelve la nueva aproximacion."""
        sign = Decimal(1) if self._n % 2 == 0 else Decimal(-1)
        term = sign / Decimal(2 * self._n + 1)
        self._partial_sum += term
        self._n += 1
        return Decimal(4) * self._partial_sum


class WallisMethod(PiMethod):
    """Producto de Wallis: pi/2 = prod((2n/(2n-1))*(2n/(2n+1)))."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        """Prepara el estado incremental del producto de Wallis."""
        super().__init__(name="Producto de Wallis", color=color, pi_real=pi_real)
        self._n = 1
        self._product = Decimal(1)

    def _compute_next_value(self) -> Decimal:
        """Actualiza un factor de Wallis y devuelve la nueva aproximacion."""
        n = self._n
        two_n = Decimal(2 * n)
        factor = (two_n / Decimal(2 * n - 1)) * (two_n / Decimal(2 * n + 1))
        self._product *= factor
        self._n += 1
        return Decimal(2) * self._product


class EulerBaselMethod(PiMethod):
    """Serie de Euler (Basilea): pi = sqrt(6 * sum(1 / n^2))."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        """Prepara el estado incremental de la serie de Basilea."""
        super().__init__(
            name="Serie de Euler (Problema de Basilea)",
            color=color,
            pi_real=pi_real,
        )
        self._n = 1
        self._partial_sum = Decimal(0)

    def _compute_next_value(self) -> Decimal:
        """Actualiza la suma de Basilea y calcula pi mediante raiz cuadrada."""
        n_decimal = Decimal(self._n)
        self._partial_sum += Decimal(1) / (n_decimal * n_decimal)
        self._n += 1
        return decimal_sqrt(Decimal(6) * self._partial_sum)


class RamanujanMethod(PiMethod):
    """Serie de Ramanujan optimizada por recurrencia para evitar factoriales enormes."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        """Inicializa la recurrencia de Ramanujan y su tope de calculo."""
        super().__init__(name="Serie de Ramanujan", color=color, pi_real=pi_real)
        self._max_compute_iterations = 10
        self._n = 0
        self._sum_terms = Decimal(0)
        self._b_n = Decimal(1)
        self._pow_396_4 = Decimal(396) ** 4
        self._constant = (Decimal(2) * decimal_sqrt(Decimal(2))) / Decimal(9801)

    def _compute_next_value(self) -> Decimal:
        """Calcula el siguiente termino de Ramanujan o reutiliza el ultimo valor."""
        # Se deja de calcular Ramanujan en la decima iteracion para evitar computo innecesario.
        if self._n >= self._max_compute_iterations:
            return self._current_value

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


class MachinMethod(PiMethod):
    """Formula de Machin: pi = 16*arctan(1/5) - 4*arctan(1/239)."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        """Inicializa la expansion de arctangente para la formula de Machin."""
        super().__init__(name="Machin (Arcotangente)", color=color, pi_real=pi_real)
        self._max_compute_iterations = 20
        self._x1 = Decimal(1) / Decimal(5)
        self._x2 = Decimal(1) / Decimal(239)
        self._x1_sq = self._x1 * self._x1
        self._x2_sq = self._x2 * self._x2
        self._term1 = self._x1
        self._term2 = self._x2
        self._sum1 = Decimal(0)
        self._sum2 = Decimal(0)
        self._n = 0

    def _compute_next_value(self) -> Decimal:
        """Actualiza Machin por series de arctan o congela tras 20 iteraciones."""
        # Se deja de calcular Machin en la veinteava iteracion para mantener rendimiento.
        if self._n >= self._max_compute_iterations:
            return self._current_value

        self._sum1 += self._term1
        self._sum2 += self._term2

        ratio = Decimal(2 * self._n + 1) / Decimal(2 * self._n + 3)
        self._term1 = -self._term1 * self._x1_sq * ratio
        self._term2 = -self._term2 * self._x2_sq * ratio

        self._n += 1
        return Decimal(16) * self._sum1 - Decimal(4) * self._sum2


class GaussLegendreMethod(PiMethod):
    """Metodo AGM de Gauss-Legendre para aproximar pi."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        """Inicializa variables AGM y tope de calculo para Gauss-Legendre."""
        super().__init__(name="Gauss-Legendre (AGM)", color=color, pi_real=pi_real)
        self._max_compute_iterations = 10
        self._n = 0
        self._a = Decimal(1)
        self._b = Decimal(1) / decimal_sqrt(Decimal(2))
        self._t = Decimal(1) / Decimal(4)
        self._p = Decimal(1)

    def _compute_next_value(self) -> Decimal:
        """Ejecuta una iteracion AGM o reutiliza el ultimo valor tras 10 iteraciones."""
        # Se deja de calcular Gauss-Legendre en la decima iteracion por convergencia rapida.
        if self._n >= self._max_compute_iterations:
            return self._current_value

        next_a = (self._a + self._b) / Decimal(2)
        next_b = decimal_sqrt(self._a * self._b)
        delta = self._a - next_a
        self._t = self._t - self._p * delta * delta
        self._p = self._p * Decimal(2)
        self._a = next_a
        self._b = next_b
        numerator = (self._a + self._b) * (self._a + self._b)
        self._n += 1
        return numerator / (Decimal(4) * self._t)


class NilakanthaMethod(PiMethod):
    """Serie de Nilakantha: pi = 3 + sum((-1)^(n+1)*4/((2n)(2n+1)(2n+2)))."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        """Prepara el estado incremental de la serie de Nilakantha."""
        super().__init__(name="Nilakantha", color=color, pi_real=pi_real)
        self._n = 1
        self._partial_sum = Decimal(0)

    def _compute_next_value(self) -> Decimal:
        """Actualiza un termino de Nilakantha y devuelve la aproximacion resultante."""
        n = self._n
        a = Decimal(2 * n)
        term = Decimal(4) / (a * (a + 1) * (a + 2))
        if n % 2 == 1:
            self._partial_sum += term
        else:
            self._partial_sum -= term
        self._n += 1
        return Decimal(3) + self._partial_sum


class ChudnovskyMethod(PiMethod):
    """Serie de Chudnovsky con actualizacion incremental por recurrencia."""

    def __init__(self, color: str, pi_real: Decimal) -> None:
        """Inicializa la serie de Chudnovsky con recurrencia y tope de calculo."""
        super().__init__(name="Chudnovsky", color=color, pi_real=pi_real)
        self._max_compute_iterations = 10
        self._k = 0
        self._m = 1
        self._l = 13591409
        self._x = 1
        self._k_factor = 6
        self._sum_terms = Decimal(self._l)
        self._constant = Decimal(426880) * decimal_sqrt(Decimal(10005))

    def _compute_next_value(self) -> Decimal:
        """Actualiza Chudnovsky o congela el valor luego de 10 iteraciones."""
        # Se deja de calcular Chudnovsky en la decima iteracion por convergencia muy alta.
        if self._k >= self._max_compute_iterations:
            return self._current_value

        if self._k > 0:
            numerator = self._k_factor**3 - 16 * self._k_factor
            self._m = (self._m * numerator) // (self._k**3)
            self._l += 545140134
            self._x *= -262537412640768000
            self._sum_terms += Decimal(self._m * self._l) / Decimal(self._x)
            self._k_factor += 12

        pi_value = self._constant / self._sum_terms
        self._k += 1
        return pi_value
