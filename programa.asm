; Programa de prueba para ensamblador IA-32

inicio:
    MOV EAX, EBX      ; Mueve el valor de EBX a EAX
    ADD EAX, 10       ; Suma 10 a EAX
    SUB EAX, ECX      ; Resta ECX de EAX
    CMP EAX, ECX      ; Compara EAX con ECX
    JE iguales        ; Salta a 'iguales' si EAX == ECX
    MOV ECX, 0x20     ; Mueve el valor inmediato 0x20 a ECX
    JNE diferentes    ; Salta a 'diferentes' si EAX != ECX
iguales:
    MOV EDX, 0x1      ; Si son iguales, mueve 0x1 a EDX
    JMP fin           ; Salta al final
diferentes:
    MOV EDX, 0x2      ; Si son diferentes, mueve 0x2 a EDX

fin:
    ; Fin del programa
