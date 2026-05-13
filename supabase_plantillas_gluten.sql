-- ============================================================
-- TABLA: plantillas_dieta
-- Dietas pre-validadas sin gluten para uso como referencia
-- ============================================================

CREATE TABLE IF NOT EXISTS plantillas_dieta (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre      text NOT NULL,
  tipo        text NOT NULL,          -- 'sin_gluten', 'sin_lactosa', etc.
  descripcion text,
  activa      boolean DEFAULT true,
  dias        jsonb NOT NULL,         -- array de días con comidas
  created_at  timestamptz DEFAULT now()
);

-- ============================================================
-- PLANTILLA 1: Dieta Sin Gluten - Lourdes (versión 1)
-- ============================================================
INSERT INTO plantillas_dieta (nombre, tipo, descripcion, dias) VALUES (
  'Dieta Sin Gluten - Semana A',
  'sin_gluten',
  'Dieta semanal completa validada para celiaquía. 7 días, 4 comidas/día. Sin lácteos convencionales, con pan sin gluten, pasta de guisantes, noodles de arroz y tortitas de arroz.',
  '[
    {
      "dia": 1, "nombre_dia": "Lunes",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Bol de yogur alpro con corn flakes sin gluten y plátano", "ingredientes": ["200g yogur alpro coco", "15g corn flakes sin gluten", "1 plátano", "5g crema cacahuete", "canela", "edulcorante líquido"] },
        { "tipo": "Comida", "nombre": "Ensalada de pasta de guisantes con serrano y huevo duro", "ingredientes": ["30g pasta de guisante sin gluten", "1 huevo duro", "30g jamón serrano", "100g tomate", "50g pimiento rojo", "100g champiñones", "orégano", "sal", "1 manzana"] },
        { "tipo": "Merienda", "nombre": "Tortitas de arroz con queso y jamón cocido", "ingredientes": ["2 rebanadas tortitas de arroz", "1 cucharada queso para untar light", "3 lonchas jamón cocido"] },
        { "tipo": "Cena", "nombre": "Revuelto de calabacín con tomate y gamba pelada", "ingredientes": ["200g calabacín", "100g gambas peladas", "200g tomate", "100g zanahoria", "1 diente de ajo", "5ml aceite de oliva virgen", "sal rosa del Himalaya", "1 flan de huevo sin azúcares añadidos"] }
      ]
    },
    {
      "dia": 2, "nombre_dia": "Martes",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Pan sin gluten tostado con jamón cocido y tomate", "ingredientes": ["100ml leche", "café", "40g pan integral sin gluten", "2 lonchas jamón cocido", "3g aceite de oliva virgen", "tomate rallado"] },
        { "tipo": "Comida", "nombre": "Bol de quinoa con atún y verduras", "ingredientes": ["100g atún alita amarilla", "30g quinoa", "50g zanahoria", "20g maíz", "150g tomate", "lechuga al gusto", "1 yogur natural sin lactosa"] },
        { "tipo": "Merienda", "nombre": "Pan tostado sin gluten con lomo de pavo", "ingredientes": ["2 rebanadas pan tostado sin gluten 20-30g", "6 lonchas lomo de pavo"] },
        { "tipo": "Cena", "nombre": "Pescado blanco con guisantes y zanahoria", "ingredientes": ["120g merluza o lenguado", "90g guisantes de bote", "100g cebolla", "50g zanahoria", "7ml aceite de oliva virgen", "sal rosa del Himalaya", "1/2 yogur profeel protein pudding"] }
      ]
    },
    {
      "dia": 3, "nombre_dia": "Miércoles",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Bol de yogur alpro con corn flakes sin gluten y plátano", "ingredientes": ["200g yogur alpro coco", "15g corn flakes sin gluten", "1 plátano", "5g crema cacahuete", "canela", "edulcorante líquido"] },
        { "tipo": "Comida", "nombre": "Hamburguesa de espinaca y pollo con patata y berenjena", "ingredientes": ["1 hamburguesa espinaca y pollo", "150g patata", "150g berenjena", "5ml aceite de oliva virgen", "sal rosa del Himalaya", "pimienta", "laurel", "1/2 yogur profeel protein pudding"] },
        { "tipo": "Merienda", "nombre": "Pan tostado sin gluten con lomo de pavo", "ingredientes": ["2 rebanadas pan tostado sin gluten 20-30g", "6 lonchas lomo de pavo"] },
        { "tipo": "Cena", "nombre": "Habas con jamón de pavo y huevo", "ingredientes": ["80g habas baby tiernas", "60g jamón de pavo", "55g huevo", "100g cebolla", "1 diente de ajo", "5g aceite de oliva virgen", "sal", "pimentón dulce", "1 gelatina 0 azúcares"] }
      ]
    },
    {
      "dia": 4, "nombre_dia": "Jueves",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Pan sin gluten con lomo embuchado y tomate", "ingredientes": ["100ml leche", "café", "40g pan integral sin gluten", "1 pack lomo embuchado", "3g aceite de oliva virgen", "tomate rallado"] },
        { "tipo": "Comida", "nombre": "Mini pizza sobre fajita sin gluten con atún y champiñones", "ingredientes": ["1 fajita integral sin gluten", "1 vasito queso fresco sin lactosa", "1 lata atún al natural", "2 cucharadas tomate triturado", "100g espárrago de bote", "100g champiñones", "orégano", "1 kiwi"] },
        { "tipo": "Merienda", "nombre": "Tortitas de arroz con atún y semillas", "ingredientes": ["2 rebanadas tortitas de arroz", "1 cucharada queso para untar light", "1 lata atún al natural", "5g mezcla de semillas"] },
        { "tipo": "Cena", "nombre": "Ternera con salteado de verduras al horno", "ingredientes": ["120g ternera", "5ml aceite de oliva virgen", "sal rosa", "100g calabacín", "100g coliflor o brócoli", "100g pimiento rojo", "1/2 mousse proteína"] }
      ]
    },
    {
      "dia": 5, "nombre_dia": "Viernes",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Bol de yogur alpro con corn flakes sin gluten y plátano", "ingredientes": ["200g yogur alpro coco", "15g corn flakes sin gluten", "1 plátano", "5g crema cacahuete", "canela", "edulcorante líquido"] },
        { "tipo": "Comida", "nombre": "Mero a la plancha con palitos crujientes de zanahoria", "ingredientes": ["120g mero o dorada", "200g zanahoria", "7ml aceite de oliva virgen", "15g mostaza en grano", "vinagre de manzana", "comino", "pimentón dulce", "sal", "1/2 mousse proteína"] },
        { "tipo": "Merienda", "nombre": "Pan tostado sin gluten con lomo de pavo", "ingredientes": ["2 rebanadas pan tostado sin gluten 20-30g", "6 lonchas lomo de pavo"] },
        { "tipo": "Cena", "nombre": "Revuelto de setas con huevo y leche", "ingredientes": ["1 cebolleta grande", "1 diente de ajo", "100g setas o champiñones", "1 huevo", "1 clara de huevo", "50ml leche desnatada", "perejil fresco", "pimienta y sal", "5ml aceite de oliva virgen", "1 gelatina 0 azúcares"] }
      ]
    },
    {
      "dia": 6, "nombre_dia": "Sábado",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Pan sin gluten tostado con lomo embuchado y tomate", "ingredientes": ["100ml leche", "café", "40g pan integral sin gluten", "1 pack lomo embuchado", "3g aceite de oliva virgen", "tomate rallado"] },
        { "tipo": "Comida", "nombre": "Noodles de arroz con salsa de soja sin gluten y pollo", "ingredientes": ["30g noodles de arroz", "100g pechuga de pollo", "1 huevo duro", "100g brócoli", "50g champiñones", "50g zanahoria", "soja líquida sin gluten o tamari", "1 cucharada queso untar light", "2 rodajas piña"] },
        { "tipo": "Merienda", "nombre": "Yogur alpro con manzana y canela", "ingredientes": ["150g yogur alpro natural", "1 manzana", "edulcorante", "canela"] },
        { "tipo": "Cena", "nombre": "Lomo magro con verduras a la plancha", "ingredientes": ["120g lomo magro", "100g champiñones", "100g espárrago", "100g calabacín", "100g pimiento rojo", "5ml aceite de oliva virgen", "sal rosa del himalaya", "100g gelatina"] }
      ]
    },
    {
      "dia": 7, "nombre_dia": "Domingo",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Bol de corn flakes sin gluten con yogur y fruta", "ingredientes": ["100g yogur natural 0%", "15g corn flakes sin gluten", "1/2 plátano", "10g pipas de calabaza", "edulcorante", "canela"] },
        { "tipo": "Comida", "nombre": "Ensalada de queso de cabra con manzana y nueces", "ingredientes": ["lechuga o rúcula al gusto", "30g queso de cabra sin lactosa", "50g jamón serrano", "1 manzana", "15g nuez sin cáscara", "5ml aceite de oliva virgen", "5g vinagre", "sal"] },
        { "tipo": "Merienda", "nombre": "Yogur alpro con manzana y canela", "ingredientes": ["150g yogur alpro natural", "1 manzana", "edulcorante", "canela"] },
        { "tipo": "Cena", "nombre": "Tomate asado con huevo y queso fresco sin lactosa", "ingredientes": ["1 huevo", "1 vasito queso fresco 0% sin lactosa", "1/2 tomate", "7 tomates cherry", "orégano", "sal", "5g aceite de oliva virgen", "1/2 mousse proteína"] }
      ]
    }
  ]'::jsonb
);

