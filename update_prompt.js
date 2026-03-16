const fs = require('fs');
const dir = __dirname;
const wf2 = JSON.parse(fs.readFileSync(dir + '/G2Fit - 2. Generador de Dietas.json', 'utf8'));

const node = wf2.nodes.find(n => n.name === 'Function - Construir Prompt Claude');

node.parameters.jsCode = `// ===== CONSTRUIR PROMPT PARA CLAUDE =====

const item = $input.first().json;
const cliente = item.cliente;
const calculos = item.calculos;
const cliente_id = item.cliente_id;

// Helpers para formatear arrays
const lista = (arr) => arr && arr.length > 0 ? arr.join(', ') : 'Ninguna';
const listaOpcional = (arr) => arr && arr.length > 0 ? arr.join(', ') : null;

// ─── SECCIÓN PREFERENCIAS ALIMENTARIAS ───────────────────────────────────────
const preferenciasLineas = [];

if (cliente.consume_lacteos === false) {
  preferenciasLineas.push('- NO consume lácteos');
} else if (cliente.consume_lacteos === true) {
  preferenciasLineas.push('- Consume lácteos: Sí');
}

if (listaOpcional(cliente.proteinas_preferidas)) {
  preferenciasLineas.push(\`- Proteínas preferidas: \${lista(cliente.proteinas_preferidas)}\`);
}
if (cliente.notas_proteinas) {
  preferenciasLineas.push(\`- Notas proteínas: \${cliente.notas_proteinas}\`);
}
if (listaOpcional(cliente.apetencias)) {
  preferenciasLineas.push(\`- Apetencias / gustos: \${lista(cliente.apetencias)}\`);
}
if (cliente.consume_verduras) {
  preferenciasLineas.push(\`- Verduras: \${cliente.consume_verduras}\`);
}
if (listaOpcional(cliente.carbohidratos_preferidos)) {
  preferenciasLineas.push(\`- Carbohidratos preferidos: \${lista(cliente.carbohidratos_preferidos)}\`);
}
if (cliente.frutos_secos_preferidos) {
  preferenciasLineas.push(\`- Frutos secos preferidos: \${cliente.frutos_secos_preferidos}\`);
}
if (cliente.alimentos_a_evitar) {
  preferenciasLineas.push(\`- Alimentos a evitar / que sientan mal: \${cliente.alimentos_a_evitar}\`);
}
if (cliente.consume_alcohol) {
  preferenciasLineas.push(\`- Consumo de alcohol: \${cliente.consume_alcohol}\`);
}
if (cliente.pica_entre_comidas) {
  preferenciasLineas.push(\`- Picoteo entre comidas: \${cliente.pica_entre_comidas}\`);
}

// ─── SECCIÓN HISTORIAL ────────────────────────────────────────────────────────
const historialLineas = [];
if (cliente.dieta_anterior) {
  historialLineas.push(\`- Dieta anterior: \${cliente.dieta_anterior}\`);
}
if (cliente.tiempo_objetivo) {
  historialLineas.push(\`- Tiempo para lograr el objetivo: \${cliente.tiempo_objetivo}\`);
}
if (cliente.datos_interes) {
  historialLineas.push(\`- Datos de interés adicionales: \${cliente.datos_interes}\`);
}

// ─── COMIDAS DEL DÍA ─────────────────────────────────────────────────────────
const comidasDia = cliente.comidas_diarias || 5;
const comidasSeleccionadas = cliente.comidas_seleccionadas && cliente.comidas_seleccionadas.length > 0
  ? cliente.comidas_seleccionadas.join(', ')
  : 'Desayuno, Snack Mañana, Almuerzo, Snack Tarde, Cena';

const prompt = \`Eres un nutricionista experto. Genera un plan nutricional personalizado de 1 SEMANA (7 días) que el cliente seguirá durante el mes.

**DATOS DEL CLIENTE:**
- Nombre: \${cliente.nombre} \${cliente.apellidos || ''}
- Edad: \${cliente.edad} años
- Sexo: \${cliente.sexo}
- Peso actual: \${cliente.peso_actual} kg
- Altura: \${cliente.altura} cm
- Peso objetivo: \${cliente.peso_objetivo || 'No especificado'} kg
- Objetivo: \${cliente.objetivo}
- Nivel de actividad: \${cliente.nivel_actividad}
- IMC: \${calculos.imc} (\${calculos.imc_categoria})

**REQUERIMIENTOS CALÓRICOS DIARIOS:**
- Calorías: \${calculos.objetivo.calorias} kcal
- Proteínas: \${calculos.objetivo.proteinas_g}g
- Carbohidratos: \${calculos.objetivo.carbohidratos_g}g
- Grasas: \${calculos.objetivo.grasas_g}g

**RESTRICCIONES OBLIGATORIAS (respetar siempre):**
- Alergias: \${lista(cliente.alergias)}
- Intolerancias: \${lista(cliente.intolerancias)}

**COMIDAS DEL DÍA:**
- Número de comidas: \${comidasDia}
- Comidas seleccionadas: \${comidasSeleccionadas}

**PREFERENCIAS ALIMENTARIAS (adaptar el plan a estas preferencias):**
\${preferenciasLineas.length > 0 ? preferenciasLineas.join('\n') : '- Sin preferencias especificadas'}
\${historialLineas.length > 0 ? '\n**HISTORIAL Y CONTEXTO:**\n' + historialLineas.join('\n') : ''}

INSTRUCCIONES MUY IMPORTANTES:
1. Responde SOLO con JSON válido
2. NO uses markdown (\\`\\`\\`json)
3. NO incluyas texto antes o después
4. El JSON debe empezar con { y terminar con }
5. Usa exactamente las comidas que el cliente seleccionó (no añadas ni quites comidas)
6. Respeta SIEMPRE las alergias e intolerancias
7. Prioriza los alimentos y proteínas que el cliente prefiere
8. Evita los alimentos que el cliente indicó que le sientan mal

