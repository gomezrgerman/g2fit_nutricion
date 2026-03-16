"""
REGLAS DEL NUTRICIONISTA EXPERTO
Sistema completo de generación de dietas personalizadas
Autor: Sistema G2Fit
Versión: 1.0
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Sexo(Enum):
    MASCULINO = "masculino"
    FEMENINO = "femenino"


class Objetivo(Enum):
    PERDER_PESO = "perder_peso"
    GANAR_MASA = "ganar_masa"
    MANTENER = "mantener"
    DEFINICION = "definicion"


class NivelActividad(Enum):
    SEDENTARIO = 1.2
    LIGERAMENTE_ACTIVO = 1.375
    MODERADAMENTE_ACTIVO = 1.55
    MUY_ACTIVO = 1.725
    EXTREMADAMENTE_ACTIVO = 1.9


@dataclass
class PerfilCliente:
    """Perfil completo del cliente"""
    nombre: str
    edad: int
    sexo: Sexo
    peso_kg: float
    altura_cm: float
    objetivo: Objetivo
    nivel_actividad: NivelActividad
    
    # Opcionales
    restricciones: List[str] = None
    alergias: List[str] = None
    alimentos_no_gustan: List[str] = None
    preferencias: List[str] = None
    
    def __post_init__(self):
        if self.restricciones is None:
            self.restricciones = []
        if self.alergias is None:
            self.alergias = []
        if self.alimentos_no_gustan is None:
            self.alimentos_no_gustan = []
        if self.preferencias is None:
            self.preferencias = []


class CalculadoraNutricional:
    """
    Calculadora de requerimientos nutricionales basada en
    las mejores prácticas y estudios científicos actuales
    """
    
    @staticmethod
    def calcular_tmb(peso_kg: float, altura_cm: float, edad: int, sexo: Sexo) -> float:
        """
        Calcula la Tasa Metabólica Basal usando Mifflin-St Jeor
        (ecuación más precisa y moderna)
        
        Fórmula:
        - Hombres: TMB = (10 × peso) + (6.25 × altura) - (5 × edad) + 5
        - Mujeres: TMB = (10 × peso) + (6.25 × altura) - (5 × edad) - 161
        """
        base = (10 * peso_kg) + (6.25 * altura_cm) - (5 * edad)
        
        if sexo == Sexo.MASCULINO:
            return base + 5
        else:
            return base - 161
    
    @staticmethod
    def calcular_tdee(tmb: float, nivel_actividad: NivelActividad) -> float:
        """
        Calcula el Gasto Energético Total Diario
        TDEE = TMB × Factor de Actividad
        """
        return tmb * nivel_actividad.value
    
    @staticmethod
    def ajustar_calorias_por_objetivo(tdee: float, objetivo: Objetivo) -> float:
        """
        Ajusta las calorías según el objetivo del cliente
        
        Déficit/Superávit recomendados:
        - Perder peso: -15% a -25% (déficit)
        - Ganar masa: +10% a +15% (superávit)
        - Mantener: 0% (mantenimiento)
        - Definición: -10% a -15% (déficit leve)
        """
        if objetivo == Objetivo.PERDER_PESO:
            return tdee * 0.80  # -20% déficit
        elif objetivo == Objetivo.GANAR_MASA:
            return tdee * 1.12  # +12% superávit
        elif objetivo == Objetivo.DEFINICION:
            return tdee * 0.88  # -12% déficit leve
        else:  # MANTENER
            return tdee
    
    @staticmethod
    def calcular_proteina(peso_kg: float, objetivo: Objetivo, edad: int) -> float:
        """
        Calcula gramos de proteína diarios
        
        Rangos por objetivo:
        - Perder peso: 2.0-2.4 g/kg (preservar músculo en déficit)
        - Ganar masa: 1.6-2.2 g/kg (construcción muscular)
        - Mantener: 1.6-2.0 g/kg
        - Definición: 2.2-2.6 g/kg (máxima preservación)
        
        Ajustes por edad:
        - 40-60 años: +0.2 g/kg (combatir sarcopenia)
        - 60+ años: +0.4 g/kg
        """
        # Base según objetivo
        if objetivo == Objetivo.PERDER_PESO:
            base = 2.2
        elif objetivo == Objetivo.GANAR_MASA:
            base = 1.9
        elif objetivo == Objetivo.DEFINICION:
            base = 2.4
        else:  # MANTENER
            base = 1.8
        
        # Ajuste por edad
        if edad >= 60:
            base += 0.4
        elif edad >= 40:
            base += 0.2
        
        return peso_kg * base
    
    @staticmethod
    def calcular_grasas(peso_kg: float, sexo: Sexo) -> float:
        """
        Calcula gramos de grasas diarios
        
        Rangos:
        - Mujeres: 1.0-1.2 g/kg (NUNCA <0.9 g/kg - salud hormonal)
        - Hombres: 0.8-1.0 g/kg (NUNCA <0.7 g/kg)
        
        Las grasas son esenciales para:
        - Producción hormonal
        - Absorción vitaminas liposolubles
        - Función cerebral
        - Salud cardiovascular
        """
        if sexo == Sexo.FEMENINO:
            return peso_kg * 1.0  # Mujeres necesitan más grasa
        else:
            return peso_kg * 0.9
    
    @staticmethod
    def calcular_carbohidratos(calorias_objetivo: float, proteina_g: float, grasas_g: float) -> float:
        """
        Calcula gramos de carbohidratos (variable de ajuste)
        
        Carbohidratos = (Calorías totales - Calorías proteína - Calorías grasas) / 4
        
        - Proteína: 4 kcal/g
        - Grasas: 9 kcal/g
        - Carbohidratos: 4 kcal/g
        """
        calorias_proteina = proteina_g * 4
        calorias_grasas = grasas_g * 9
        calorias_carbohidratos = calorias_objetivo - calorias_proteina - calorias_grasas
        
        return max(0, calorias_carbohidratos / 4)  # Nunca negativo


class MacrosCalculados:
    """Contenedor para los macros calculados"""
    
    def __init__(self, perfil: PerfilCliente):
        self.perfil = perfil
        calc = CalculadoraNutricional()
        
        # Cálculos base
        self.tmb = calc.calcular_tmb(
            perfil.peso_kg,
            perfil.altura_cm,
            perfil.edad,
            perfil.sexo
        )
        
        self.tdee = calc.calcular_tdee(self.tmb, perfil.nivel_actividad)
        
        self.calorias_objetivo = calc.ajustar_calorias_por_objetivo(
            self.tdee,
            perfil.objetivo
        )
        
        # Macronutrientes
        self.proteina_g = calc.calcular_proteina(
            perfil.peso_kg,
            perfil.objetivo,
            perfil.edad
        )
        
        self.grasas_g = calc.calcular_grasas(
            perfil.peso_kg,
            perfil.sexo
        )
        
        self.carbohidratos_g = calc.calcular_carbohidratos(
            self.calorias_objetivo,
            self.proteina_g,
            self.grasas_g
        )
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para uso fácil"""
        return {
            "tmb": round(self.tmb, 0),
            "tdee": round(self.tdee, 0),
            "calorias_objetivo": round(self.calorias_objetivo, 0),
            "proteina_g": round(self.proteina_g, 1),
            "grasas_g": round(self.grasas_g, 1),
            "carbohidratos_g": round(self.carbohidratos_g, 1),
            "proteina_kcal": round(self.proteina_g * 4, 0),
            "grasas_kcal": round(self.grasas_g * 9, 0),
            "carbohidratos_kcal": round(self.carbohidratos_g * 4, 0)
        }
    
    def __str__(self) -> str:
        d = self.to_dict()
        return f"""
Perfil: {self.perfil.nombre}
TMB: {d['tmb']} kcal
TDEE: {d['tdee']} kcal
Objetivo Calórico: {d['calorias_objetivo']} kcal

MACRONUTRIENTES DIARIOS:
├─ Proteína: {d['proteina_g']}g ({d['proteina_kcal']} kcal)
├─ Grasas: {d['grasas_g']}g ({d['grasas_kcal']} kcal)
└─ Carbohidratos: {d['carbohidratos_g']}g ({d['carbohidratos_kcal']} kcal)
        """


