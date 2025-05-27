# Ensamblador IA-32 (x86, 32 bits)

Este proyecto implementa un ensamblador básico en Python para la arquitectura IA-32 (x86, 32 bits). El ensamblador realiza el proceso en **una sola pasada** y genera:

- Código máquina en hexadecimal (`programa.hex`)
- Tabla de símbolos (`simbolos.txt`)
- Tabla de referencias pendientes (`referencias.txt`)

## 📦 Requisitos

- Python 3.6 o superior

## ⚙️ Instrucciones soportadas

| Instrucción | Sintaxis       | Opcode     |
|------------|----------------|------------|
| `MOV`      | `MOV dest, src`| 88–8B      |
| `ADD`      | `ADD dest, src`| 00–03      |
| `SUB`      | `SUB dest, src`| 28–2B      |
| `JMP`      | `JMP etiqueta` | E9         |
| `CMP`      | `CMP op1, op2` | 38–3B      |
| `JE`       | `JE etiqueta`  | 74         |
| `JNE`      | `JNE etiqueta` | 75         |

### Modos de direccionamiento:

- Registro a registro
- Inmediato a registro
- Memoria a registro (mediante etiquetas)

## 🚀 Uso

1. Coloca tu código ensamblador en `programa.asm`.
2. Ejecuta:

```bash
python ensamblador.py
```

3. Se generarán los siguientes archivos:
   - `programa.hex`: Código máquina en formato hexadecimal
   - `simbolos.txt`: Tabla de símbolos
   - `referencias.txt`: Tabla de referencias pendientes

## 📁 Estructura del repositorio

```
ensamblador-ia32/
├── ensamblador.py
├── programa.asm
├── programa.hex         # Generado
├── simbolos.txt         # Generado
├── referencias.txt      # Generado
├── README.md
└── .gitignore
```

## ✍️ Autor

Este proyecto fue desarrollado como parte de un ejercicio académico sobre ensambladores y arquitectura IA-32.