ESTRUCTURA REQUERIDA:
{
  "semanas": [
    {
      "numero": 1,
      "dias": [
        {
          "dia": 1,
          "nombre_dia": "Lunes",
          "comidas": [
            {
              "tipo": "Desayuno",
              "nombre": "Nombre corto",
              "ingredientes": ["ingrediente 1", "ingrediente 2"],
              "calorias": 400,
              "proteinas": 30,
              "carbohidratos": 45,
              "grasas": 10
            }
          ],
          "totales_dia": {
            "calorias": \${calculos.objetivo.calorias},
            "proteinas": \${calculos.objetivo.proteinas_g},
            "carbohidratos": \${calculos.objetivo.carbohidratos_g},
            "grasas": \${calculos.objetivo.grasas_g}
          }
        }
      ]
    }
  ],
  "resumen_plan": {
    "calorias_promedio": \${calculos.objetivo.calorias},
    "proteinas_promedio": \${calculos.objetivo.proteinas_g},
    "carbohidratos_promedio": \${calculos.objetivo.carbohidratos_g},
    "grasas_promedio": \${calculos.objetivo.grasas_g}
  }
}

REQUISITOS:
- Genera EXACTAMENTE 1 semana (7 días)
- Cada día incluye solo las comidas que el cliente eligió: \${comidasSeleccionadas}
- NO incluyas "preparacion" en las comidas (solo nombre e ingredientes)
- Calcula correctamente totales_dia
- Respeta las calorías objetivo (\${calculos.objetivo.calorias} kcal/día)

Genera ahora el plan completo en JSON puro.\`;

return [{
  json: {
    prompt,
    cliente_id,
    nombre_cliente: cliente.nombre,
    objetivo: cliente.objetivo,
    calculos,
    cliente
  }
}];`;

fs.writeFileSync(dir + '/G2Fit - 2. Generador de Dietas.json', JSON.stringify(wf2, null, 2));
console.log('OK - Function - Construir Prompt Claude actualizado con todos los campos nuevos');