class DistribucionComidas:
    """
    Distribuye los macros en comidas a lo largo del día
    siguiendo las mejores prácticas de nutrición deportiva
    """
    
    PATRONES_DISTRIBUCION = {
        "estandar_4_comidas": {
            "desayuno": 0.25,
            "comida": 0.35,
            "snack": 0.15,
            "cena": 0.25
        },
        "estandar_5_comidas": {
            "desayuno": 0.20,
            "snack_manana": 0.15,
            "comida": 0.30,
            "snack_tarde": 0.15,
            "cena": 0.20
        },
        "deportista": {
            "desayuno": 0.20,
            "pre_entreno": 0.20,
            "post_entreno": 0.35,
            "cena": 0.25
        }
    }
    
    @staticmethod
    def distribuir_macros(macros: MacrosCalculados, patron: str = "estandar_4_comidas") -> Dict:
        """
        Distribuye los macros según el patrón elegido
        
        Regla importante: Proteína se distribuye EQUITATIVAMENTE
        (no por porcentaje de calorías, sino por gramos)
        """
        distribucion_calorias = DistribucionComidas.PATRONES_DISTRIBUCION.get(
            patron,
            DistribucionComidas.PATRONES_DISTRIBUCION["estandar_4_comidas"]
        )
        
        num_comidas = len(distribucion_calorias)
        proteina_por_comida = macros.proteina_g / num_comidas
        
        resultado = {}
        
        for comida, porcentaje in distribucion_calorias.items():
            calorias_comida = macros.calorias_objetivo * porcentaje
            
            # Proteína equitativa
            proteina = proteina_por_comida
            
            # Grasas proporcionales
            grasas = macros.grasas_g * porcentaje
            
            # Carbohidratos llenan el resto
            calorias_restantes = calorias_comida - (proteina * 4) - (grasas * 9)
            carbohidratos = max(0, calorias_restantes / 4)
            
            resultado[comida] = {
                "calorias": round(calorias_comida, 0),
                "proteina_g": round(proteina, 1),
                "grasas_g": round(grasas, 1),
                "carbohidratos_g": round(carbohidratos, 1)
            }
        
        return resultado


