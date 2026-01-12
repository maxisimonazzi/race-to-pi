# Proyecto: Visualización Animada de Métodos Numéricos para Calcular π

## 1. Objetivo General

Desarrollar una aplicación en Python utilizando Matplotlib que permita visualizar de manera animada la convergencia de distintos métodos numéricos para calcular el valor de π.

Se deben comparar los siguientes métodos:

- Serie de Leibniz
- Producto de Wallis
- Serie de Euler (Problema de Basilea)
- Serie de Ramanujan

Para cada método se debe:

- Calcular sucesivas iteraciones.
- Calcular el error absoluto respecto al valor real de π.
- Mostrar la evolución en gráficos animados.
- Trabajar con al menos 15 cifras decimales significativas.

---

## 2. Requerimientos Matemáticos

El valor real de referencia será:

    π = math.pi

Pero el cálculo interno debe realizarse usando alta precisión con:

    from decimal import Decimal, getcontext

Y se debe configurar:

    getcontext().prec = 25

Como mínimo 25 dígitos de precisión para asegurar al menos 15 correctos.

El error debe calcularse como:

    error = abs(pi_real - pi_aproximado)

Donde:
- pi_real será Decimal(str(math.pi))
- pi_aproximado será Decimal

---

## 3. Métodos a Implementar

### 3.1 Serie de Leibniz

π = 4 * Σ [ (-1)^n / (2n+1) ]

Implementación incremental por iteración.

---

### 3.2 Producto de Wallis

π/2 = Π [ (2n / (2n-1)) * (2n / (2n+1)) ]

Implementación acumulativa por iteración.

---

### 3.3 Serie de Euler (Basilea)

π = sqrt(6 * Σ (1/n²))

Implementación acumulativa con uso de Decimal y raíz cuadrada compatible.

---

### 3.4 Serie de Ramanujan

1/π = (2√2 / 9801) * Σ [ ( (4n)! (1103 + 26390n) ) / ( (n!)^4 396^(4n) ) ]

Implementar con cuidado en el manejo de factoriales grandes.
Usar Decimal y funciones auxiliares.

---

## 4. Flujo de Iteración

El programa debe:

1. Definir un número máximo de iteraciones N (configurable al inicio).
2. Para cada iteración i:
   - Calcular el valor aproximado de π para cada método.
   - Calcular el error correspondiente.
   - Guardar resultados en estructuras acumulativas.
3. La animación debe actualizarse en cada iteración.

---

## 5. Visualización (Matplotlib)

Debe haber dos modos de visualización.

---

# MODO 1 — Gráfico de Error

Plano XY:

- Eje X: Número de iteración (escala logaritmica, para ver que el metodo de ramanujan converge muy rapidamente)
- Eje Y: Error absoluto

Debe mostrar:

- 4 curvas simultáneas
- Cada método con un color distinto
- Leyenda indicando el método
- Escala Y posiblemente logarítmica (opcional pero recomendable)

Además:

A la derecha del gráfico debe mostrarse una tabla dinámica con:

- Nombre del método
- Color correspondiente
- Valor aproximado actual
- Error actual

Esta tabla debe actualizarse en cada frame de la animación.

---

# MODO 2 — Gráfico de Aproximación

Plano XY:

- Eje X: Número de iteración (escala logaritmica, para ver que el metodo de ramanujan converge muy rapidamente)
- Eje Y: Valor aproximado de π

Debe incluir:

- Línea horizontal constante en el valor real de π
- Curvas de los 4 métodos
- Tabla lateral igual al modo anterior

---

## 6. Interfaz de Usuario

Debe haber:

Opción A:
- Dos botones en la ventana:
    - "Ver Error"
    - "Ver Aproximación"

Opción B:
- Dos pestañas usando matplotlib.widgets o interfaz compatible.

El usuario puede cambiar de vista sin reiniciar el programa.

---

## 7. Animación

Debe utilizar:

    matplotlib.animation.FuncAnimation

Características:

- Intervalo configurable
- Actualización progresiva
- No recalcular desde cero cada frame (usar acumulación incremental)

---

## 8. Estructura del Proyecto

El proyecto debe organizarse así:

pi_visualization/
│
├── main.py
├── methods.py
├── visualization.py
├── config.py
└── utils.py


### main.py
Control principal del programa.

### methods.py
Implementación de los 4 métodos.
Cada método debe ser una clase con:

- update()
- get_current_value()
- get_error()

### visualization.py
Contiene:
- Lógica de gráficos
- Animación
- Botones
- Tabla lateral

### config.py
- Número de iteraciones
- Precisión decimal
- Colores de cada método

### utils.py
- Funciones auxiliares
- Factoriales grandes
- Conversión Decimal segura

---

## 9. Reglas de Implementación

- Usar únicamente Python estándar + matplotlib.
- No usar librerías externas.
- Código modular y orientado a objetos.
- Documentar funciones con docstrings.
- Mantener claridad matemática.
- Evitar recalcular iteraciones previas.
- Optimizar Ramanujan para evitar explosión computacional.

---

## 10. Criterios de Correctitud

- Las curvas deben tender a error → 0
- Ramanujan debe converger extremadamente rápido
- Leibniz debe converger muy lentamente
- Wallis intermedio
- Euler relativamente rápido

---

## 11. Consideraciones Numéricas Importantes

- Usar Decimal en todos los cálculos.
- Evitar mezclar float con Decimal.
- Implementar sqrt para Decimal correctamente.
- Manejar factoriales con precisión arbitraria.
- Controlar crecimiento de números en Ramanujan.

---

## 12. Resultado Esperado

Una aplicación ejecutable con:

    python main.py

Que abra una ventana interactiva animada mostrando la convergencia comparativa de los métodos. La animacion debe comenzar cuando se presione el boton play para evitar sobrecargar el sistema en la apertura.

El resultado debe ser visualmente claro, estable numéricamente y estructurado profesionalmente.