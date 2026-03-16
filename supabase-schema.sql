-- ============================================================
-- G2FIT NUTRICIÓN - Schema Supabase
-- ============================================================

-- Extensión UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- TABLA: clientes
-- ============================================================
CREATE TABLE IF NOT EXISTS public.clientes (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  nombre              TEXT NOT NULL,
  email               TEXT NOT NULL UNIQUE,
  telefono            TEXT,
  edad                INTEGER NOT NULL CHECK (edad > 0 AND edad < 120),
  sexo                TEXT NOT NULL CHECK (sexo IN ('masculino','femenino')),
  peso_actual         DECIMAL(5,2) NOT NULL,
  altura              INTEGER NOT NULL,
  peso_objetivo       DECIMAL(5,2),
  objetivo            TEXT NOT NULL CHECK (objetivo IN ('perder_peso','ganar_masa','mantener','definicion')),
  nivel_actividad     TEXT NOT NULL CHECK (nivel_actividad IN ('sedentario','ligero','moderado','activo','muy_activo')),
  alergias            TEXT[] DEFAULT '{}',
  intolerancias       TEXT[] DEFAULT '{}',
  preferencias_dieta  TEXT[] DEFAULT '{}',
  alimentos_excluidos TEXT[] DEFAULT '{}',
  patologias          TEXT[] DEFAULT '{}',
  medicacion          TEXT,
  comidas_diarias     INTEGER DEFAULT 3 CHECK (comidas_diarias BETWEEN 2 AND 6),
  presupuesto_semanal DECIMAL(8,2),
  cocina_habitualmente BOOLEAN DEFAULT true,
  imc                 DECIMAL(4,2),
  id_solicitud        TEXT UNIQUE,
  created_at          TIMESTAMPTZ DEFAULT NOW(),
  updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLA: recetas
-- ============================================================
CREATE TABLE IF NOT EXISTS public.recetas (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  nombre          TEXT NOT NULL,
  categoria       TEXT NOT NULL CHECK (categoria IN ('desayuno','comida','cena','snack','merienda')),
  calorias        DECIMAL(7,2) NOT NULL,
  proteinas_g     DECIMAL(6,2) NOT NULL,
  carbohidratos_g DECIMAL(6,2) NOT NULL,
  grasas_g        DECIMAL(6,2) NOT NULL,
  fibra_g         DECIMAL(6,2) DEFAULT 0,
  azucar_g        DECIMAL(6,2) DEFAULT 0,
  sodio_mg        DECIMAL(7,2) DEFAULT 0,
  ingredientes    JSONB NOT NULL DEFAULT '[]',
  preparacion     TEXT,
  tiempo_prep_min INTEGER DEFAULT 15,
  dificultad      TEXT DEFAULT 'media' CHECK (dificultad IN ('facil','media','dificil')),
  porciones       INTEGER DEFAULT 1,
  alergenos       TEXT[] DEFAULT '{}',
  restricciones   TEXT[] DEFAULT '{}',
  tags            TEXT[] DEFAULT '{}',
  imagen_url      TEXT,
  activa          BOOLEAN DEFAULT true,
  veces_usada     INTEGER DEFAULT 0,
  valoracion_media DECIMAL(3,2) DEFAULT 0,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLA: dietas_generadas
-- ============================================================
CREATE TABLE IF NOT EXISTS public.dietas_generadas (
  id                     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  cliente_id             UUID NOT NULL REFERENCES public.clientes(id) ON DELETE CASCADE,
  estado                 TEXT DEFAULT 'generada' CHECK (estado IN ('generada','en_revision','aprobada','enviada','completada','cancelada')),
  -- Objetivos calculados
  calorias_objetivo      DECIMAL(7,2),
  proteinas_objetivo     DECIMAL(6,2),
  carbohidratos_objetivo DECIMAL(6,2),
  grasas_objetivo        DECIMAL(6,2),
  -- Valores reales del plan
  calorias_reales        DECIMAL(7,2),
  proteinas_reales       DECIMAL(6,2),
  carbohidratos_reales   DECIMAL(6,2),
  grasas_reales          DECIMAL(6,2),
  desviacion_porcentaje  DECIMAL(5,2),
  -- Plan completo
  plan_completo          JSONB,
  pdf_url                TEXT,
  -- Revisión
  requiere_revision      BOOLEAN DEFAULT false,
  motivo_revision        TEXT,
  revisada_por           TEXT,
  fecha_revision         TIMESTAMPTZ,
  -- Seguimiento
  fecha_envio            TIMESTAMPTZ,
  email_dia3_enviado     BOOLEAN DEFAULT false,
  email_dia14_enviado    BOOLEAN DEFAULT false,
  email_dia28_enviado    BOOLEAN DEFAULT false,
  feedback_dia_28        TEXT,
  renovacion_solicitada  BOOLEAN DEFAULT false,
  -- Metadatos
  modelo_ia              TEXT DEFAULT 'claude-sonnet-4-20250514',
  tokens_usados          INTEGER,
  tiempo_generacion_ms   INTEGER,
  created_at             TIMESTAMPTZ DEFAULT NOW(),
  updated_at             TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- TABLA: logs_generacion
-- ============================================================
CREATE TABLE IF NOT EXISTS public.logs_generacion (
  id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  dieta_id    UUID REFERENCES public.dietas_generadas(id) ON DELETE SET NULL,
  cliente_id  UUID REFERENCES public.clientes(id) ON DELETE SET NULL,
  tipo_log    TEXT NOT NULL CHECK (tipo_log IN ('info','warning','error','debug')),
  fase        TEXT,
  nodo        TEXT,
  mensaje     TEXT NOT NULL,
  datos       JSONB DEFAULT '{}',
  stack_trace TEXT,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ÍNDICES
-- ============================================================
CREATE INDEX idx_clientes_email         ON public.clientes(email);
CREATE INDEX idx_clientes_objetivo      ON public.clientes(objetivo);
CREATE INDEX idx_clientes_created_at    ON public.clientes(created_at DESC);

CREATE INDEX idx_recetas_categoria      ON public.recetas(categoria);
CREATE INDEX idx_recetas_activa         ON public.recetas(activa);
CREATE INDEX idx_recetas_calorias       ON public.recetas(calorias);
CREATE INDEX idx_recetas_alergenos      ON public.recetas USING GIN(alergenos);
CREATE INDEX idx_recetas_restricciones  ON public.recetas USING GIN(restricciones);
CREATE INDEX idx_recetas_tags           ON public.recetas USING GIN(tags);

CREATE INDEX idx_dietas_cliente_id      ON public.dietas_generadas(cliente_id);
CREATE INDEX idx_dietas_estado          ON public.dietas_generadas(estado);
CREATE INDEX idx_dietas_requiere_rev    ON public.dietas_generadas(requiere_revision) WHERE requiere_revision = true;
CREATE INDEX idx_dietas_created_at      ON public.dietas_generadas(created_at DESC);

CREATE INDEX idx_logs_dieta_id          ON public.logs_generacion(dieta_id);
CREATE INDEX idx_logs_tipo              ON public.logs_generacion(tipo_log);
CREATE INDEX idx_logs_created_at        ON public.logs_generacion(created_at DESC);

-- ============================================================
-- TRIGGER: updated_at automático
-- ============================================================
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_clientes_updated_at
  BEFORE UPDATE ON public.clientes
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER trg_recetas_updated_at
  BEFORE UPDATE ON public.recetas
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER trg_dietas_updated_at
  BEFORE UPDATE ON public.dietas_generadas
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================
ALTER TABLE public.clientes         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.recetas          ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dietas_generadas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.logs_generacion  ENABLE ROW LEVEL SECURITY;

-- Service role bypasses RLS (n8n usa service role key)
-- Solo lectura pública para recetas activas
CREATE POLICY "Recetas activas visibles" ON public.recetas
  FOR SELECT USING (activa = true);

-- Service role tiene acceso total (para n8n)
CREATE POLICY "Service role full access clientes" ON public.clientes
  USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access dietas" ON public.dietas_generadas
  USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access logs" ON public.logs_generacion
  USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access recetas" ON public.recetas
  USING (auth.role() = 'service_role');

-- Acceso completo desde browser con anon key (gestor de recetas es herramienta privada)
-- La anon key es segura de usar en el browser, no expone credenciales admin
CREATE POLICY "Anon full access recetas insert" ON public.recetas
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Anon full access recetas update" ON public.recetas
  FOR UPDATE USING (true) WITH CHECK (true);

CREATE POLICY "Anon full access recetas delete" ON public.recetas
  FOR DELETE USING (true);

-- ============================================================
-- DATOS INICIALES: Recetas de ejemplo
-- ============================================================
INSERT INTO public.recetas (nombre, categoria, calorias, proteinas_g, carbohidratos_g, grasas_g, fibra_g, ingredientes, preparacion, tiempo_prep_min, dificultad, alergenos, restricciones, tags) VALUES
('Tortilla de avena con frutas', 'desayuno', 380, 22, 45, 10, 5, '[{"nombre":"avena","cantidad":"80g","gramos":80},{"nombre":"huevos","cantidad":"2","gramos":120},{"nombre":"platano","cantidad":"1","gramos":118},{"nombre":"fresas","cantidad":"100g","gramos":100}]', 'Mezclar avena molida con huevos batidos. Cocinar en sartén antiadherente. Servir con frutas.', 10, 'facil', '{"gluten","huevo"}', '{"vegetariana"}', '{"alto_proteina","rapido"}'),
('Pechuga de pollo con quinoa y verduras', 'comida', 520, 45, 48, 12, 8, '[{"nombre":"pechuga_pollo","cantidad":"200g","gramos":200},{"nombre":"quinoa","cantidad":"80g","gramos":80},{"nombre":"brocoli","cantidad":"200g","gramos":200},{"nombre":"zanahoria","cantidad":"1","gramos":80},{"nombre":"aceite_oliva","cantidad":"1cda","gramos":14}]', 'Cocinar quinoa. Asar pollo a la plancha con especias. Saltear verduras con aceite de oliva. Servir todo junto.', 25, 'media', '{}', '{"sin_gluten","sin_lactosa","alta_proteina"}', '{"alto_proteina","saludable"}'),
('Salmon al horno con patata dulce', 'cena', 480, 38, 35, 18, 6, '[{"nombre":"salmon","cantidad":"180g","gramos":180},{"nombre":"batata","cantidad":"200g","gramos":200},{"nombre":"esparragos","cantidad":"150g","gramos":150},{"nombre":"limon","cantidad":"1","gramos":58},{"nombre":"aceite_oliva","cantidad":"1cda","gramos":14}]', 'Hornear salmón con limón y hierbas a 180°C 20 min. Asar batata en dados. Cocinar espárragos al vapor.', 30, 'facil', '{"pescado"}', '{"sin_gluten","sin_lactosa"}', '{"omega3","antiinflamatorio"}'),
('Greek yogurt con granola y miel', 'desayuno', 320, 18, 42, 8, 3, '[{"nombre":"yogur_griego","cantidad":"200g","gramos":200},{"nombre":"granola","cantidad":"50g","gramos":50},{"nombre":"miel","cantidad":"1cda","gramos":21},{"nombre":"arandanos","cantidad":"80g","gramos":80}]', 'Disponer yogur en bol, añadir granola y frutos rojos, terminar con miel.', 5, 'facil', '{"lacteo","gluten"}', '{"vegetariana"}', '{"rapido","probiotico"}'),
('Ensalada de garbanzos y aguacate', 'comida', 440, 18, 42, 20, 12, '[{"nombre":"garbanzos_cocidos","cantidad":"200g","gramos":200},{"nombre":"aguacate","cantidad":"1","gramos":150},{"nombre":"tomate","cantidad":"2","gramos":200},{"nombre":"pepino","cantidad":"1","gramos":200},{"nombre":"limon","cantidad":"1","gramos":58},{"nombre":"aceite_oliva","cantidad":"2cda","gramos":28}]', 'Mezclar todos los ingredientes en bol grande. Aliñar con limón y aceite de oliva. Salpimentar.', 10, 'facil', '{}', '{"vegana","sin_gluten","sin_lactosa"}', '{"vegano","fibra","grasas_saludables"}'),
('Batido proteico post-entreno', 'snack', 280, 30, 28, 5, 2, '[{"nombre":"proteina_whey","cantidad":"30g","gramos":30},{"nombre":"platano","cantidad":"1","gramos":118},{"nombre":"leche_desnatada","cantidad":"250ml","gramos":250},{"nombre":"mantequilla_cacahuete","cantidad":"1cda","gramos":16}]', 'Batir todos los ingredientes en licuadora hasta obtener textura homogénea.', 5, 'facil', '{"lacteo","cacahuete"}', '{}', '{"post_entreno","alto_proteina","rapido"}'),
('Sopa de lentejas con verduras', 'cena', 350, 20, 52, 6, 14, '[{"nombre":"lentejas","cantidad":"150g","gramos":150},{"nombre":"zanahoria","cantidad":"2","gramos":160},{"nombre":"cebolla","cantidad":"1","gramos":110},{"nombre":"tomate","cantidad":"2","gramos":200},{"nombre":"espinacas","cantidad":"100g","gramos":100},{"nombre":"comino","cantidad":"1cta","gramos":2}]', 'Sofreír cebolla y zanahoria. Añadir lentejas, tomate y caldo. Cocinar 25 min. Añadir espinacas al final.', 35, 'facil', '{}', '{"vegana","sin_gluten","sin_lactosa"}', '{"vegano","legumbres","economico"}'),
('Tostada integral con aguacate y huevo', 'desayuno', 410, 20, 38, 18, 7, '[{"nombre":"pan_integral","cantidad":"2_rebanadas","gramos":80},{"nombre":"aguacate","cantidad":"1","gramos":150},{"nombre":"huevos","cantidad":"2","gramos":120},{"nombre":"tomate_cherry","cantidad":"6","gramos":90},{"nombre":"sal_pimienta","cantidad":"al_gusto","gramos":0}]', 'Tostar pan. Chafar aguacate con limón y sal. Freír o escalfar huevos. Montar sobre pan con tomates.', 12, 'facil', '{"gluten","huevo"}', '{"vegetariana"}', '{"desayuno_completo","grasas_saludables"}');