# ============================================================
# BASE DE DATOS DE ALIMENTOS Y ROTACIONES
# ============================================================

PROTEINAS_ANIMALES = {
    "pollo": {
        "proteina_por_100g": 31,
        "grasas_por_100g": 3.6,
        "carbohidratos_por_100g": 0,
        "preparaciones": [
            "A la plancha con limón y hierbas",
            "Al horno con especias cajún",
            "Estofado con verduras",
            "Salteado estilo asiático (soja, jengibre)",
            "A la parrilla con chimichurri",
            "En curry con leche de coco light",
            "Relleno al horno con espinacas"
        ]
    },
    "pavo": {
        "proteina_por_100g": 29,
        "grasas_por_100g": 1,
        "carbohidratos_por_100g": 0,
        "preparaciones": [
            "A la plancha con romero",
            "En albóndigas con tomate",
            "Salteado con verduras",
            "Al horno con mostaza y miel",
            "En fajitas con pimientos"
        ]
    },
    "ternera_magra": {
        "proteina_por_100g": 26,
        "grasas_por_100g": 5,
        "carbohidratos_por_100g": 0,
        "preparaciones": [
            "Estofado con verduras",
            "A la plancha con ajo y perejil",
            "Salteado estilo mongol",
            "En ragú con tomate",
            "A la parrilla con chimichurri"
        ]
    },
    "salmon": {
        "proteina_por_100g": 25,
        "grasas_por_100g": 13,
        "carbohidratos_por_100g": 0,
        "tipo": "pescado_azul",
        "preparaciones": [
            "Al horno con limón",
            "A la plancha con eneldo",
            "En papillote con verduras",
            "Ahumado en ensalada",
            "Teriyaki a la parrilla"
        ]
    },
    "merluza": {
        "proteina_por_100g": 17,
        "grasas_por_100g": 2,
        "carbohidratos_por_100g": 0,
        "tipo": "pescado_blanco",
        "preparaciones": [
            "Al vapor con verduras",
            "Al horno con tomate",
            "A la plancha con limón",
            "En salsa verde",
            "Rebozada light (harina avena)"
        ]
    },
    "huevos": {
        "proteina_por_100g": 13,
        "grasas_por_100g": 11,
        "carbohidratos_por_100g": 1,
        "preparaciones": [
            "Revueltos con verduras",
            "Tortilla francesa",
            "Cocidos (para ensaladas)",
            "Pochados sobre tostada",
            "Al horno con tomate (shakshuka)",
            "Frittata de verduras"
        ]
    },
    "atun": {
        "proteina_por_100g": 30,
        "grasas_por_100g": 1,
        "carbohidratos_por_100g": 0,
        "tipo": "pescado_azul",
        "preparaciones": [
            "Fresco a la plancha",
            "En tataki estilo japonés",
            "Natural en ensalada",
            "Al horno con sésamo",
            "Sellado con especias"
        ]
    }
}

