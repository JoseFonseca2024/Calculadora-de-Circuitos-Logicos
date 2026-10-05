# Calculadora de Simplificación de Circuitos Lógicos

Aplicación de escritorio para Windows desarrollada en Python 3.12+, PySide6, SymPy y Matplotlib.

## Características

- Aplicación 100% local y gráfica.
- Interfaz de escritorio desarrollada con PySide6.
- Configuración del número de entradas de 2 a 6.
- Nombres de entradas mediante:
  - A, B, C, D...
  - X1, X2, X3...
  - Nombres personalizados.
- Entrada por expresión booleana.
- Entrada por minterms `Σm(1,3,5,7)`.
- Tabla de verdad.
- Simplificación lógica mediante SymPy.
- Procedimiento educativo de álgebra booleana.
- Mapa de Karnaugh para hasta 4 variables.
- Orden Gray para filas y columnas del mapa.
- Agrupaciones de Karnaugh representadas visualmente mediante círculos.
- Representación de grupos que cruzan los bordes del mapa.
- Verificación automática de equivalencia entre la función original y la simplificada.
- Exportación del procedimiento a TXT y PDF.
- Guardado del mapa de Karnaugh como PNG.
- Interfaz adaptable al tamaño de la ventana.
- Preparada para compilación mediante PyInstaller.

## Estructura del procesamiento

La aplicación sigue el flujo:

```text
FUNCIÓN ORIGINAL
       ↓
TABLA DE VERDAD
       ↓
SIMPLIFICACIÓN
       ↓
ÁLGEBRA DE BOOLE
       ↓
MAPA DE KARNAUGH
       ↓
AGRUPACIONES
       ↓
FUNCIÓN SIMPLIFICADA
       ↓
VERIFICACIÓN