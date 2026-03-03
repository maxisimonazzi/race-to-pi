# La carrera de pi - Visualizacion animada de metodos numericos

Aplicacion en Python + Matplotlib para comparar como convergen distintos metodos numericos al calcular el valor de pi.

El proyecto muestra, en tiempo real, la evolucion del error y de la aproximacion de cada metodo, usando calculo de alta precision con `Decimal`.

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

La app permite ver:

- Error absoluto por iteracion.
- Valor aproximado de pi por iteracion.
- Tabla lateral dinamica con metodo, color, aproximacion y error.

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

