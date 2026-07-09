# Codebook: ventas_limpio.csv

Dataset de ventas de una tienda (datos sinteticos), version limpia generada
por el pipeline en `src/` (etapas `01_ingesta.py` -> `02_deduplicacion.py` ->
`03_tipado.py` -> `04_features.py`) a partir de `data/raw/ventas.csv`.
Ver `README.md` para el detalle de cada etapa.

| Variable         | Tipo (Python/pandas) | Descripcion                                              | Valores validos / notas                              |
|------------------|-----------------------|-----------------------------------------------------------|--------------------------------------------------------|
| id_venta         | int                   | Identificador unico de la venta                           | Entero positivo, sin duplicados                        |
| fecha            | datetime64            | Fecha en que se realizo la venta                           | Se estandarizo desde 4 formatos distintos en crudo     |
| producto         | str                   | Nombre del producto vendido                                | Texto libre                                             |
| categoria        | str (categorica)      | Categoria del producto                                     | Electronica, Ropa, Hogar, Deportes                      |
| precio_unitario  | float                 | Precio de una unidad del producto, en quetzales             | Sin simbolo de moneda, siempre positivo                |
| cantidad         | float (int logico)    | Unidades vendidas                                           | Entero positivo (llega como texto en crudo, ej. "dos") |
| cliente_email    | str                   | Correo del cliente                                          | Se repara la `@` faltante si el dominio es conocido; formato validado con regex; invalidos -> NA |
| metodo_pago      | str (categorica)      | Forma de pago utilizada                                     | tarjeta, efectivo, transferencia                        |
| en_oferta        | bool                  | Si la venta se hizo con descuento                            | True / False                                            |
| calificacion     | float (int logico)    | Calificacion del cliente sobre la compra                     | Entero entre 1 y 5; fuera de rango -> NA                |
| total_venta      | float                 | Columna derivada: precio_unitario * cantidad                 | Calculada en la limpieza, no viene en crudo             |

## Reglas de limpieza aplicadas

- Se unificaron marcadores de nulo (`""`, `NA`, `N/A`, `null`, `NULL`, `-`, `?`)
  a un unico valor faltante (`NaN`).
- Se eliminaron filas duplicadas exactas y duplicados de `id_venta`
  (se conserva la primera ocurrencia).
- `fecha` se parseo probando 4 formatos comunes de captura manual.
- `precio_unitario` se limpio de simbolos de moneda (`Q`, `$`) y comas de
  miles; los valores negativos se tomaron como error de captura y se
  convirtieron a su valor absoluto.
- `cantidad` convierte numeros escritos en palabras (uno, dos, tres...) a
  su equivalente numerico.
- `cliente_email`: primero se **repara** el formato cuando falta la `@` pero el
  texto termina en un dominio conocido (`gmail.com`, `hotmail.com`, `uvg.edu.gt`),
  ej. `cliente131gmail.com` -> `cliente131@gmail.com` (el dato existe, solo estaba
  mal escrito). Luego se valida con una expresion regular basica; los que aun no
  cumplen el formato se marcan como faltantes.
- `categoria` y `metodo_pago` se normalizaron a un conjunto fijo de
  categorias (mismo dato escrito con mayusculas/minusculas/espacios distintos
  se unifica).
- `calificacion` fuera del rango 1-5 se descarta por ser un error de captura.

## Valores faltantes (NaN): por que quedan y como se justifican

La limpieza deja cada celda en uno de dos estados: **valida** o **faltante
(NaN)**. NO se imputan (rellenan) faltantes en esta etapa: como tratarlos
(descartar filas, imputar por media/mediana/modelo, etc.) es una decision de
**analisis** que se documentara y justificara mas adelante, en el EDA. Rellenar
aqui meteria un supuesto oculto antes de ver los datos.

Por la misma razon, **tampoco se eliminan filas por tener valores faltantes**.
Una fila con un solo dato ausente (ej. `id_venta` 65: solo le falta
`precio_unitario`) sigue siendo util para todo analisis que no dependa de esa
columna (conteos por categoria, calificaciones, metodo de pago, etc.). Borrarla
en la limpieza le impondria a *todos* los analisis la restriccion de uno solo, y
es irreversible. Cada analisis descarta faltantes (`dropna`) solo sobre las
columnas que necesita, y lo justifica ahi. Solo se eliminarian en la limpieza
filas basura (casi todas vacias) o que violen una regla dura (sin `id_venta`,
duplicadas), lo cual no ocurre en este dataset.

Los NaN del dataset final caen en dos categorias, ambas legitimas:

1. **Ausente en el origen** — la celda nunca se capturo (venia vacia o con un
   marcador de nulo). NaN es la representacion honesta del dato que no existe.
   Aplica a `fecha`, `precio_unitario`, `cantidad`, `metodo_pago`, `en_oferta`,
   y parte de `cliente_email` y `calificacion`.

2. **Rechazado por invalido** — habia un valor, pero no es confiable y
   conservarlo sesgaria el analisis:
   - `calificacion` con `-1` o `7`: fuera de la escala 1-5.
   - `cliente_email` que sigue sin `@` valida tras el intento de reparacion.

`total_venta` (derivada) queda NaN cuando falta `precio_unitario` o `cantidad`;
es propagacion correcta, no un dato perdido aparte.

## Fuente de los datos

Dataset sintetico generado para fines didacticos (curso de Data Mining,
UVG). Simula ventas capturadas manualmente por distintos empleados, de ahi
la inconsistencia en formatos.
