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

    def procesar_linea(self, linea):
        # Limpiar linea (quitar comentarios y espacios)
        linea = linea.strip()
        if not linea or linea.startswith(';'):  # Línea vacía o comentario
            return

        # Detectar etiqueta (termina en ':')
        if linea.endswith(':'):
            etiqueta = linea[:-1].strip()
            self.procesar_etiqueta(etiqueta)
            return

        # Si no es etiqueta, debe ser instrucción
        self.procesar_instruccion(linea)

    def procesar_etiqueta(self, etiqueta):
        if etiqueta in self.tabla_simbolos:
            print(f"Error: etiqueta {etiqueta} duplicada")
        else:
            self.tabla_simbolos[etiqueta] = self.contador_posicion
            print(f"Etiqueta {etiqueta} definida en {self.contador_posicion:04X}")

    def procesar_instruccion(self, instruccion):
        # Por ahora solo imprimir para verificar
        print(f"Procesando instrucción en {self.contador_posicion:04X}: {instruccion}")
        # Aquí luego iría la lógica para parsear instrucción y generar código hex
        # Actualizamos el contador_posicion simulando 2 bytes por instrucción (solo para ejemplo)
        self.contador_posicion += 2
