# Paquete Python

Autrexs también ofrece una interfaz de terminal ligera, independiente de la aplicación web y sin dependencias de ejecución.

## Instalar desde GitHub

Requisitos: Python 3.10 o superior y Git instalado.

```bash
python -m pip install "git+https://github.com/programador777lolxddd-dot/Autrexs.git"
```

En algunos sistemas puede ser necesario usar `python3 -m pip`.

## Usar

```bash
autrexs
autrexs now
autrexs now --12h
autrexs now --no-seconds
autrexs count 90
autrexs --version
```

## Instalar desde una copia local

```bash
python -m pip install .
```

El paquete de terminal no sustituye ni empaqueta el reloj web; ambos forman parte del mismo repositorio.
