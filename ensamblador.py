class EnsambladorIA32:
    def __init__(self):
        self.tabla_simbolos = {}  # {simbolo: direccion}
        self.referencias_pendientes = {}  # {simbolo: [posiciones]}
        self.codigo_hex = []  # Lista de bytes
        self.contador_posicion = 0  # Location counter

    def ensamblar(self, archivo_entrada):
        with open(archivo_entrada, 'r') as f:
            lineas = f.readlines()

        for linea in lineas:
            self.procesar_linea(linea.strip())

    def procesar_linea(self, linea):
        # Quitar comentarios
        linea = linea.split(';')[0].strip()
        if not linea:
            return

        if ':' in linea:
            etiqueta, *resto = linea.split(':')
            self.procesar_etiqueta(etiqueta.strip())
            if resto:
                self.procesar_linea(':'.join(resto).strip())
        else:
            self.procesar_instruccion(linea)

    def procesar_etiqueta(self, etiqueta):
        self.tabla_simbolos[etiqueta] = self.contador_posicion

    def procesar_instruccion(self, instruccion):
        partes = instruccion.split(None, 1)
        if len(partes) != 2:
            return

        mnem, operandos = partes[0].upper(), partes[1]
        ops = [op.strip().upper() for op in operandos.split(',')]

        if mnem == "MOV" and self.es_registro(ops[0]) and self.es_registro(ops[1]):
            opcode = 0x89
            modrm = self.codificar_modrm(ops[1], ops[0])  # MOV dest, src
            self.codigo_hex.append(opcode)
            self.codigo_hex.append(modrm)
            self.contador_posicion += 2

        elif mnem == "JMP":
            etiqueta = ops[0]
            opcode = 0xE9
            self.codigo_hex.append(opcode)
            pos_disp = self.contador_posicion + 1  # posición del desplazamiento
            self.contador_posicion += 5  # E9 + 4 bytes

            if etiqueta in self.tabla_simbolos:
                offset = self.tabla_simbolos[etiqueta] - self.contador_posicion
                bytes_offset = list(offset.to_bytes(4, 'little', signed=True))
                self.codigo_hex.extend(bytes_offset)
            else:
                self.codigo_hex.extend([0x00, 0x00, 0x00, 0x00])
                self.referencias_pendientes.setdefault(etiqueta, []).append(pos_disp)

    def codificar_modrm(self, reg, rm):
        codigos = {
            'EAX': 0b000, 'ECX': 0b001, 'EDX': 0b010, 'EBX': 0b011,
            'ESP': 0b100, 'EBP': 0b101, 'ESI': 0b110, 'EDI': 0b111
        }
        mod = 0b11
        reg_code = codigos[reg]
        rm_code = codigos[rm]
        return (mod << 6) | (reg_code << 3) | rm_code

    def es_registro(self, op):
        return op in ['EAX', 'EBX', 'ECX', 'EDX', 'ESI', 'EDI', 'EBP', 'ESP']

    def resolver_referencias_pendientes(self):
        for simbolo, posiciones in self.referencias_pendientes.items():
            if simbolo in self.tabla_simbolos:
                dir_final = self.tabla_simbolos[simbolo]
                for pos in posiciones:
                    offset = dir_final - (pos + 4)
                    bytes_offset = list(offset.to_bytes(4, 'little', signed=True))
                    self.codigo_hex[pos:pos+4] = bytes_offset

    def generar_hex(self, archivo_salida):
        with open(archivo_salida, 'w') as f:
            for byte in self.codigo_hex:
                f.write(f"{byte:02X} ")

    def generar_reportes(self):
        with open('simbolos.txt', 'w') as f:
            for simb, dir in self.tabla_simbolos.items():
                f.write(f"{simb}: {dir:04X}\n")
        with open('referencias.txt', 'w') as f:
            for simb, dirs in self.referencias_pendientes.items():
                f.write(f"{simb}: {', '.join(hex(d) for d in dirs)}\n")

# Ejecución
if __name__ == "__main__":
    ensamblador = EnsambladorIA32()
    ensamblador.ensamblar('programa.asm')
    ensamblador.resolver_referencias_pendientes()
    ensamblador.generar_hex('programa.hex')
    ensamblador.generar_reportes()