PROTEINAS_VEGETALES = {
    "lentejas": {
        "proteina_por_100g": 9,
        "grasas_por_100g": 0.4,
        "carbohidratos_por_100g": 20,
        "fibra_por_100g": 8,
        "preparaciones": [
            "Guiso tradicional",
            "Dal indio con especias",
            "Ensalada fría con verduras",
            "Hamburguesas vegetales",
            "Salteadas con arroz"
        ]
    },
    "garbanzos": {
        "proteina_por_100g": 9,
        "grasas_por_100g": 2.6,
        "carbohidratos_por_100g": 27,
        "fibra_por_100g": 8,
        "preparaciones": [
            "Hummus casero",
            "Cocido completo",
            "Asados al horno especiados",
            "Curry de garbanzos",
            "Ensalada mezclum"
        ]
    },
    "tofu": {
        "proteina_por_100g": 8,
        "grasas_por_100g": 4,
        "carbohidratos_por_100g": 2,
        "preparaciones": [
            "Salteado con verduras",
            "Revuelto (sustituto huevos)",
            "Al horno marinado",
            "En curry tailandés",
            "A la plancha con especias"
        ]
    },
    "quinoa": {
        "proteina_por_100g": 4.4,
        "grasas_por_100g": 1.9,
        "carbohidratos_por_100g": 21,
        "fibra_por_100g": 2.8,
        "preparaciones": [
            "Ensalada fría con verduras",
            "Salteada con vegetales",
            "Base para buddha bowl",
            "Con leche vegetal (desayuno)",
            "Relleno para pimientos"
        ]
    }
}

CARBOHIDRATOS_COMPLEJOS = {
    "arroz_integral": {
        "carbohidratos_por_100g": 23,
        "proteina_por_100g": 2.6,
        "grasas_por_100g": 0.9,
        "fibra_por_100g": 1.8,
        "ig": "medio"
    },
    "arroz_basmati": {
        "carbohidratos_por_100g": 25,
        "proteina_por_100g": 2.7,
        "grasas_por_100g": 0.3,
        "fibra_por_100g": 0.4,
        "ig": "bajo"
    },
    "avena": {
        "carbohidratos_por_100g": 12,
        "proteina_por_100g": 2.4,
        "grasas_por_100g": 1.4,
        "fibra_por_100g": 1.7,
        "ig": "bajo"
    },
    "patata": {
        "carbohidratos_por_100g": 17,
        "proteina_por_100g": 2,
        "grasas_por_100g": 0.1,
        "fibra_por_100g": 2.2,
        "ig": "medio-alto"
    },
    "boniato": {
        "carbohidratos_por_100g": 20,
        "proteina_por_100g": 1.6,
        "grasas_por_100g": 0.1,
        "fibra_por_100g": 3,
        "ig": "medio"
    },
    "pasta_integral": {
        "carbohidratos_por_100g": 23,
        "proteina_por_100g": 5,
        "grasas_por_100g": 0.5,
        "fibra_por_100g": 3.5,
        "ig": "bajo"
    },
    "pan_centeno": {
        "carbohidratos_por_100g": 48,
        "proteina_por_100g": 8.5,
        "grasas_por_100g": 1.7,
        "fibra_por_100g": 5.8,
        "ig": "bajo"
    }
}

VERDURAS = {
    "verdes": ["brócoli", "espinacas", "judías verdes", "calabacín", "lechuga", "pepino", "col", "espárragos"],
    "rojas_naranjas": ["tomate", "pimiento rojo", "zanahoria", "calabaza", "remolacha", "pimiento naranja"],
    "blancas": ["coliflor", "cebolla", "ajo", "champiñones", "puerro"],
    "moradas": ["berenjena", "col lombarda", "cebolla morada"]
}

