import re

REGISTROS_32 = {
    'EAX': 0b000,
    'ECX': 0b001,
    'EDX': 0b010,
    'EBX': 0b011,
}

class EnsambladorIA32:
    def __init__(self):
        self.tabla_simbolos = {}  # {simbolo: direccion}
        self.referencias_pendientes = {}  # {simbolo: [lista de posiciones donde se usa]}
        self.codigo_hex = []  # Lista de bytes en hexadecimal
        self.contador_posicion = 0  # Contador de posición (location counter)

    def ensamblar(self, archivo_entrada):
        with open(archivo_entrada, 'r') as f:
            lineas = f.readlines()

        # Procesamos todo en una sola pasada
        for linea in lineas:
            self.procesar_linea(linea)

        # Resolver las referencias pendientes después de procesar todo el código
        self.resolver_referencias_pendientes()

        # Generar los archivos de salida
        self.generar_tabla_simbolos()
        self.generar_referencias_pendientes()

    def procesar_linea(self, linea):
        # Eliminar comentarios y espacios
        linea = re.sub(r';.*', '', linea).strip()  
        if not linea:
            return
        if linea.endswith(':'):  # Si es una etiqueta, registrarla
            etiqueta = linea[:-1].strip()
            self.procesar_etiqueta(etiqueta)
            return
        # Sino, es instrucción
        self.procesar_instruccion(linea)

    def procesar_etiqueta(self, etiqueta):
        if etiqueta in self.tabla_simbolos:
            print(f"Error: etiqueta duplicada '{etiqueta}'")
        else:
            self.tabla_simbolos[etiqueta] = self.contador_posicion
            print(f"Etiqueta '{etiqueta}' definida en {self.contador_posicion:04X}")

    def procesar_instruccion(self, instruccion):
        partes = instruccion.split(None, 1)
        if len(partes) != 2:
            print(f"Error: instrucción mal formada '{instruccion}'")
            return
        mnemonico = partes[0].upper()
        operandos = partes[1].split(',')
        operandos = [op.strip().upper() for op in operandos]

        if mnemonico == 'MOV':
            self.generar_mov(operandos)
        elif mnemonico == 'ADD':
            self.generar_add(operandos)
        elif mnemonico == 'SUB':
            self.generar_sub(operandos)
        elif mnemonico == 'CMP':
            self.generar_cmp(operandos)
        elif mnemonico == 'JMP':
            self.generar_jmp(operandos[0])
        elif mnemonico == 'JE':
            self.generar_je(operandos[0])
        elif mnemonico == 'JNE':
            self.generar_jne(operandos[0])
        else:
            print(f"Instrucción '{mnemonico}' no implementada aún")
            self.contador_posicion += 2

    def generar_mov(self, operandos):
        if len(operandos) != 2:
            print("Error: MOV requiere 2 operandos")
            return
        dest, src = operandos

        if dest in REGISTROS_32 and src in REGISTROS_32:
            opcode = 0x89
            mod = 0b11
            reg = REGISTROS_32[src]
            rm = REGISTROS_32[dest]
            modrm = (mod << 6) | (reg << 3) | rm

            self.codigo_hex.append(opcode)
            self.codigo_hex.append(modrm)
            print(f"Generado MOV reg,reg: opcode {opcode:02X} modrm {modrm:02X}")
            self.contador_posicion += 2
            return

        if dest in REGISTROS_32:
            try:
                valor_inmediato = int(src, 0)
            except ValueError:
                print(f"Error: valor inmediato inválido '{src}'")
                return

            opcode = 0xB8 + REGISTROS_32[dest]
            self.codigo_hex.append(opcode)
            for i in range(4):
                self.codigo_hex.append((valor_inmediato >> (8 * i)) & 0xFF)
            print(f"Generado MOV reg,imm: opcode {opcode:02X} imm {valor_inmediato}")
            self.contador_posicion += 5
            return

        print("Error: modo de direccionamiento no soportado o mal operandos")

    def generar_add(self, operandos):
        if len(operandos) != 2:
            print("Error: ADD requiere 2 operandos")
            return

        dest, src = operandos

        if dest in REGISTROS_32 and src in REGISTROS_32:
            opcode = 0x01
            mod = 0b11
            reg = REGISTROS_32[src]
            rm = REGISTROS_32[dest]
            modrm = (mod << 6) | (reg << 3) | rm

            self.codigo_hex.append(opcode)
            self.codigo_hex.append(modrm)
            print(f"Generado ADD reg,reg: opcode {opcode:02X} modrm {modrm:02X}")
            self.contador_posicion += 2
            return

        if dest in REGISTROS_32:
            try:
                valor_inmediato = int(src, 0)
            except ValueError:
                print(f"Error: valor inmediato inválido '{src}'")
                return

            opcode = 0x81
            mod = 0b11
            reg = 0b000
            rm = REGISTROS_32[dest]
            modrm = (mod << 6) | (reg << 3) | rm

            self.codigo_hex.append(opcode)
            self.codigo_hex.append(modrm)
            for i in range(4):
                self.codigo_hex.append((valor_inmediato >> (8 * i)) & 0xFF)
            print(f"Generado ADD reg,imm: opcode {opcode:02X} modrm {modrm:02X} imm {valor_inmediato}")
            self.contador_posicion += 6
            return

        print("Error: modo de direccionamiento no soportado o mal operandos")

    def generar_sub(self, operandos):
        if len(operandos) != 2:
            print("Error: SUB requiere 2 operandos")
            return

        dest, src = operandos

        if dest in REGISTROS_32 and src in REGISTROS_32:
            opcode = 0x29
            mod = 0b11
            reg = REGISTROS_32[src]
            rm = REGISTROS_32[dest]
            modrm = (mod << 6) | (reg << 3) | rm

            self.codigo_hex.append(opcode)
            self.codigo_hex.append(modrm)
            print(f"Generado SUB reg,reg: opcode {opcode:02X} modrm {modrm:02X}")
            self.contador_posicion += 2
            return

        if dest in REGISTROS_32:
            try:
                valor_inmediato = int(src, 0)
            except ValueError:
                print(f"Error: valor inmediato inválido '{src}'")
                return

            opcode = 0x81
            mod = 0b11
            reg = 0b101
            rm = REGISTROS_32[dest]
            modrm = (mod << 6) | (reg << 3) | rm

            self.codigo_hex.append(opcode)
            self.codigo_hex.append(modrm)
            for i in range(4):
                self.codigo_hex.append((valor_inmediato >> (8 * i)) & 0xFF)
            print(f"Generado SUB reg,imm: opcode {opcode:02X} modrm {modrm:02X} imm {valor_inmediato}")
            self.contador_posicion += 6
            return

        print("Error: modo de direccionamiento no soportado o mal operandos")

    def generar_cmp(self, operandos):
        if len(operandos) != 2:
            print("Error: CMP requiere 2 operandos")
            return

        dest, src = operandos

        if dest in REGISTROS_32 and src in REGISTROS_32:
            opcode = 0x39
            mod = 0b11
            reg = REGISTROS_32[src]
            rm = REGISTROS_32[dest]
            modrm = (mod << 6) | (reg << 3) | rm

            self.codigo_hex.append(opcode)
            self.codigo_hex.append(modrm)
            print(f"Generado CMP reg,reg: opcode {opcode:02X} modrm {modrm:02X}")
            self.contador_posicion += 2
            return

        if dest in REGISTROS_32:
            try:
                valor_inmediato = int(src, 0)
            except ValueError:
                print(f"Error: valor inmediato inválido '{src}'")
                return

            opcode = 0x81
            mod = 0b11
            reg = 0b111  # /7 en ModR/M para CMP
            rm = REGISTROS_32[dest]
            modrm = (mod << 6) | (reg << 3) | rm

            self.codigo_hex.append(opcode)
            self.codigo_hex.append(modrm)
            for i in range(4):
                self.codigo_hex.append((valor_inmediato >> (8 * i)) & 0xFF)
            print(f"Generado CMP reg,imm: opcode {opcode:02X} modrm {modrm:02X} imm {valor_inmediato}")
            self.contador_posicion += 6
            return

        print("Error: modo de direccionamiento no soportado o mal operandos")

    def generar_jmp(self, etiqueta):
        if etiqueta not in self.tabla_simbolos:
            print(f"Error: Etiqueta '{etiqueta}' no definida.")
            self.referencias_pendientes[etiqueta] = self.referencias_pendientes.get(etiqueta, [])
            self.referencias_pendientes[etiqueta].append(self.contador_posicion)
            return

        desplazamiento = self.tabla_simbolos[etiqueta] - self.contador_posicion - 5
        self.codigo_hex.append(0xE9)
        for i in range(4):
            self.codigo_hex.append((desplazamiento >> (8 * i)) & 0xFF)
    
        print(f"Generado JMP a {etiqueta} con desplazamiento {desplazamiento}")
        self.contador_posicion += 5

    def generar_je(self, etiqueta):
        self.generar_condicional(0x74, etiqueta)

    def generar_jne(self, etiqueta):
        self.generar_condicional(0x75, etiqueta)

    def generar_condicional(self, opcode, etiqueta):
        if etiqueta not in self.tabla_simbolos:
            print(f"Error: Etiqueta '{etiqueta}' no definida.")
            self.referencias_pendientes[etiqueta] = self.referencias_pendientes.get(etiqueta, [])
            self.referencias_pendientes[etiqueta].append(self.contador_posicion)
            return

        desplazamiento = self.tabla_simbolos[etiqueta] - self.contador_posicion - 2
        self.codigo_hex.append(opcode)
        self.codigo_hex.append(desplazamiento & 0xFF)

        print(f"Generado salto condicional {hex(opcode)} a {etiqueta} con desplazamiento {desplazamiento}")
        self.contador_posicion += 2

    def resolver_referencias_pendientes(self):
        for simbolo, direcciones in self.referencias_pendientes.items():
            if simbolo in self.tabla_simbolos:
                direccion_etiqueta = self.tabla_simbolos[simbolo]
                for pos in direcciones:
                    desplazamiento = direccion_etiqueta - pos - 5  # 1 byte de opcode + 4 bytes de desplazamiento
                    self.codigo_hex[pos + 1] = desplazamiento & 0xFF
                print(f"Resuelto salto a '{simbolo}' con dirección {direccion_etiqueta:04X}")
            else:
                print(f"Error: La etiqueta '{simbolo}' no está definida.")

    def generar_tabla_simbolos(self):
        with open('simbolos.txt', 'w') as f:
            for simbolo, direccion in self.tabla_simbolos.items():
                f.write(f"{simbolo}: {direccion:04X}\n")

    def generar_referencias_pendientes(self):
        with open('referencias.txt', 'w') as f:
            for simbolo, direcciones in self.referencias_pendientes.items():
                f.write(f"{simbolo}: {', '.join(hex(d) for d in direcciones)}\n")


if __name__ == "__main__":
    ensamblador = EnsambladorIA32()
    ensamblador.ensamblar("programa.asm")

    print("\nCódigo máquina generado:")
    print(" ".join(f"{byte:02X}" for byte in ensamblador.codigo_hex))

