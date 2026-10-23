# Autrexs

```text
    _         _                  __
   / \  _   _| |_ _ __ _____  __/ _|
  / _ \| | | | __| '__/ _ \ \/ / |_
 / ___ \ |_| | |_| | | (_) >  <|  _|
/_/   \_\\__,_|\__|_|  \___/_/\\_\_|
```

**Un reloj moderno, ligero y extensible.**

Autrexs es un proyecto experimental de reloj avanzado. La meta es combinar una interfaz clara con módulos de tiempo fáciles de revisar, probar y ampliar.

> **Estado:** desarrollo inicial. El reloj local y el cronómetro básico están en la interfaz. Temporizador, alarmas, preferencias y reloj mundial siguen siendo módulos experimentales o funciones pendientes de integración.

## ✦ Funciones actuales

- Reloj local con actualización en tiempo real.
- Fecha localizada en español.
- Cronómetro con iniciar, pausar, continuar, reiniciar y vueltas.
- Interfaz adaptable con estética oscura azul/violeta.
- Sin API ni backend para las funciones locales.
- Pruebas de lógica y flujo de calidad en GitHub Actions.

## ▶ Ejecutar

Los módulos JavaScript pueden bloquearse al abrir la página con `file://`. Desde la raíz del repositorio, ejecuta:

```bash
python3 -m http.server 8000
```

Después abre [http://localhost:8000/autrexs/](http://localhost:8000/autrexs/).

También puedes usar cualquier servidor estático que sirva módulos ES correctamente.

## 🧪 Pruebas

Necesitas Node.js 20 o superior:

```bash
npm test
npm run check
```

O ejecuta directamente `node --test tests/*.test.js`.

## 🗂️ Estructura

| Ruta | Propósito |
|---|---|
| `autrexs/` | Interfaz web y módulos JavaScript |
| `assets/` | Favicon y recursos visuales |
| `docs/` | Arquitectura, guía, hoja de ruta y limitaciones |
| `tests/` | Pruebas automatizadas y listas manuales |
| `examples/` | Ejemplos de los módulos experimentales |
| `scripts/` | Verificaciones de mantenimiento |
| `.github/` | CI y plantillas para contribuciones |

## 🧭 Hoja de ruta

1. Consolidar las pruebas y la accesibilidad de la versión inicial.
2. Integrar un temporizador con controles y avisos dentro de la página.
3. Añadir preferencias de formato y tema.
4. Diseñar alarmas con límites claros sobre permisos y segundo plano.
5. Añadir relojes mundiales y más pruebas.

Consulta [docs/ROADMAP.md](docs/ROADMAP.md) y [docs/FEATURES.md](docs/FEATURES.md). Las casillas pendientes son planes, no funciones completas.

## 🤝 Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md), revisa [el modelo de seguridad](docs/SECURITY_MODEL.md) y añade pruebas cuando cambies lógica. Los errores se pueden reportar con la plantilla de [bug](.github/ISSUE_TEMPLATE/bug_report.md).

## 🔒 Seguridad y privacidad

No publiques claves API, tokens ni datos personales. La interfaz base muestra la hora del dispositivo y no necesita cuenta ni servicio remoto. Más detalles en [SECURITY.md](SECURITY.md) y [docs/PRIVACY.md](docs/PRIVACY.md).

## 📄 Licencia

El proyecto todavía no tiene una licencia de reutilización seleccionada por el autor. Consulta [LICENSE](LICENSE) antes de redistribuir o reutilizar el código.

---

**Autrexs — el tiempo, con otra perspectiva.**
