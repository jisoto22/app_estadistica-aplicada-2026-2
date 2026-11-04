# Plan de desarrollo

## Objetivo

Construir una aplicación multipágina en Streamlit para explorar datos y aplicar métodos de estadística aplicada pertinentes a problemas de Ingeniería Agrícola. La aplicación debe hacer visibles los supuestos, las unidades y las limitaciones de cada análisis; no debe presentar un resultado estadístico como válido cuando los datos no cumplan las condiciones necesarias.

## Páginas, entradas y resultados

| Página | Entradas principales | Funciones, tablas y gráficas |
|---|---|---|
| **Inicio** | Ninguna; opcionalmente selección de un conjunto de datos de ejemplo cuando se incorpore uno. | Presentar el propósito, la navegación y un resumen del conjunto de datos activo (filas, columnas y período, si corresponde). Mostrar avisos sobre datos faltantes o análisis aún no ejecutados. No realizar inferencia estadística. |
| **Datos** | Archivo CSV o Excel, hoja si aplica, delimitador y separador decimal cuando corresponda; selección de columnas, tipos y valores faltantes. | Validar la carga, mostrar una vista previa, dimensiones, nombres y tipos de variables, faltantes y posibles duplicados. Permitir seleccionar variables y aplicar transformaciones explícitas sin alterar silenciosamente el archivo original. |
| **EDA: Análisis Exploratorio de Datos** | Conjunto de datos cargado; selección de variables y agrupación opcional (por ejemplo, estación, cultivo o año). | Tabla de resumen con n, faltantes, media, mediana, desviación estándar, mínimo, máximo y cuartiles; frecuencias para variables categóricas. Histogramas y densidades, diagramas de caja, gráficos de dispersión y, si hay fechas, gráficos de evolución. Facilitar la detección de asimetría, valores extremos, patrones temporales y asociaciones iniciales. |
| **Distribuciones** | Serie de máximos anuales de precipitación (una observación por año), unidad, período de retorno o nivel de riesgo; distribuciones seleccionadas. Para secado: tiempo y contenido de humedad observados, base de humedad, valor de humedad de equilibrio si se requiere y modelos candidatos. | Para precipitación, tabla comparativa de parámetros, log-verosimilitud, KS, Anderson-Darling, AIC, BIC y AICc; curvas de densidad y de distribución acumulada con datos empíricos; gráfico de niveles de retorno. Para secado, tabla con parámetros y AICc, curvas observadas/ajustadas y residuos por modelo. Presentar intervalos o bandas de incertidumbre cuando se implementen y documentar el método usado. |
| **Regresión** | Dos variables cuantitativas (predictora y respuesta), selección opcional de filas o grupos y nivel de significancia. | Tabla de Pearson y Spearman con tamaño muestral y p-valor; ecuación estimada por MCO, errores estándar, intervalo de confianza y prueba de la pendiente; R², R² ajustado, RMSE y tabla ANOVA. Mostrar dispersión con recta e intervalo, residuos frente a ajustados, gráfico Q-Q y observaciones influyentes. |
| **Series de tiempo** | Variable, fecha o índice temporal, frecuencia, método de agregación si hay más de una observación por período, horizonte de pronóstico y ventana de evaluación. | Gráfico de la serie y sus componentes; tablas/gráficas de promedios móviles e índices estacionales; descomposición clásica aditiva o multiplicativa cuando sea apropiada; comparación de métodos de referencia y modelos AutoTS. Tabla de validación con MAE, RMSE y SMAPE, más pronóstico e intervalos si el método los proporciona. |

## Cálculos estadísticos

### Datos y EDA

- Resumir cada variable numérica con cantidad de observaciones válidas, media, mediana, desviación estándar muestral, mínimo, máximo y cuartiles. Para variables categóricas, calcular conteos y proporciones.
- Contabilizar valores faltantes y duplicados antes de cualquier análisis. No imputar ni eliminar observaciones sin una decisión visible y documentada.
- Construir las gráficas a partir de las variables y filtros seleccionados. Las asociaciones exploratorias no se deben interpretar como evidencia causal.

### Distribuciones de precipitación máxima anual

- Ajustar Normal, Lognormal, Gamma, Weibull, Gumbel y GEV a máximos anuales. Verificar tamaño de muestra, finitud, valores positivos cuando la distribución lo exige y configuración de parámetros (por ejemplo, ubicación, escala y forma); mostrar el método de estimación utilizado.
- Calcular la función de verosimilitud y los criterios de información, con k parámetros y n observaciones: AIC = 2k - 2 logLik; BIC = k log(n) - 2 logLik; AICc = AIC + 2k(k + 1)/(n - k - 1), cuando n > k + 1. Menores valores indican mejor ajuste relativo entre modelos ajustados a los mismos datos, no una prueba de que el modelo sea correcto.
- Comparar la distribución empírica y la ajustada con la estadística KS y la de Anderson-Darling. Si los parámetros se estiman con la misma muestra, los p-valores estándar de estas pruebas pueden no ser válidos; usar calibración por bootstrap paramétrico o dejar clara esa limitación. No seleccionar un modelo solo por un p-valor.
- Para período de retorno T en años, bajo independencia y estacionariedad, calcular la probabilidad anual de excedencia p = 1/T y el nivel de retorno con el cuantil F⁻¹(1 - 1/T). Calcular el riesgo de al menos una excedencia en N años como 1 - (1 - 1/T)^N. Explicar que estos resultados dependen del modelo y de los supuestos; cuantificar incertidumbre mediante un método definido (por ejemplo, bootstrap) y mostrar intervalos, no solo estimaciones puntuales.

### Modelos de secado en capa delgada

