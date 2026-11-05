import os
import sys

from limpiar_pantalla import limpiar_pantalla


def _leer_clave(mensaje):
    sys.stdout.write(mensaje)
    sys.stdout.flush()
    caracteres = []

    if os.name == "nt":
        import msvcrt

        while True:
            caracter = msvcrt.getwch()
            if caracter in ("\r", "\n"):
                break
            if caracter == "\003":
                raise KeyboardInterrupt
            if caracter in ("\b", "\x7f"):
                if caracteres:
                    caracteres.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            elif caracter in ("\x00", "\xe0"):
                msvcrt.getwch()
            else:
                caracteres.append(caracter)
                sys.stdout.write("*")
                sys.stdout.flush()
    else:
        import termios
        import tty

        entrada = sys.stdin.fileno()
        ajustes = termios.tcgetattr(entrada)
        try:
            tty.setraw(entrada)
            while True:
                caracter = sys.stdin.read(1)
                if caracter in ("\r", "\n"):
                    break
                if caracter == "\003":
                    raise KeyboardInterrupt
                if caracter in ("\b", "\x7f"):
                    if caracteres:
                        caracteres.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    caracteres.append(caracter)
                    sys.stdout.write("*")
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(entrada, termios.TCSADRAIN, ajustes)

    sys.stdout.write("\n")
    sys.stdout.flush()
    return "".join(caracteres)


def pedir_credenciales(mensaje_nombre, mensaje_clave):
    while True:
        nombre = input(mensaje_nombre).strip()
        clave = _leer_clave(mensaje_clave).strip()
        if nombre == "" or clave == "":
            print("Error: el nombre y la contraseña no pueden estar vacíos.")
            input("Presione Enter para intentarlo de nuevo...")
            limpiar_pantalla()
            continue
        return nombre, clave
