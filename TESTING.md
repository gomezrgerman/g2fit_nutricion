# TESTING.md - Guía de Pruebas

## Pruebas por fase

### Fase 1 - Webhook (Nodo 1-2)

Envía una solicitud de prueba con `curl` o Postman:

```bash
curl -X POST https://n8n.srv964210.hstgr.cloud/webhook-test/nueva-solicitud-dieta \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María García",
    "email": "maria@test.com",
    "telefono": "+34 600 000 001",
    "edad": 32,
    "sexo": "femenino",
    "peso_actual": 70,
    "altura": 165,
    "peso_objetivo": 62,
    "objetivo": "perder_peso",
    "nivel_actividad": "moderado",
    "alergias": "lacteos",
    "intolerancias": "",
    "preferencias_dieta": "sin_gluten",
    "alimentos_excluidos": "",
    "patologias": "",
    "medicacion": "",
    "comidas_diarias": 4,
    "presupuesto_semanal": 80,
    "cocina_habitualmente": true
  }'
```

**Resultado esperado:** `{"status": "received", "message": "..."}`

---

### Fase 2 - Cálculo de Macros (Nodo 3)

Verifica en los logs de n8n que el output del nodo `Function - Calcular Macros` contiene:

```json
{
  "calculos": {
    "tmb": 1489,
    "tdee": 2306,
    "imc": 25.7,
    "imc_categoria": "Sobrepeso",
    "objetivo": {
      "calorias": 1845,
      "proteinas_g": 126,
      "carbohidratos_g": 178,
      "grasas_g": 57
    }
  }
}
```

> Los valores exactos variarán según los datos enviados. Verifica que la fórmula Mifflin-St Jeor sea correcta.

---

### Fase 3 - Base de datos (Nodos 4-5)

Comprueba en Supabase:

```sql
-- Verificar que se insertó el cliente
SELECT * FROM clientes ORDER BY created_at DESC LIMIT 1;

-- Verificar que hay recetas disponibles
SELECT COUNT(*) FROM recetas WHERE activa = true;
```

---

### Fase 4 - Claude API (Nodos 6-8)

- Verificar en n8n que el nodo `HTTP - Claude API` devuelve `status: 200`
- El output de `Function - Validar Respuesta IA` debe tener `validacion.valido: true`
- Si hay errores de parseo, buscar en los logs del nodo la respuesta raw de Claude

**Prueba manual del prompt:**
```bash
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: TU_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Di solo: OK"}]
  }'
```

---

### Fase 5 - PDF (Nodo 12)

```bash
# Prueba directa del script Python
python3 /opt/scripts/generar_pdf_dieta.py '{
  "dieta_id": "test-001",
  "fecha_generacion": "2026-02-25",
  "cliente": {
    "nombre": "María García",
    "email": "maria@test.com",
    "edad": 32,
    "sexo": "femenino",
    "peso_actual": 70,
    "altura": 165,
    "imc": 25.7,
    "imc_categoria": "Sobrepeso",
    "objetivo": "perder_peso",
    "alergias": [],
    "preferencias_dieta": [],
    "comidas_diarias": 4
  },
  "objetivos_nutricionales": {
    "calorias": 1845,
    "proteinas_g": 126,
    "carbohidratos_g": 178,
    "grasas_g": 57
  },
  "plan_28_dias": [
    {
      "numero_semana": 1,
      "dias": [
        {
          "dia_semana": "Lunes",
          "comidas": [
            {"momento": "desayuno", "nombre": "Tortilla de avena", "macros": {"calorias": 380, "proteinas_g": 22, "carbohidratos_g": 45, "grasas_g": 10}},
            {"momento": "comida", "nombre": "Pollo con quinoa", "macros": {"calorias": 520, "proteinas_g": 45, "carbohidratos_g": 48, "grasas_g": 12}},
            {"momento": "merienda", "nombre": "Batido proteico", "macros": {"calorias": 280, "proteinas_g": 30, "carbohidratos_g": 28, "grasas_g": 5}},
            {"momento": "cena", "nombre": "Salmón al horno", "macros": {"calorias": 480, "proteinas_g": 38, "carbohidratos_g": 35, "grasas_g": 18}}
          ],
          "totales_dia": {"calorias": 1660, "proteinas_g": 135, "carbohidratos_g": 156, "grasas_g": 45}
        }
      ]
    }
  ],
  "resumen": {"calorias_promedio": 1845, "proteinas_promedio": 126},
  "recomendaciones": ["Beber 2L de agua diarios"],
  "nutricionista": {"nombre": "Nutricionista G2Fit", "email": "nutricion@g2fit.com", "num_colegiado": "CO-12345"}
}' '/tmp/dieta_test.pdf'

# Verificar que se generó
ls -la /tmp/dieta_test.pdf
```

---

### Fase 6 - Telegram (Nodos 16a, 16b, ERR-3)

```bash
# Obtener el chat_id de tu bot
curl https://api.telegram.org/bot<TU_BOT_TOKEN>/getUpdates

# Enviar mensaje de prueba
curl -X POST https://api.telegram.org/bot<TU_BOT_TOKEN>/sendMessage \
  -d chat_id=<CHAT_ID> \
  -d text="Test conexión G2Fit ✅"
```

---

### Fase 7 - Gmail (Nodo 19)

Después de ejecutar el workflow completo, verifica:
1. Que el cliente recibió el email
2. Que el PDF se adjunta correctamente
3. Que el asunto es correcto

---

### Verificación en Supabase (estado final)

```sql
-- Ver dieta generada
SELECT id, estado, calorias_objetivo, calorias_reales, desviacion_porcentaje,
       requiere_revision, motivo_revision, pdf_url, created_at
FROM dietas_generadas
ORDER BY created_at DESC LIMIT 1;

-- Ver logs de la ejecución
SELECT tipo_log, fase, mensaje, created_at
FROM logs_generacion
ORDER BY created_at DESC LIMIT 20;
```

---

## Casos de prueba especiales

| Caso | Datos | Resultado esperado |
|---|---|---|
| Alergias múltiples | `"alergias": "lacteos,gluten,huevo"` | Recetas sin esos alergenos |
| Calorías muy bajas | `edad:50, peso:45, altura:150, sexo:femenino, sedentario` | Alerta en Telegram |
| IMC extremo | `peso:120, altura:160` | `requiere_revision: true` |
| JSON inválido de Claude | Simular error de red | Nodo ERR activado |
| PDF falla | Cambiar path a ruta inexistente | Telegram 🚨 con error PDF |

---

## Monitoreo en producción

```sql
-- Dashboard resumen diario
SELECT
  DATE(created_at) as fecha,
  COUNT(*) as total_generadas,
  SUM(CASE WHEN requiere_revision THEN 1 ELSE 0 END) as con_revision,
  SUM(CASE WHEN estado = 'enviada' THEN 1 ELSE 0 END) as enviadas,
  AVG(desviacion_porcentaje) as desviacion_media
FROM dietas_generadas
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY fecha DESC;
```
