# Ethernet desde Python

En este directorio hay pequeños ejemplos en Python de recepción y envío de paquetes a nivel de enlace.

## Requerimientos

Los ejemplos están implementados para su ejecución en Windows, por lo que debemos instalar lo siguiente.

### winpcapy

Este módulo de Python es un wrapper o intermediario de la librería WinPcap, que permite acceder directamente a los dispositivos de red, saltándonos así las restricciones del sistema operativo.

Instalar `winpcapy`:

```powershell
pip install -y winpcapy
```

Si queremos instalar el módulo `winpcapy` desde el repositorio de código fuente:

```bash
pip install -e git+https://github.com/orweis/winpcapy#egg=winpcapy
```

> En ambos casos, ejecutar como `Administrador`.

Esta última opción es preferible porque hay un error al importar el módulo `winpcapy` (ya que no es compatible con versiones superiores a Python 3.7) solucionado en el código fuente que aún no se ha publicado en [**PiPy**](https://pypi.org/project/WinPcapy/).

### WinPcap

Para poder capturar y enviar paquetes a nivel de enlace en Windows es necesario instalar la librería **WinPcap**, ya que este nivel de red es gestionado por el kernel del sistema operativo.

Para saltarnos esta limitación es posible instalar **WinPcap** mediante Chocolatey como `Administrador`:

```powershell
choco install -y winpcap
```

O podemos descargarlo directamente desde este [enlace](https://www.winpcap.org/).


