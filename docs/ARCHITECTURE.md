# Arquitectura

Autrexs separa interfaz, lógica temporal y formato. La interfaz usa HTML y CSS nativos; la lógica usa módulos ES; `Intl.DateTimeFormat` localiza fecha y hora, y `performance.now()` mide intervalos. Las preferencias pueden almacenarse localmente. Los módulos experimentales no deben anunciarse como funciones terminadas hasta integrarlos y probarlos.
