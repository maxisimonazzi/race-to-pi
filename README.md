# La carrera de pi - Visualizacion animada de metodos numericos

Aplicacion en Python + Matplotlib para comparar como convergen distintos metodos numericos al calcular el valor de pi.

El proyecto muestra, en tiempo real, la evolucion del error y de la aproximacion de cada metodo, usando calculo de alta precision con `Decimal`.

## Video del error
https://github.com/user-attachments/assets/544a36b8-9eef-4539-8e2a-3460bb8a3616

## Video de la aproximación
https://github.com/user-attachments/assets/f27da360-bd09-4123-bbed-84a3dd3688a1

---

## Objetivo

Comparar visualmente la convergencia de 8 metodos para aproximar pi:

1. Serie de Ramanujan
2. Serie de Leibniz
3. Producto de Wallis
4. Serie de Euler (Problema de Basilea)
5. Machin (Arcotangente)
6. Gauss-Legendre (AGM)
7. Nilakantha
8. Chudnovsky

La animación mostrará:

1.  Error absoluto en función del número de iteración.
2.  Aproximación progresiva al valor real de π.
3.  Comparación directa entre métodos clásicos y modernos.
4.  Tabla lateral dinamica con metodo, color, aproximacion y error.

Se espera observar:

-   Convergencia extremadamente lenta en Leibniz.
-   Caída abrupta del error en Ramanujan y Chudnovsky.
-   Comportamiento intermedio en Machin y Euler.
-   Convergencia cuadrática destacada en Gauss--Legendre.

---

## Estructura del proyecto

El proyecto esta organizado en modulos:

- `main.py`: punto de entrada, construccion de metodos y lanzamiento de la app.
- `methods.py`: implementacion orientada a objetos de todos los metodos numericos.
- `visualization.py`: interfaz interactiva, animacion, botones y tabla lateral.
- `config.py`: parametros globales (precision, iteraciones, colores, limites por metodo).
- `utils.py`: funciones auxiliares para manejo de `Decimal` y formato.

---

## Requisitos

- Python 3.10 o superior.
- Matplotlib instalado en el entorno.
- PySide6 (usado por el backend `QtAgg` de Matplotlib).

## Instalacion de dependencias

Desde la carpeta raiz del proyecto:

```bash
pip install matplotlib PySide6
```

---

## Ejecucion

Desde la carpeta raiz del proyecto:

```bash
python main.py
```

Se abre una ventana interactiva de Matplotlib con la animacion.

---

## Controles de la interfaz

- `Ver Error`: muestra el grafico de error absoluto.
- `Ver Aproximacion`: muestra el grafico de aproximacion de pi.
- `Play / Pausa`: inicia o pausa la animacion.
- `Reset`: reinicia toda la aplicacion al estado inicial.
- `CheckButtons` (panel de metodos visibles): permite activar/desactivar metodos tanto en el grafico como en la tabla.

---

## Configuracion principal (`config.py`)

Parametros importantes:

- `DECIMAL_PRECISION`: precision global de `Decimal`.
- `MAX_ITERATIONS`: iteraciones maximas de la animacion.
- `ANIMATION_INTERVAL_MS`: tiempo entre frames.
- `USE_LOG_SCALE_Y_ERROR`: activa escala log en Y para modo error.
- `MIN_PLOT_ERROR`: piso numerico para evitar problemas visuales con error muy pequeno.
- `PI_REAL`: valor de referencia de pi.
- `METHOD_COLORS`: colores por metodo.

### Limites de calculo por metodo

Para metodos de convergencia muy rapida se define un tope de calculo real y luego se reutiliza el ultimo valor:

- `RAMANUJAN_MAX_COMPUTE_ITERATIONS = 10`
- `CHUDNOVSKY_MAX_COMPUTE_ITERATIONS = 10`
- `GAUSS_LEGENDRE_MAX_COMPUTE_ITERATIONS = 10`
- `MACHIN_MAX_COMPUTE_ITERATIONS = 20`

Motivo: luego de pocas iteraciones, estos metodos ya alcanzan precision muy alta para el contexto visual del proyecto, por lo que seguir calculando agrega costo computacional y casi nulo beneficio en la grafica.

---

## Diseño numerico

- Todos los metodos trabajan con `Decimal`.
- Se evita mezclar `float` en los calculos internos.
- El error se calcula como:

```python
error = abs(pi_real - pi_aproximado)
```