GRASAS_SALUDABLES = {
    "aceite_oliva": {
        "grasas_por_100ml": 100,
        "tipo": "monoinsaturada"
    },
    "aguacate": {
        "grasas_por_100g": 15,
        "tipo": "monoinsaturada"
    },
    "frutos_secos": {
        "almendras": {"grasas_por_100g": 50, "proteina_por_100g": 21},
        "nueces": {"grasas_por_100g": 65, "proteina_por_100g": 15},
        "anacardos": {"grasas_por_100g": 44, "proteina_por_100g": 18}
    },
    "semillas": {
        "chia": {"grasas_por_100g": 31, "proteina_por_100g": 17, "omega3": "alto"},
        "lino": {"grasas_por_100g": 42, "proteina_por_100g": 18, "omega3": "alto"},
        "sesamo": {"grasas_por_100g": 50, "proteina_por_100g": 18}
    }
}

ESPECIAS_POR_TIPO_COCINA = {
    "mediterraneo": ["orégano", "tomillo", "romero", "albahaca", "laurel"],
    "asiatico": ["jengibre", "cilantro", "lima", "salsa soja baja en sodio", "aceite sésamo"],
    "mexicano": ["comino", "cilantro", "chile", "pimentón", "lima"],
    "indio": ["curry", "cúrcuma", "garam masala", "comino", "cilantro"],
    "marroqui": ["canela", "comino", "cilantro", "jengibre", "pimentón"]
}


# ============================================================
# REGLAS DE VARIEDAD Y NO MONOTONÍA
# ============================================================

class ReglaVariedad:
    """
    Implementa las reglas de oro de variedad para evitar dietas monótonas
    """
    
    REGLAS = {
        "nunca_repetir_proteina_consecutiva": True,
        "nunca_repetir_carbohidrato_consecutivo": True,
        "minimo_3_colores_por_plato": True,
        "rotar_tecnicas_culinarias": True,
        "incluir_receta_fun_semanal": True,
        "variar_especias_diariamente": True
    }
    
    @staticmethod
    def validar_proteinas_semana(proteinas_semana: List[str]) -> bool:
        """
        Valida que no haya proteínas repetidas en días consecutivos
        """
        for i in range(len(proteinas_semana) - 1):
            if proteinas_semana[i] == proteinas_semana[i + 1]:
                return False
        return True
    
    @staticmethod
    def generar_rotacion_proteinas(dias: int = 7, restricciones: List[str] = None) -> List[str]:
        """
        Genera una rotación de proteínas para X días sin repeticiones consecutivas
        """
        if restricciones is None:
            restricciones = []
        
        proteinas_disponibles = list(PROTEINAS_ANIMALES.keys())
        
        # Filtrar según restricciones
        if "pescado" in restricciones or "no_pescado" in restricciones:
            proteinas_disponibles = [p for p in proteinas_disponibles 
                                    if "tipo" not in PROTEINAS_ANIMALES[p] or 
                                    "pescado" not in PROTEINAS_ANIMALES[p].get("tipo", "")]
        
        if "vegetariano" in restricciones or "vegano" in restricciones:
            proteinas_disponibles = list(PROTEINAS_VEGETALES.keys())
        
        # Generar rotación evitando repeticiones
        rotacion = []
        ultimo = None
        
        for _ in range(dias):
            opciones = [p for p in proteinas_disponibles if p != ultimo]
            import random
            seleccion = random.choice(opciones)
            rotacion.append(seleccion)
            ultimo = seleccion
        
        return rotacion
    
    @staticmethod
    def generar_plato_con_colores(proteina: str, carbohidrato: str) -> Dict:
        """
        Genera un plato asegurando mínimo 3 colores
        """
        import random
        
        # Seleccionar verduras de diferentes colores
        color_verde = random.choice(VERDURAS["verdes"])
        color_rojo_naranja = random.choice(VERDURAS["rojas_naranjas"])
        
        return {
            "proteina": proteina,
            "carbohidrato": carbohidrato,
            "verdura_verde": color_verde,
            "verdura_color": color_rojo_naranja,
            "colores": 4  # proteína + carbohidrato + 2 verduras
        }


