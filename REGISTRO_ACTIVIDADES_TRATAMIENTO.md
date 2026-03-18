# Registro de Actividades de Tratamiento (RAT)
**Responsable:** Lydia Sarrió — G2Fit Nutrición
**Fecha de creación:** marzo de 2026
**Base legal:** Art. 30 RGPD (UE) 2016/679

---

> Este documento es de uso INTERNO. No publicar. Actualizar cada vez que cambie
> algún proceso, proveedor o finalidad del tratamiento de datos.

---

## Actividad 1 — Gestión de clientes y prestación del servicio nutricional

| Campo | Detalle |
|-------|---------|
| **Nombre de la actividad** | Gestión de clientes y elaboración de planes nutricionales |
| **Responsable del tratamiento** | Lydia Sarrió (G2Fit Nutrición) |
| **Finalidad** | Elaborar y entregar el plan de alimentación personalizado contratado por el cliente |
| **Base legal** | Ejecución de contrato (art. 6.1.b RGPD) + Consentimiento explícito para datos de salud (art. 9.2.a RGPD) |
| **Categorías de interesados** | Clientes particulares (personas físicas mayores de 18 años) |
| **Categorías de datos** | Nombre, email, teléfono, objetivo nutricional, peso/altura, alergias e intolerancias, preferencias alimentarias |
| **Datos especiales (art. 9)** | Sí — datos de salud (alergias, intolerancias, condición física) |
| **Destinatarios** | Ver tabla de encargados más abajo |
| **Transferencias internacionales** | Sí — Anthropic PBC (EE.UU.) bajo Cláusulas Contractuales Tipo de la UE; Supabase Inc. (servidores UE posible); Stripe Inc. (EE.UU.) con Privacy Shield / SCCs |
| **Plazo de conservación** | Durante la relación contractual + 5 años (obligaciones mercantiles/fiscales). Datos de salud: se eliminan al finalizar el contrato salvo consentimiento para conservarlos |
| **Medidas de seguridad** | Cifrado en tránsito (HTTPS/TLS), control de acceso con contraseña al panel de administración, acceso a datos limitado a la responsable |

---

## Actividad 2 — Gestión de pagos

| Campo | Detalle |
|-------|---------|
| **Nombre de la actividad** | Procesamiento de pagos del servicio |
| **Responsable del tratamiento** | Lydia Sarrió (G2Fit Nutrición) — datos de tarjeta gestionados íntegramente por Stripe |
| **Finalidad** | Cobro del servicio contratado |
| **Base legal** | Ejecución de contrato (art. 6.1.b RGPD) |
| **Categorías de interesados** | Clientes que contratan el servicio |
| **Categorías de datos** | Nombre, email, importe abonado, referencia de pago Stripe (G2Fit NO almacena datos de tarjeta) |
| **Datos especiales (art. 9)** | No |
| **Destinatarios** | Stripe Inc. (procesador de pago) |
| **Transferencias internacionales** | Sí — Stripe Inc. (EE.UU.) bajo mecanismos adecuados (SCCs) |
| **Plazo de conservación** | 5 años (obligación fiscal) |
| **Medidas de seguridad** | Stripe gestiona la seguridad de los datos de pago (PCI DSS). G2Fit solo conserva referencia de sesión |

---

## Actividad 3 — Envío de comunicaciones comerciales

| Campo | Detalle |
|-------|---------|
| **Nombre de la actividad** | Envío del plan nutricional y comunicaciones relacionadas con el servicio |
| **Responsable del tratamiento** | Lydia Sarrió (G2Fit Nutrición) |
| **Finalidad** | Entrega del plan de alimentación y lista de la compra por email; seguimiento del servicio |
| **Base legal** | Ejecución de contrato (art. 6.1.b RGPD) |
| **Categorías de interesados** | Clientes que han contratado y pagado el servicio |
| **Categorías de datos** | Nombre, email, contenido del plan nutricional |
| **Datos especiales (art. 9)** | Sí — el plan contiene información sobre preferencias y restricciones alimentarias |
| **Destinatarios** | Google LLC (Gmail, envío de email) |
| **Transferencias internacionales** | Sí — Google LLC (EE.UU.) bajo Privacy Shield / SCCs |
| **Plazo de conservación** | Hasta que el cliente solicite la baja o finalice el servicio |
| **Medidas de seguridad** | Cifrado TLS en tránsito; acceso al email limitado a la responsable |

---

## Tabla de encargados del tratamiento

| Proveedor | Rol | País | Garantía de transferencia | Web política privacidad |
|-----------|-----|------|--------------------------|------------------------|
| **Stripe Inc.** | Procesador de pago | EE.UU. | Cláusulas Contractuales Tipo (SCCs) | stripe.com/privacy |
| **Supabase Inc.** | Almacenamiento de datos (BBDD) | EE.UU. / UE | SCCs / servidores UE disponibles | supabase.com/privacy |
| **Google LLC (Gmail)** | Envío de correos electrónicos | EE.UU. | SCCs | policies.google.com/privacy |
| **Anthropic PBC** | Generación de planes con IA | EE.UU. | SCCs | anthropic.com/privacy |
| **n8n GmbH** | Automatización de flujos de trabajo | Alemania (UE) | Aplica RGPD directamente | n8n.io/privacy |
| **Tally** | Formulario de captación de datos | Bélgica (UE) | Aplica RGPD directamente | tally.so/privacy |

---

## Derechos de los interesados

Los interesados pueden ejercer sus derechos (acceso, rectificación, supresión, limitación, portabilidad, oposición, retirada del consentimiento) contactando en:

**lydia.dietista.denia@gmail.com**

Plazo de respuesta: 30 días naturales desde la recepción de la solicitud (art. 12 RGPD).
En caso de denegación, el interesado puede reclamar ante la **AEPD** (aepd.es).

---

## Historial de modificaciones

| Fecha | Cambio |
|-------|--------|
| Marzo 2026 | Creación inicial del registro |

---

*Actualizar este documento ante cualquier cambio en proveedores, finalidades o tipos de datos tratados.*