- Para graficar, se convierte a `float` solo al momento de dibujar.

---

## Diseno de software

- Enfoque orientado a objetos:
  - Clase base `PiMethod`.
  - Cada metodo implementa `_compute_next_value()`.
  - API comun por metodo:
    - `update()`
    - `get_current_value()`
    - `get_error()`

- Calculo incremental:
  - No se recalcula desde cero en cada frame.
  - Cada metodo mantiene su estado interno entre iteraciones.

---

## Fundamentos

El valor de referencia utilizado es:

``` math
\pi \approx 3.141592653589793...
```

## Serie de Ramanujan

``` math
\frac{1}{\pi} = \frac{2\sqrt{2}}{9801} \sum_{n=0}^{\infty} \frac{(4n)! (1103 + 26390n)}{(n!)^4 396^{4n}}
```

------------------------------------------------------------------------

## Serie de Leibniz

``` math
\pi = 4 \sum_{n=0}^{\infty} \frac{(-1)^n}{2n+1}
```

------------------------------------------------------------------------

## Producto de Wallis

``` math
\frac{\pi}{2} = \prod_{n=1}^{\infty} \left( \frac{2n}{2n-1} \cdot \frac{2n}{2n+1} \right)
```

------------------------------------------------------------------------

## Serie de Euler (Problema de Basilea)

``` math
\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}
```

``` math
\pi = \sqrt{6 \sum_{n=1}^{\infty} \frac{1}{n^2}}
```

------------------------------------------------------------------------

## Fórmula de Machin

``` math
\pi = 16 \arctan\left(\frac{1}{5}\right) - 4 \arctan\left(\frac{1}{239}\right)
```

``` math
\arctan(x) = \sum_{n=0}^{\infty} (-1)^n \frac{x^{2n+1}}{2n+1}, \quad |x| \le 1
```

------------------------------------------------------------------------

## Método de Gauss--Legendre (AGM)

``` math
a_0 = 1, \quad b_0 = \frac{1}{\sqrt{2}}, \quad t_0 = \frac{1}{4}, \quad p_0 = 1
```

``` math
a_{n+1} = \frac{a_n + b_n}{2}, \quad b_{n+1} = \sqrt{a_n b_n}, \quad t_{n+1} = t_n - p_n (a_n - a_{n+1})^2, \quad p_{n+1} = 2 p_n
```

``` math
\pi \approx \frac{(a_n + b_n)^2}{4 t_n}
```

------------------------------------------------------------------------

## Serie de Nilakantha

``` math
\pi = 3 + \sum_{n=1}^{\infty} (-1)^{n+1} \frac{4}{(2n)(2n+1)(2n+2)}
```

------------------------------------------------------------------------

## Serie de Chudnovsky

``` math
\frac{1}{\pi} = 12 \sum_{n=0}^{\infty} \frac{(-1)^n (6n)! (13591409 + 545140134n)}{(3n)! (n!)^3 (640320)^{3n + \frac{3}{2}}}
```

------------------------------------------------------------------------

# Comparativa de Convergencia


|Método | Tipo de Convergencia | Velocidad Aproximada | Iteraciones para \~15|
|-|-|-|-|
|Leibniz|Lineal muy lenta|Muy lenta|\~10 millones|
|Wallis|Lineal lenta|Lenta|\~100 mil|
|Nilakantha|Lineal mejorada|Lenta-intermedia|\~10 mil|
|Euler (Basilea)|Polinómica|Intermedia|\~1000|
|Machin|Serie de arctan|Rápida|\~100|
|Gauss-Legendre|Cuadrática|Muy rápida|\~5|
|Ramanujan|Cuasi-exponencial|Extremadamente Rapida|1-2|
|Chudnovsky|Cuasi-exponencial|Extremadamente Rapida|1|

---

## Resultado esperado

La herramienta permite observar claramente comportamientos tipicos:

- Ramanujan y Chudnovsky convergen muy rapido.
- Gauss-Legendre converge muy rapido por AGM.
- Machin converge rapido.
- Euler y Wallis convergen de forma intermedia.
- Leibniz converge mas lentamente.

---

## Notas

- Si queres ajustar rendimiento o nivel de detalle visual, modifica primero:
  - `MAX_ITERATIONS`
  - `ANIMATION_INTERVAL_MS`
  - limites por metodo en `config.py`

- El proyecto esta preparado para extenderse facilmente agregando nuevos metodos en `methods.py` y registrandolos en `main.py`.