# ============================================================
# AJUSTES POR PERFIL ESPECÍFICO
# ============================================================

class AjustesPorEdad:
    """Ajustes nutricionales específicos por rango de edad"""
    
    @staticmethod
    def aplicar_ajustes(edad: int, macros: Dict) -> Dict:
        """
        Aplica ajustes según edad
        """
        ajustes = macros.copy()
        
        if edad >= 60:
            # Seniors: Mayor proteína (anti-sarcopenia)
            ajustes["proteina_g"] *= 1.15
            ajustes["notas_edad"] = [
                "Proteína aumentada para prevenir sarcopenia",
                "Priorizar alimentos ricos en calcio y vitamina D",
                "Considerar 5-6 comidas pequeñas para mejor digestión",
                "Texturas más blandas si es necesario"
            ]
            
        elif edad >= 50:
            # Pre-seniors
            ajustes["proteina_g"] *= 1.10
            ajustes["notas_edad"] = [
                "Proteína aumentada para preservar masa muscular",
                "Aumentar omega-3 (salud cardiovascular)",
                "Control de sodio (<2300mg/día)",
                "Alimentos ricos en calcio"
            ]
            
        elif edad >= 40:
            # Adultos maduros
            ajustes["proteina_g"] *= 1.05
            ajustes["notas_edad"] = [
                "Ligero aumento de proteína por cambios metabólicos",
                "Priorizar grasas saludables",
                "Incluir omega-3 regularmente",
                "Controlar carbohidratos refinados"
            ]
        
        return ajustes


class AjustesPorSexo:
    """Ajustes nutricionales específicos por sexo"""
    
    @staticmethod
    def aplicar_ajustes_mujer(macros: Dict, edad: int) -> Dict:
        """
        Ajustes específicos para mujeres
        """
        ajustes = macros.copy()
        
        # Grasas nunca por debajo del mínimo (salud hormonal)
        if ajustes["grasas_g"] < ajustes.get("peso_kg", 70) * 0.9:
            ajustes["grasas_g"] = ajustes.get("peso_kg", 70) * 0.9
        
        ajustes["notas_sexo"] = [
            "Grasas mantenidas en rango alto (salud hormonal)",
            "Incluir alimentos ricos en hierro (18mg/día si pre-menopausia)",
            "Calcio: 1000-1200mg/día"
        ]
        
        if edad >= 50:
            ajustes["notas_sexo"].append("Post-menopausia: Calcio 1200mg/día, considerar fitoestrógenos (soja, lino)")
        else:
            ajustes["notas_sexo"].append("Considerar ciclo menstrual: más carbos en fase folicular, más grasas en fase lútea")
        
        return ajustes
    
    @staticmethod
    def aplicar_ajustes_hombre(macros: Dict) -> Dict:
        """
        Ajustes específicos para hombres
        """
        ajustes = macros.copy()
        
        ajustes["notas_sexo"] = [
            "Mayor capacidad de síntesis proteica",
            "Zinc: 11mg/día (producción testosterona)",
            "Pueden manejar déficits/superávits más agresivos"
        ]
        
        return ajustes


# ============================================================
# SUSTITUCIONES POR RESTRICCIONES
# ============================================================

SUSTITUCIONES = {
    "gluten": {
        "trigo": ["arroz", "quinoa", "maíz", "patata", "avena sin gluten"],
        "pan": ["pan sin gluten", "tortas de arroz", "pan de maíz"],
        "pasta": ["pasta de arroz", "pasta de maíz", "pasta de quinoa"]
    },
    "lactosa": {
        "leche": ["leche sin lactosa", "bebida de soja enriquecida", "bebida de avena", "bebida de almendras enriquecida"],
        "yogur": ["yogur sin lactosa", "yogur de soja", "yogur de coco"],
        "queso": ["queso sin lactosa", "queso curado (bajo en lactosa)", "queso vegano"]
    },
    "huevo": {
        "huevo_entero": ["tofu revuelto", "semillas de lino molidas + agua (repostería)"],
        "clara": ["aquafaba (agua de garbanzos)"]
    },
    "frutos_secos": {
        "almendras": ["semillas de calabaza", "semillas de girasol"],
        "nueces": ["semillas de chía", "semillas de lino"],
        "mantequilla_frutos_secos": ["tahini", "mantequilla de semillas"]
    },
    "pescado": {
        "salmon": ["pollo", "tofu", "tempeh", "huevos"],
        "omega3": ["semillas de lino molidas", "semillas de chía", "nueces", "suplemento omega-3 vegetal"]
    }
}


