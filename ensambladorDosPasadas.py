import re
# Constantes globales
REGISTROS_32 = {
    'EAX': 0b000,
    'ECX': 0b001,
    'EDX': 0b010,
    'EBX': 0b011,
}

class EnsambladorIA32:
    def __init__(self):
        self.tabla_simbolos = {}  # {simbolo: direccion}
        self.referencias_pendientes = {}  # {simbolo: [lista de direcciones]}
        self.codigo_hex = []  # Lista de bytes en hex
        self.contador_posicion = 0  # Location counter

    def ensamblar(self, archivo_entrada):
        with open(archivo_entrada, 'r') as f:
            lineas = f.readlines()
        for linea in lineas:
            self.procesar_linea(linea)
        # Resolver las referencias pendientes
        self.resolver_referencias_pendientes()
        # Generar los archivos de salida
        self.generar_tabla_simbolos()
        self.generar_referencias_pendientes()
    def resolver_referencias_pendientes(self):
    # Resuelve las referencias pendientes, es decir, actualiza los saltos a etiquetas
        for simbolo, direcciones in self.referencias_pendientes.items():
            if simbolo in self.tabla_simbolos:
                # Obtener la dirección de la etiqueta
                direccion_etiqueta = self.tabla_simbolos[simbolo]
                # Actualizar las direcciones pendientes
                for pos in direcciones:
                    # Calcular el desplazamiento de la etiqueta
                    desplazamiento = direccion_etiqueta - pos - 5  # 1 byte de opcode + 4 bytes de desplazamiento
                    # Reemplazar el código hexadecimal en la posición correcta
                    self.codigo_hex[pos + 1] = desplazamiento & 0xFF  # Solo el byte de desplazamiento

                print(f"Resuelto salto a '{simbolo}' con dirección {direccion_etiqueta:04X}")
            else:
                print(f"Error: La etiqueta '{simbolo}' no está definida.")

    def procesar_linea(self, linea):
        # Eliminar comentarios usando expresión regular y quitar espacios
        linea = re.sub(r';.*', '', linea).strip()  # Elimina todo después de ';'
        if not linea:  # Si la línea está vacía después de eliminar comentarios, la ignoramos
            return
        if linea.endswith(':'):  # Si es una etiqueta, procesarla
            etiqueta = linea[:-1].strip()
            self.procesar_etiqueta(etiqueta)
            return
        # Sino, es instrucción
        self.procesar_instruccion(linea)

    def procesar_etiqueta(self, etiqueta):
        if etiqueta in self.tabla_simbolos:
            print(f"Error: etiqueta {etiqueta} duplicada")
        else:
            self.tabla_simbolos[etiqueta] = self.contador_posicion
            print(f"Etiqueta {etiqueta} definida en {self.contador_posicion:04X}")

    def procesar_instruccion(self, instruccion):
        partes = instruccion.split(None, 1)
        if len(partes) != 2:
            print(f"Error: instrucción mal formada '{instruccion}'")
            return
        mnemonico = partes[0].upper()
        operandos = partes[1].split(',')
        # Limpiar operandos
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
            self.contador_posicion += 2  # Temporal   
            
    def generar_mov(self, operandos):
        if len(operandos) != 2:
            print("Error: MOV requiere 2 operandos")
            return
        dest, src = operandos
        
        # Registro a registro
        if dest in REGISTROS_32 and src in REGISTROS_32:
            opcode = 0x89  # MOV reg to reg
            mod = 0b11     # modo registro a registro
            reg = REGISTROS_32[src]   # registro fuente (reg field)
            rm = REGISTROS_32[dest]   # registro destino (r/m field)

            # Byte ModR/M: mod (2 bits) | reg (3 bits) | r/m (3 bits)
            modrm = (mod << 6) | (reg << 3) | rm

            self.codigo_hex.append(opcode)
            self.codigo_hex.append(modrm)

            print(f"Generado MOV reg,reg: opcode {opcode:02X} modrm {modrm:02X}")
            self.contador_posicion += 2
            return

        # Inmediato a registro (ejemplo MOV EAX, 10)
        if dest in REGISTROS_32:
            try:
                valor_inmediato = int(src, 0)  # Detecta decimal, hex (0x), etc.
            except ValueError:
                print(f"Error: valor inmediato inválido '{src}'")
                return

            opcode = 0xB8 + REGISTROS_32[dest]  # Opcode MOV reg32, imm32 empieza en B8
            self.codigo_hex.append(opcode)

            # El inmediato es de 32 bits, little endian
            for i in range(4):
                self.codigo_hex.append((valor_inmediato >> (8 * i)) & 0xFF)

            print(f"Generado MOV reg,imm: opcode {opcode:02X} imm {valor_inmediato}")
            self.contador_posicion += 5  # 1 byte opcode + 4 bytes inmediato
            return

        print("Error: modo de direccionamiento no soportado o mal operandos")
    
    def generar_add(self, operandos):
        if len(operandos) != 2:
            print("Error: ADD requiere 2 operandos")
            return

        dest, src = operandos

        # Registro a registro
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

        # Inmediato a registro
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

        # Registro a registro
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

        # Inmediato a registro
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

        # Registro a registro
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

        # Inmediato a registro
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

    # Mostrar código generado en hexadecimal
    print("Código máquina generado:")
    print(" ".join(f"{byte:02X}" for byte in ensamblador.codigo_hex))