-- ============================================================
-- PLANTILLA 2: Dieta Sin Gluten - Lourdes (versión 2)
-- ============================================================
INSERT INTO plantillas_dieta (nombre, tipo, descripcion, dias) VALUES (
  'Dieta Sin Gluten - Semana B',
  'sin_gluten',
  'Segunda semana sin gluten con variación en platos. Incluye boniato, garbanzos, salmón ahumado, quesadillas de maíz. Más comidas al día (5). Sin lactosa.',
  '[
    {
      "dia": 1, "nombre_dia": "Lunes",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Pan sin gluten con jamón cocido y leche sin lactosa", "ingredientes": ["100ml leche sin lactosa", "café", "2 rebanadas pan tostado sin gluten 20-30g", "3 lonchas jamón cocido", "rodajas de tomate", "3ml aceite de oliva virgen", "1 kiwi"] },
        { "tipo": "Comida", "nombre": "Alitas de pollo con boniato y piña", "ingredientes": ["5 alitas de pollo", "1 cebolla", "ajo en polvo", "pimentón dulce", "perejil", "100g boniato", "100g piña en su jugo"] },
        { "tipo": "Merienda 1", "nombre": "Yogur alpro con frutos secos y fresas", "ingredientes": ["200g yogur alpro sin azúcares añadidos", "15g frutos secos tostados sin sal", "150g fresas"] },
        { "tipo": "Cena", "nombre": "Pavo con guacamole gratinado y verduras", "ingredientes": ["150g pechuga de pavo", "50g guacamole", "30ml soja líquida sin gluten o tamari", "100g champiñones", "100g espárrago verde", "especias al gusto", "1 gelatina 0 azúcares"] }
      ]
    },
    {
      "dia": 2, "nombre_dia": "Martes",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Bol de yogur soja con corn flakes sin gluten y plátano", "ingredientes": ["125g yogur soja sin azúcares añadidos", "15g corn flakes sin gluten", "1 plátano pequeño", "5g crema cacahuete", "canela", "edulcorante líquido"] },
        { "tipo": "Comida", "nombre": "Pan pizza sin gluten con berenjena y salmón ahumado", "ingredientes": ["3 rebanadas pan integral sin gluten 60g máx", "100g berenjena", "2 lonchas queso sin lactosa", "70g salmón ahumado", "2 cucharadas pesto", "40g tomate triturado", "1 kiwi"] },
        { "tipo": "Merienda 1", "nombre": "Yogur alpro coco con manzana", "ingredientes": ["1 yogur alpro coco natural", "edulcorante", "canela", "1 manzana"] },
        { "tipo": "Cena", "nombre": "Ensalada de jamón con garbanzos y semillas", "ingredientes": ["60g jamón serrano", "40g jamón cocido", "80g garbanzos cocidos", "100g remolacha", "100g zanahoria", "10g mezcla de semillas", "sal rosa", "5ml aceite de oliva virgen", "1 gelatina 0 azúcares"] }
      ]
    },
    {
      "dia": 3, "nombre_dia": "Miércoles",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Pan sin gluten con queso fresco y jamón cocido", "ingredientes": ["100ml leche sin lactosa", "café", "2 rebanadas pan tostado sin gluten", "1/2 vasito queso fresco sin lactosa", "2 lonchas jamón cocido", "3ml aceite de oliva virgen", "1 kiwi"] },
        { "tipo": "Comida", "nombre": "Lomo con patata puñetazo al horno", "ingredientes": ["150g lomo magro", "150g patata", "pimentón dulce", "orégano", "sal", "cebolla en polvo", "ajo en polvo", "1 gelatina 0 azúcares"] },
        { "tipo": "Merienda 1", "nombre": "Yogur alpro con frutos secos y fresas", "ingredientes": ["200g yogur alpro sin azúcares añadidos", "15g frutos secos tostados sin sal", "150g fresas"] },
        { "tipo": "Cena", "nombre": "Tomate asado con huevo y queso fresco", "ingredientes": ["1 huevo", "1 vasito queso fresco 0% sin lactosa", "1/2 tomate", "7 tomates cherry", "orégano", "sal", "5g aceite de oliva virgen", "1/2 mousse proteína chocolate o vainilla"] }
      ]
    },
    {
      "dia": 4, "nombre_dia": "Jueves",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Bol de yogur soja con corn flakes sin gluten y plátano", "ingredientes": ["125g yogur soja sin azúcares añadidos", "15g corn flakes sin gluten", "1 plátano pequeño", "5g crema cacahuete", "canela", "edulcorante líquido"] },
        { "tipo": "Comida", "nombre": "Noodles de arroz con gambas y verduras", "ingredientes": ["30g noodles de arroz", "100g gambas peladas", "70g cebolla", "1 ajito tierno", "100g champiñones", "150g verdura verde", "5g aceite de oliva virgen", "sal rosa", "1 gelatina 0 azúcares"] },
        { "tipo": "Merienda 1", "nombre": "Tortitas de arroz con queso y jamón cocido", "ingredientes": ["14g tortitas de arroz o maíz (2 unidades)", "1/2 vasito queso fresco sin lactosa", "2 lonchas jamón cocido", "20g MIX beans edamame y soja"] },
        { "tipo": "Cena", "nombre": "Ternera con brócoli gratinado y tomate", "ingredientes": ["150g ternera", "200g brócoli", "1 tomate", "5 champiñones", "30g mozzarella", "orégano", "5g aceite de oliva virgen", "100g piña natural"] }
      ]
    },
    {
      "dia": 5, "nombre_dia": "Viernes",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Pan sin gluten con jamón cocido y tomate", "ingredientes": ["100ml leche sin lactosa", "café", "2 rebanadas pan tostado sin gluten", "3 lonchas jamón cocido", "rodajas de tomate", "3ml aceite de oliva virgen"] },
        { "tipo": "Comida", "nombre": "Quesadillas de maíz sin gluten con pollo y queso", "ingredientes": ["2 fajitas de maíz sin gluten pequeñas (Mercadona)", "5ml aceite de oliva virgen", "100g pechuga de pavo", "lechuga", "2 lonchas queso sin lactosa", "1 tomate", "20g jamón serrano", "1 naranja"] },
        { "tipo": "Merienda 1", "nombre": "Yogur alpro con frutos secos y fresas", "ingredientes": ["200g yogur alpro sin azúcares añadidos", "15g frutos secos tostados sin sal", "150g fresas"] },
        { "tipo": "Cena", "nombre": "Tortilla de berenjena con ensalada y yogur", "ingredientes": ["1 huevo", "1 clara de huevo", "1/2 berenjena o calabacín", "100g cebolla", "5ml aceite de oliva virgen", "1 tomate natural", "100g pepino", "sal y vinagre", "150g yogur de coco alpro natural"] }
      ]
    },
    {
      "dia": 6, "nombre_dia": "Sábado",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Tortita de harina de arroz con chocolate negro", "ingredientes": ["100ml claras de huevo", "20g harina de arroz", "canela", "edulcorante", "1 plátano", "1 onza chocolate negro +75% 15g", "10ml leche desnatada sin lactosa"] },
        { "tipo": "Snack", "nombre": "Batido de kéfir con arándanos", "ingredientes": ["250ml kéfir coco", "40g arándanos", "canela", "edulcorante"] },
        { "tipo": "Comida", "nombre": "Arroz con longanizas de pollo y garbanzos", "ingredientes": ["30g arroz", "2 longanizas de pollo sin gluten", "50g garbanzos cocidos", "1 tomate", "250ml caldo de pollo", "1 naranja"] },
        { "tipo": "Cena", "nombre": "Guisantes con jamón serrano y verduras", "ingredientes": ["100g guisantes o habas", "50g jamón serrano", "100g cebolla", "100g zanahoria", "5ml aceite de oliva virgen", "1/2 mousse proteína chocolate o vainilla"] }
      ]
    },
    {
      "dia": 7, "nombre_dia": "Domingo",
      "comidas": [
        { "tipo": "Desayuno", "nombre": "Tortita de harina de arroz con chocolate negro", "ingredientes": ["100ml claras de huevo", "20g harina de arroz", "canela", "edulcorante", "1 plátano", "1 onza chocolate negro +75% 15g", "10ml leche desnatada sin lactosa"] },
        { "tipo": "Snack", "nombre": "Batido de kéfir con arándanos", "ingredientes": ["250ml kéfir coco", "40g arándanos", "canela", "edulcorante"] },
        { "tipo": "Comida", "nombre": "Pasta sin gluten carbonara con pollo y champiñones", "ingredientes": ["30g pasta sin gluten", "100g pechuga de pollo o pavo", "10g jamón cocido", "100g champiñones", "5ml aceite de oliva virgen", "especias", "1/2 cebolla", "leche desnatada sin lactosa", "1 loncha queso havarti sin lactosa", "100g piña en su jugo"] },
        { "tipo": "Cena", "nombre": "Emperador con verduras al horno", "ingredientes": ["150g emperador", "100g calabacín", "100g pimiento verde", "100g cebolla", "5ml aceite de oliva virgen", "sal y especias", "1/2 mousse proteína chocolate o vainilla"] }
      ]
    }
  ]'::jsonb
);

-- Verificar inserción
SELECT id, nombre, tipo, activa, created_at FROM plantillas_dieta ORDER BY created_at;
