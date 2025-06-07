[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/3l5uE2JZ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19627061&assignment_repo_type=AssignmentRepo)

# Proyecto Final: Ensamblador Básico IA-32 (x86) de 32 bits

## Descripción

Este proyecto consiste en desarrollar un ensamblador básico para arquitectura IA-32 (x86) de 32 bits que realice el proceso de ensamblado en una sola pasada. El ensamblador debe leer código fuente en lenguaje ensamblador, generar la tabla de símbolos, resolver referencias pendientes y producir el código máquina en formato hexadecimal.

### Funcionalidades principales

- Soporte para instrucciones básicas: `MOV`, `ADD`, `SUB`, `JMP`, `CMP`, `JE`, `JNE`.
- Manejo de modos de direccionamiento: registro a registro, inmediato a registro, memoria a registro (con etiquetas simples).
- Generación automática de:
  - Tabla de símbolos (etiquetas y direcciones).
  - Tabla de referencias pendientes (saltos a etiquetas definidas posteriormente).
  - Código máquina en hexadecimal.
- Generación de archivos de salida que incluyen el código máquina y reportes de las tablas.

## Requisitos

- Python 3.6 o superior.
- Conocimientos básicos de arquitectura IA-32 y conjunto de instrucciones.
- Manejo de estructuras de datos en Python.

## Integrantes

- Guadalupe Isabela De la Fuente Flores
- Laura Isabel Hernández Castro
- Pérez Carmona José Bruno
- Martínez Rosales Hugo Armando

## Uso

1. Preparar un archivo de código ensamblador con extensión `.asm` con instrucciones soportadas.
2. Ejecutar el ensamblador con Python indicando el archivo de entrada.
3. El ensamblador generará:
   - Un archivo `.hex` con el código máquina en formato hexadecimal.
   - Archivos `simbolos.txt` y `referencias.txt` con las tablas generadas.

## Ejemplo de ejecución

```bash
python ensamblador.py programa.asm