# ============================================================
# GENERADOR DE PLAN SEMANAL
# ============================================================

class GeneradorPlanSemanal:
    """
    Generador inteligente de planes nutricionales semanales
    que aplica todas las reglas del nutricionista experto
    """
    
    def __init__(self, perfil: PerfilCliente):
        self.perfil = perfil
        self.macros = MacrosCalculados(perfil)
        self.distribucion = DistribucionComidas.distribuir_macros(self.macros)
    
    def generar_plan_completo(self) -> Dict:
        """
        Genera un plan nutricional completo de 7 días
        aplicando todas las reglas de variedad
        """
        # Generar rotación de proteínas
        proteinas_semana = ReglaVariedad.generar_rotacion_proteinas(
            dias=7,
            restricciones=self.perfil.restricciones
        )
        
        plan_semanal = {
            "perfil": {
                "nombre": self.perfil.nombre,
                "edad": self.perfil.edad,
                "objetivo": self.perfil.objetivo.value
            },
            "macros_objetivo": self.macros.to_dict(),
            "dias": []
        }
        
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        for i, dia in enumerate(dias_semana):
            plan_dia = {
                "nombre_dia": dia,
                "proteina_principal": proteinas_semana[i],
                "comidas": self._generar_comidas_dia(proteinas_semana[i])
            }
            plan_semanal["dias"].append(plan_dia)
        
        return plan_semanal
    
    def _generar_comidas_dia(self, proteina_principal: str) -> List[Dict]:
        """
        Genera las comidas de un día completo
        """
        comidas = []
        
        for nombre_comida, macros_comida in self.distribucion.items():
            comida = {
                "nombre": nombre_comida,
                "macros": macros_comida,
                "ejemplo": f"Ejemplo de {nombre_comida} con {proteina_principal}"
            }
            comidas.append(comida)
        
        return comidas


# ============================================================
# FUNCIÓN PRINCIPAL DE USO
# ============================================================

