# OrderSystem · Integration Testing y Continuous Integration

Taller de 90 minutos en equipos de cinco. Van a diseñar sus propias pruebas de integración y a configurar GitHub Actions para ejecutar
la suite cada vez que suban cambios a `main` con `git push`. Los cinco
trabajarán en esa misma rama.

## Antes de clase

Un integrante crea el repositorio del equipo con **Use this template** y
agrega a los otros cuatro como colaboradores. Todo el equipo debe aceptar la
invitación y poder clonar el repo. Confirmen que la rama de trabajo sea `main`.
<img width="805" height="77" alt="image" src="https://github.com/user-attachments/assets/9b7231ac-ac75-4a8c-8536-3327345ddde4" />


## Flujo del pedido

La interfaz de línea de comandos (CLI) recibe el producto, la cantidad y el token de pago y delega en
`OrderService`. El servicio comprueba que haya stock suficiente, consulta el
precio, calcula el total con el IVA configurado y solicita el cobro a
`PaymentGateway`. La pasarela convierte la respuesta HTTP en un resultado para
el servicio. Con el pago aprobado, el servicio registra el pedido y descuenta
las unidades. Si el pago se rechaza, el servicio informa el rechazo, conserva
el inventario y deja el pedido sin registrar. La CLI comunica el resultado al
usuario.

La base de datos y el proveedor de pagos no están desplegados. Para preparar
sus pruebas, pueden usar:

- `FakeDb` es una clase escrita para este taller que pueden usar para sustituir
  la base de datos durante las pruebas. Guarda el inventario, los precios y los
  pedidos en memoria. Está en `tests/support/fake_db.py`.
- Un objeto simulado que devuelve la respuesta que ustedes configuren y permite
  revisar qué llamadas recibió (mock).
- Herramientas que `pytest` prepara y entrega a la prueba (fixtures). Por
  ejemplo, `mocker` permite crear objetos simulados y `requests_mock` permite
  controlar las respuestas HTTP sin llamar al proveedor de pagos.

A los reemplazos de dependencias reales que se usan durante una prueba se les
llama dobles de prueba.

### Ejemplo de uso de FakeDb

Dentro de una prueba que recibe `mocker`, pueden crear una base de datos en
memoria con sus propios datos y pasársela a `OrderService` junto con una
pasarela simulada.

```python
from app.order_service import OrderService
from app.payment_gateway import PaymentGateway
from tests.support.fake_db import FakeDb

# Dentro de la función de prueba:
db = FakeDb(stock={"TAZA": 9}, prices={"TAZA": 7.5})
pasarela = mocker.Mock(spec=PaymentGateway)
servicio = OrderService(db, pasarela)
```

A partir de ahí, configuren la respuesta de la pasarela según el
comportamiento que quieran probar.

## Ejecutar localmente

Desde la raíz del repositorio, con Python 3.13:

```sh
python -m pip install -r requirements.txt
python -m pytest -q
```

Al iniciar hay una prueba resuelta.
```powershell
python -m pytest tests/test_ejemplo_cli.py -q
```
## Probar un pedido desde la terminal

Desde la misma carpeta, ejecuten:

```powershell
python -m app.cli
```
Cuando el programa lo pida, ingresen `CUADERNO`, luego `2` y cualquier
token ficticio. La CLI mostrará un mensaje de error porque el conector lanza
`DatabaseConnectionError` al intentar consultar el inventario. La base de
datos aún no está desplegada y el pedido se detiene antes de llegar al cobro.
El cliente de la pasarela está implementado, pero el servicio externo de pagos
tampoco está disponible para el taller.

En `app/cli.py`, la función `main()` lee los datos con `input()` y llama a
`run_order()`, que usa el método `place_order()` para procesar el pedido.
En la prueba resuelta, las entradas ya están preparadas y pytest comprueba
el mensaje automáticamente.

## Cuatro pruebas de integración

Diseñen **cuatro pruebas nuevas de integración** para OrderSystem. El equipo
elige los componentes que va a integrar, las reglas que quiere comprobar, los
datos, qué dependencias van a sustituir y qué resultados van a comprobar. Conserven el ejemplo de la CLI como material
de consulta. Con el ejemplo, la suite tendrá **cinco pruebas en total**.

Para cada prueba nueva, indiquen si pertenece a un recorrido **de arriba hacia abajo (top-down)** o
**de abajo hacia arriba (bottom-up)** y justifiquen su decisión. Identifiquen desde qué capa empezaron,
qué componente real incorporaron y qué dependencias sustituyeron. Pueden usar
una sola estrategia para las cuatro pruebas o combinar ambas.

## Archivos que deben entregar

**No modifiquen, agreguen ni eliminen archivos en `app/`.** Escriban
sus pruebas en `tests/` y configuren allí los reemplazos de dependencias
(mocks), como se muestra en `tests/test_ejemplo_cli.py`. Si necesitan
simular la base de datos, pueden usar el `FakeDb` que ya viene en la plantilla.
Si quieren incluir PaymentGateway real en la prueba, pueden usar requests_mock para simular la respuesta HTTP del proveedor externo. Así se ejecuta el código real de la pasarela sin contactar al proveedor.

Agreguen las cuatro pruebas nuevas únicamente en `tests/`. Cada integrante
responsable de una prueba debe crear su propio archivo con el formato
`test_<inicial del nombre><primer apellido>.py`. Por ejemplo, Angela Carrera usaría `tests/test_acarrera.py`.

El integrante responsable de GitHub Actions debe usar la misma convención:
`.github/workflows/ci_<inicial del nombre><primer apellido>.yml`. Por ejemplo,
`.github/workflows/ci_acarrera.yml`.

## Responsabilidades del equipo

| Integrante | Responsabilidad |
|---|---|
| 1 | Diseña, implementa y documenta la prueba de integración 1. |
| 2 | Diseña, implementa y documenta la prueba de integración 2. |
| 3 | Diseña, implementa y documenta la prueba de integración 3. |
| 4 | Diseña, implementa y documenta la prueba de integración 4. |
| 5 | Configura GitHub Actions, comprueba que se ejecuten las cinco pruebas y guarda el enlace de esa ejecución. |

Acuerden en equipo qué va a demostrar cada prueba antes de escribirla. Reserven
los últimos 20 minutos para ejecutar la suite en GitHub y preparar la entrega.

## CI y entrega

Escriban el workflow en `.github/workflows/` con el nombre indicado arriba que instale las dependencias y
ejecute la suite completa con `pytest` cada vez que se haga push a `main`.
Consulten la [documentación de GitHub Actions sobre el evento push](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#push).

Registren el resultado de cada prueba. Si pasa (`PASSED`), indiquen qué comportamiento confirmó. Si falla (`FAILED`), expliquen brevemente qué esperaban, qué ocurrió y qué muestra el registro sobre la causa del fallo.

En el repositorio, abran **Actions**, seleccionen la ejecución del commit que
quieren revisar y abran el trabajo que ejecuta pytest. Busquen en el paso de
pytest qué pruebas pasaron o fallaron. Copien la URL de la ejecución del último commit en `main`.

Entreguen el enlace al repositorio con las cuatro pruebas nuevas y el workflow. En la
entrega escrita:

- Indiquen, para cada prueba, su clasificación, la justificación, los componentes reales y las dependencias que sustituyeron.
- Incluyan el enlace directo a la ejecución en GitHub Actions. El registro de pytest debe mostrar el resultado de las cinco pruebas. Se aceptan ejecuciones verdes o rojas si las pruebas llegaron a ejecutarse y el equipo explica su resultado.
