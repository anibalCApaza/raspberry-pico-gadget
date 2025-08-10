import subprocess
import os
import sys
import time

from typing import Callable
from rich.progress import track

local_file = "main.py"
pico_file = ":main.py"
pico_port = "COM5"

copy_command = ["mpremote", "cp", local_file, pico_file]
reset_command = ["mpremote", "reset"]
connect_command = ["mpremote", "connect", pico_port]


def generate_progress_bar(callback: Callable[[], None]):
    for _ in track(range(20)):
        time.sleep(0.02)
    callback()


def upload_script() -> None:
    """
    Copia el archivo main.py a la Raspberry Pi Pico, reinicia y se conecta al mismo para visualizar mensajes de salida.
    """

    # --- Paso 1: Copiar el archivo ---
    print(f"Copiando '{local_file}' a la Raspberry Pi Pico...")

    # Verifica si el archivo local existe.
    if not os.path.exists(local_file):
        print(f"Error: El archivo '{local_file}' no se encontró.")
        sys.exit(1)

    try:
        subprocess.run(copy_command, check=True, text=False)
        print("¡Archivo copiado con éxito! 🎉")

    except subprocess.CalledProcessError as e:
        print("Error al ejecutar mpremote para copiar el archivo:")
        print(f"Código de salida: {e.returncode}")
        print(f"Salida del error: {e.stderr}")
        return
    except FileNotFoundError:
        print("Error: No se pudo encontrar 'mpremote'.")
        print("Asegúrate de que 'mpremote' esté instalado y en tu PATH.")
        return


def reset_microcontroller() -> None:
    # --- Paso 2: Reiniciar la Pico ---
    print("Reiniciando la Raspberry Pi Pico para ejecutar el nuevo código...")
    try:
        subprocess.run(reset_command, check=True, text=True)
        print("¡Reinicio completado! El nuevo código ya está en marcha. ✨")

    except subprocess.CalledProcessError as e:
        print("Error al ejecutar mpremote para reiniciar la Pico:")
        print(f"Código de salida: {e.returncode}")
        print(f"Salida del error: {e.stderr}")
    except FileNotFoundError:
        print("Error: No se pudo encontrar 'mpremote'.")
        print("Asegúrate de que 'mpremote' esté instalado y en tu PATH.")


def connect_to_microcontroller() -> None:
    # --- Paso 3: Conectarse a la Pico ---
    print(f"Conectándose a la Pico a través de {pico_port}...")
    try:
        time.sleep(1)
        subprocess.run(connect_command)
    except FileNotFoundError:
        print("Error: 'mpremote' no se encontró. ¿Está instalado?")
        return


def deploy_to_pico():
    generate_progress_bar(upload_script)
    generate_progress_bar(reset_microcontroller)
    generate_progress_bar(connect_to_microcontroller)


if __name__ == "__main__":
    deploy_to_pico()