def generar_dieta_personalizada(
    nombre: str,
    edad: int,
    sexo: str,
    peso_kg: float,
    altura_cm: float,
    objetivo: str,
    nivel_actividad: str,
    restricciones: List[str] = None,
    alergias: List[str] = None
) -> Dict:
    """
    FUNCIÓN PRINCIPAL para generar una dieta personalizada completa
    
    Parámetros:
    -----------
    nombre: str
        Nombre del cliente
    edad: int
        Edad en años
    sexo: str
        "masculino" o "femenino"
    peso_kg: float
        Peso en kilogramos
    altura_cm: float
        Altura en centímetros
    objetivo: str
        "perder_peso", "ganar_masa", "mantener" o "definicion"
    nivel_actividad: str
        "sedentario", "ligeramente_activo", "moderadamente_activo", 
        "muy_activo" o "extremadamente_activo"
    restricciones: List[str], opcional
        Lista de restricciones alimentarias (ej: ["vegetariano", "sin_gluten"])
    alergias: List[str], opcional
        Lista de alergias (ej: ["lactosa", "frutos_secos"])
    
    Retorna:
    --------
    Dict: Diccionario completo con el plan nutricional personalizado
    
    Ejemplo de uso:
    ---------------
    ```python
    dieta = generar_dieta_personalizada(
        nombre="María García",
        edad=32,
        sexo="femenino",
        peso_kg=68,
        altura_cm=165,
        objetivo="perder_peso",
        nivel_actividad="moderadamente_activo",
        restricciones=["sin_lactosa"],
        alergias=[]
    )
    
    print(dieta["macros_objetivo"])
    print(dieta["plan_semanal"])
    ```
    """
    # Convertir strings a enums
    sexo_enum = Sexo.MASCULINO if sexo.lower() == "masculino" else Sexo.FEMENINO
    
    objetivo_map = {
        "perder_peso": Objetivo.PERDER_PESO,
        "ganar_masa": Objetivo.GANAR_MASA,
        "mantener": Objetivo.MANTENER,
        "definicion": Objetivo.DEFINICION
    }
    objetivo_enum = objetivo_map.get(objetivo.lower(), Objetivo.MANTENER)
    
    actividad_map = {
        "sedentario": NivelActividad.SEDENTARIO,
        "ligeramente_activo": NivelActividad.LIGERAMENTE_ACTIVO,
        "moderadamente_activo": NivelActividad.MODERADAMENTE_ACTIVO,
        "muy_activo": NivelActividad.MUY_ACTIVO,
        "extremadamente_activo": NivelActividad.EXTREMADAMENTE_ACTIVO
    }
    actividad_enum = actividad_map.get(nivel_actividad.lower(), NivelActividad.MODERADAMENTE_ACTIVO)
    
    # Crear perfil
    perfil = PerfilCliente(
        nombre=nombre,
        edad=edad,
        sexo=sexo_enum,
        peso_kg=peso_kg,
        altura_cm=altura_cm,
        objetivo=objetivo_enum,
        nivel_actividad=actividad_enum,
        restricciones=restricciones or [],
        alergias=alergias or []
    )
    
    # Generar plan
    generador = GeneradorPlanSemanal(perfil)
    plan_completo = generador.generar_plan_completo()
    
    # Aplicar ajustes por edad y sexo
    macros_ajustados = AjustesPorEdad.aplicar_ajustes(edad, plan_completo["macros_objetivo"])
    
    if sexo_enum == Sexo.FEMENINO:
        macros_ajustados = AjustesPorSexo.aplicar_ajustes_mujer(macros_ajustados, edad)
    else:
        macros_ajustados = AjustesPorSexo.aplicar_ajustes_hombre(macros_ajustados)
    
    plan_completo["macros_ajustados"] = macros_ajustados
    
    # Añadir recomendaciones generales
    plan_completo["recomendaciones"] = [
        f"Hidratación: {round(peso_kg * 35)} ml/día (agua)",
        "Distribuir proteína equitativamente en todas las comidas",
        "Incluir verduras en todas las comidas principales",
        "Variar colores de verduras diariamente",
        "Priorizar alimentos enteros sobre procesados",
        "Dormir 7-9 horas para optimizar resultados"
    ]
    
    return plan_completo


# ============================================================
# EJEMPLO DE USO
# ============================================================

if __name__ == "__main__":
    # Ejemplo de uso del sistema
    print("=" * 70)
    print("SISTEMA GENERADOR DE DIETAS PERSONALIZADAS")
    print("Nutricionista Experto - G2Fit")
    print("=" * 70)
    
    # Crear un ejemplo
    dieta_ejemplo = generar_dieta_personalizada(
        nombre="María García",
        edad=32,
        sexo="femenino",
        peso_kg=68,
        altura_cm=165,
        objetivo="perder_peso",
        nivel_actividad="moderadamente_activo",
        restricciones=["sin_lactosa"],
        alergias=[]
    )
    
    print("\nPERFIL DEL CLIENTE:")
    print(f"Nombre: {dieta_ejemplo['perfil']['nombre']}")
    print(f"Edad: {dieta_ejemplo['perfil']['edad']} años")
    print(f"Objetivo: {dieta_ejemplo['perfil']['objetivo']}")
    
    print("\nMACROS OBJETIVO:")
    macros = dieta_ejemplo['macros_objetivo']
    print(f"Calorías: {macros['calorias_objetivo']} kcal")
    print(f"Proteína: {macros['proteina_g']}g")
    print(f"Grasas: {macros['grasas_g']}g")
    print(f"Carbohidratos: {macros['carbohidratos_g']}g")
    
    print("\nRECOMENDACIONES:")
    for rec in dieta_ejemplo['recomendaciones']:
        print(f"• {rec}")
    
    print("\nPLAN SEMANAL GENERADO:")
    for dia in dieta_ejemplo['dias']:
        print(f"\n{dia['nombre_dia']}: Proteína principal - {dia['proteina_principal']}")
    
    print("\n" + "=" * 70)
    print("Sistema listo para integración con n8n/Claude API")
    print("=" * 70)