- Ajustar los modelos de secado seleccionados a la razón de humedad frente al tiempo, indicando la forma de la ecuación, las unidades y las restricciones de parámetros. Documentar cómo se calcula la razón de humedad y si se conoce o estima la humedad de equilibrio.
- Para cada ajuste, calcular log-verosimilitud bajo una hipótesis de error declarada, número de parámetros y AICc; comparar solo modelos evaluados sobre las mismas observaciones y la misma respuesta. Revisar curvas ajustadas y residuos. Menor AICc favorece el modelo relativamente más informativo entre los candidatos, pero no sustituye la evaluación física ni la validación externa.

### Regresión

- Calcular correlación de Pearson (asociación lineal) y Spearman (asociación monótona basada en rangos), con p-valores e indicación de datos válidos usados.
- Estimar por MCO la pendiente y el intercepto de la regresión lineal simple. Informar errores estándar, intervalos de confianza y prueba t de H₀: pendiente = 0, además de R², R² ajustado, RMSE y ANOVA.
- Diagnosticar linealidad, varianza aproximadamente constante, independencia, normalidad aproximada de residuos para la inferencia clásica y observaciones influyentes. Mostrar los diagnósticos; no convertirlos en una garantía automática de validez. Advertir que una correlación o regresión no prueba causalidad.

### Series de tiempo

- Representar tendencia, estacionalidad y residuo; calcular promedios móviles centrados cuando corresponda e índices estacionales a partir de la frecuencia definida. Aplicar descomposición clásica aditiva si la amplitud estacional es aproximadamente constante o multiplicativa si varía proporcionalmente al nivel; exigir una frecuencia y cobertura suficientes.
- Comparar pronósticos con métodos de referencia apropiados, como último valor, media histórica, deriva y método estacional ingenuo cuando haya estacionalidad.
- Evaluar usando separación temporal (origen móvil o período de prueba posterior al entrenamiento), nunca una partición aleatoria que mezcle futuro y pasado. Calcular MAE y RMSE en las unidades de la variable. Calcular SMAPE con denominador protegido cuando los valores observados y pronosticados son ambos cercanos a cero, y documentar su fórmula y convención.
- Usar AutoTS para generar y comparar candidatos dentro de los datos de entrenamiento; seleccionar según una métrica y un esquema de validación declarados, reajustar sin fuga de información y producir el horizonte solicitado. Si AutoTS no está instalado o no resulta compatible, la página debe explicar que esa función no está disponible en vez de fallar silenciosamente.

## Organización modular propuesta

```text
app.py
pages/
  1_Inicio.py
  2_Datos.py
  3_EDA.py
  4_Distribuciones.py
  5_Regresion.py
  6_Series_de_tiempo.py
src/
  carga_datos.py
  validacion.py
  estadistica_descriptiva.py
  distribuciones.py
  secado.py
  regresion.py
  series_tiempo.py
  visualizacion.py
datos/
  README.md
verificacion/
  test_validacion.py
  test_distribuciones.py
  test_regresion.py
  test_series_tiempo.py
docs/
  PLAN_DESARROLLO.md
```

- `app.py` configura la aplicación, el título, la navegación compartida y el estado común de sesión; el cálculo estadístico no debe concentrarse ahí.
- `pages/` contiene la interfaz de cada página: entradas, mensajes de validación, tablas y gráficas. Las páginas llaman funciones de `src/` para mantener una sola implementación de cada cálculo.
- `src/` reúne carga y validación de datos, funciones estadísticas puras y rutinas de visualización reutilizables. Separar validación de cálculo hace más fácil probar casos límite sin ejecutar Streamlit.
- `datos/` se reserva para datos de ejemplo pequeños, anonimizados y con unidades/documentación. Los datos del usuario no se guardan automáticamente; archivos grandes o sensibles deben mantenerse fuera del repositorio.
- `verificacion/` contiene pruebas reproducibles para fórmulas, validaciones, casos límite y resultados conocidos. Incluir pruebas de datos insuficientes, faltantes y entradas inválidas además de casos nominales.
- Las dependencias se definirán más adelante cuando se conozcan las funciones implementadas. Este plan no instala paquetes ni crea esos módulos.

## Orden recomendado de construcción

1. **Definir contratos y datos de prueba.** Acordar tipos de variables, formatos, unidades y reglas de validación. Evita que cada página interprete fechas o faltantes de forma distinta.
2. **Crear la estructura multipágina y navegación.** Implementar Inicio y Datos primero, validando carga, vista previa y manejo de errores antes de sumar análisis.
3. **Añadir EDA.** Reutilizar el flujo de datos validado y construir resúmenes/gráficas que ayuden a descubrir problemas antes del modelado.
4. **Implementar Regresión.** Es un módulo acotado y permite establecer convenciones para estimación, inferencia, diagnósticos y pruebas unitarias.
5. **Implementar Distribuciones y secado.** Separar los dos problemas dentro de la página porque tienen respuestas, supuestos y modelos distintos. Verificar estimación y criterios con casos conocidos antes de exponerlos en la interfaz.
6. **Implementar Series de tiempo por etapas.** Primero componentes, promedios, índices y métodos de referencia; después validación temporal y métricas; por último AutoTS y pronósticos. Así se puede verificar el protocolo contra fugas de información antes de incorporar búsqueda de modelos.
7. **Revisar de extremo a extremo.** Probar carga, navegación, datos inválidos y flujos completos; confirmar que tablas, gráficas, unidades, supuestos e incertidumbre sean coherentes y comprensibles para el usuario.

Este orden construye primero una base común verificable, permite entregar valor exploratorio temprano y reserva los modelos con más supuestos y dependencias para cuando la aplicación ya tenga datos y validación confiables.