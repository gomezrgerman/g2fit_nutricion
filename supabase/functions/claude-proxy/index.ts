import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  });
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  if (req.method !== 'POST') {
    return json({ error: 'Method not allowed' }, 405);
  }

  try {
    const authHeader = req.headers.get('Authorization');
    if (!authHeader?.startsWith('Bearer ')) {
      return json({ error: 'Unauthorized' }, 401);
    }

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      { global: { headers: { Authorization: authHeader } } },
    );

    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return json({ error: 'Unauthorized' }, 401);
    }

    const body = await req.json().catch(() => null);
    if (!body || typeof body.text !== 'string' || typeof body.filename !== 'string') {
      return json({ error: 'Missing text or filename' }, 400);
    }

    const anthropicKey = Deno.env.get('ANTHROPIC_API_KEY');
    if (!anthropicKey) {
      return json({ error: 'Anthropic API key not configured on server' }, 503);
    }

    const safeName = body.filename.slice(0, 100).replace(/`/g, "'");
    const trimmed = body.text.slice(0, 8000).replace(/`/g, "'");

    const prompt = `Eres un dietista-nutricionista experto con amplios conocimientos de la composición nutricional de los alimentos. Analiza el texto del archivo "${safeName}".

TU TAREA:
1. Detecta todas las recetas o platos presentes en el texto
2. Para cada receta, extrae los ingredientes CON SUS CANTIDADES EXACTAS tal como aparecen en el PDF (ej: "200g pechuga de pollo", "1 huevo L", "50ml aceite de oliva")
3. Para cada ingrediente, indica "gramos" con el PESO NETO EN GRAMOS (número decimal):
   - "200g pechuga" → gramos: 200
   - "1 huevo L (70g)" → gramos: 70
   - "1 taza arroz (180ml)" → gramos: 180 (usa equivalencia estándar)
   - "1 cda aceite" → gramos: 14
   - Si la cantidad es un líquido en ml, usa 1ml≈1g como aproximación
   - Si no hay cantidad explícita, estima una ración típica
4. CALCULA los valores nutricionales SUMANDO los aportes de CADA ingrediente según su cantidad:
   - Usa tus valores nutricionales por 100g para cada alimento
   - Multiplica por la cantidad real indicada
   - Suma todos los ingredientes para obtener el total de la receta
   - Divide entre las porciones si se especifican

EJEMPLOS de cálculo:
- 200g pechuga de pollo (120kcal/100g) = 240kcal, 44g prot, 0g carb, 3g grasa
- 150g arroz cocido (130kcal/100g) = 195kcal, 2.5g prot, 44g carb, 0.5g grasa
- Total del plato = suma de todos los ingredientes

NUNCA dejes calorias, proteinas_g, carbohidratos_g o grasas_g en 0. Si hay ingrediente sin cantidad, estima una cantidad típica.

REGLAS JSON (obligatorio para que el resultado sea válido):
- Devuelve SOLO un array JSON, sin markdown ni texto adicional
- Strings en UNA SOLA LÍNEA: usa \\n para separar pasos de preparación, no saltos reales
- Números siempre como número (no string), nunca null
- Si no hay recetas en el texto: []

Formato exacto (un objeto por receta):
{"nombre":"Nombre del plato","categoria":"desayuno|comida|cena|snack|merienda","calorias":420,"proteinas_g":35,"carbohidratos_g":45,"grasas_g":8,"fibra_g":4,"azucar_g":2,"sodio_mg":380,"ingredientes":[{"nombre":"Pechuga de pollo","cantidad":"200g","gramos":200},{"nombre":"Arroz","cantidad":"80g seco","gramos":80}],"preparacion":"Paso 1\\nPaso 2\\nPaso 3","tiempo_prep_min":25,"dificultad":"facil|media|dificil","porciones":1,"alergenos":[],"restricciones":[],"tags":[]}

TEXTO DEL PDF:
${trimmed}`;

    const anthropicRes = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': anthropicKey,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5',
        max_tokens: 6000,
        messages: [{ role: 'user', content: prompt }],
      }),
    });

    if (!anthropicRes.ok) {
      const err = await anthropicRes.json().catch(() => ({}));
      return json(
        { error: (err as { error?: { message?: string } }).error?.message || `Anthropic HTTP ${anthropicRes.status}` },
        anthropicRes.status,
      );
    }

    const data = await anthropicRes.json();
    return json(data);

  } catch (error) {
    return json({ error: (error as Error).message }, 500);
  }
});
