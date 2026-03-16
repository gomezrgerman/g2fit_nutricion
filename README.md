# G2Fit Nutrición - Sistema de Automatización de Dietas

Sistema automatizado que genera planes nutricionales personalizados de 28 días usando n8n, Supabase y Claude AI.

## Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `workflow.json` | Workflow n8n completo (31 nodos) |
| `supabase-schema.sql` | Schema SQL de la base de datos |
| `generar_pdf_dieta.py` | Script Python generador de PDF |
| `.env.example` | Plantilla de variables de entorno |

## Requisitos previos

- n8n (self-hosted o cloud) ≥ 1.0
- Supabase (proyecto activo)
- Python 3.8+ con `reportlab` y `pillow`
- Cuenta Anthropic API (Claude)
- Gmail con OAuth2 configurado
- Bot de Telegram (o Slack)
- Integración de Notion (opcional)

## Instalación paso a paso

### 1. Base de datos Supabase

1. Ve a **SQL Editor** en tu proyecto Supabase
2. Ejecuta el contenido de `supabase-schema.sql`
3. Verifica que las 4 tablas se hayan creado correctamente:
   - `clientes`
   - `recetas`
   - `dietas_generadas`
   - `logs_generacion`
4. Copia tu **Project URL** y **Service Role Key** desde *Settings → API*

### 2. Script Python

```bash
# En el servidor donde corre n8n
pip install reportlab pillow

# Copiar el script
sudo mkdir -p /opt/scripts
sudo cp generar_pdf_dieta.py /opt/scripts/
sudo chmod +x /opt/scripts/generar_pdf_dieta.py

# Crear directorio para PDFs
sudo mkdir -p /home/pdfs
sudo chmod 777 /home/pdfs

# Probar el script
python3 /opt/scripts/generar_pdf_dieta.py '{"cliente":{"nombre":"Test"}}' '/tmp/test.pdf'
```

### 3. Credenciales en n8n

En n8n ve a **Settings → Credentials** y crea:

| Nombre | Tipo | Configuración |
|---|---|---|
| `Supabase G2Fit` | Supabase API | URL + Service Role Key |
| `Gmail G2Fit` | Gmail OAuth2 | Sigue el flujo OAuth |
| `Telegram G2Fit` | Telegram API | Bot Token |

### 4. Variables de entorno en n8n

En `Settings → Environment Variables` o en tu archivo `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_CHAT_ID=-100...
NOTION_INTEGRATION_TOKEN=secret_...
NOTION_DATABASE_ID=uuid...
NUTRICIONISTA_NOMBRE=Nombre Apellido
NUTRICIONISTA_EMAIL=email@tudominio.com
NUTRICIONISTA_NUM_COLEGIADO=CO-XXXXX
```

### 5. Importar workflow en n8n

1. Ve a **Workflows → Import from File**
2. Selecciona `workflow.json`
3. Una vez importado, actualiza los IDs de credenciales en cada nodo que las use:
   - Todos los nodos `Supabase` → `Supabase G2Fit`
   - Todos los nodos `Gmail` → `Gmail G2Fit`
   - Todos los nodos `Telegram` → `Telegram G2Fit`
4. Activa el workflow con el toggle

### 6. Configurar Notion (opcional)

1. Crea una integración en [notion.so/my-integrations](https://notion.so/my-integrations)
2. Crea una base de datos con las propiedades: `Nombre`, `Email`, `Estado`, `Requiere Revisión`, `Motivo Revisión`, `PDF URL`, `Dieta ID`, `Fecha Generación`
3. Comparte la base de datos con tu integración
4. Copia el `database_id` de la URL de la base de datos

## Arquitectura del workflow

```
Webhook POST /nueva-solicitud-dieta
    ↓
Normalizar datos (Set)
    ↓
Calcular macros TMB/TDEE/IMC (Code)
    ↓ ↓ (paralelo)
Insertar cliente (Supabase)  |  Consultar recetas (Supabase)
    ↓ (merge)
Construir prompt Claude (Code)
    ↓
Llamar Claude API (HTTP Request)
    ↓
Validar respuesta IA (Code)
    ↓
IF validación OK?
    ├── TRUE → Guardar dieta (Supabase)
    │              ↓
    │          Preparar datos PDF (Code)
    │              ↓
    │          Ejecutar Python PDF
    │              ↓
    │          IF PDF OK?
    │              ├── TRUE → Guardar URL PDF
    │              │              ↓
    │              │          IF requiere revisión?
    │              │              ├── TRUE → Telegram 🔔 revisión
    │              │              └── FALSE → Telegram ✅ lista
    │              │              ↓ (ambas ramas)
    │              │          Notion Dashboard
    │              │              ↓
    │              │          Gmail → Cliente
    │              │              ↓
    │              │          Supabase estado: enviada
    │              │              ↓
    │              │          Seguimientos: día 3, 14, 28
    │              └── FALSE → Log Error → Telegram 🚨
    └── FALSE → Log Error → Telegram 🚨
```

## Personalización

### Modificar fórmula de macros
Edita el nodo **"Function - Calcular Macros"**. Los factores de actividad y ajustes por objetivo están documentados en el código.

### Cambiar modelo de Claude
En el nodo **"HTTP - Claude API"**, cambia `"model": "claude-sonnet-4-20250514"` por el modelo deseado.

### Añadir más recetas
Usa la API de Supabase o el editor integrado para insertar filas en la tabla `recetas`.

### Deshabilitar Notion
Si no usas Notion, desconecta el nodo **"HTTP - Notion Dashboard"** y conecta directamente `Telegram → Gmail`.

## Notas sobre los seguimientos (días 3, 14, 28)

> **Importante:** n8n no tiene un `Schedule Trigger` que tome fechas dinámicas de datos anteriores. Los emails de seguimiento se envían inmediatamente en cadena cuando termina el flujo principal.

**Opciones para seguimientos reales con delay:**
1. **n8n Wait node:** Inserta un nodo `Wait` entre el envío principal y los seguimientos, configurado con tiempo relativo (3 días, 14 días, 28 días). **Requiere que el workflow esté activo y el proceso no falle.**
2. **Workflow separado:** Crea un workflow con Schedule Trigger (cron diario) que consulte Supabase buscando dietas donde `fecha_envio + 3/14/28 días = hoy` y envíe los emails correspondientes. *(Recomendado para producción)*
3. **n8n + cron job:** Usa la API de n8n para disparar ejecuciones programadas desde un servidor externo.

## Solución de problemas

| Problema | Causa probable | Solución |
|---|---|---|
| Error 401 en Claude API | API key incorrecta o expirada | Verificar `ANTHROPIC_API_KEY` |
| Error en Execute Command | Python no instalado o path incorrecto | `which python3` en el servidor |
| Supabase timeout | Conexión lenta o filtros incorrectos | Revisar `SUPABASE_URL` y `SERVICE_KEY` |
| PDF vacío | Script Python con error | Ejecutar manualmente con datos de prueba |
| Telegram no envía | `CHAT_ID` incorrecto | Verificar con `@userinfobot` en Telegram |
