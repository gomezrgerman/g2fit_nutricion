#!/usr/bin/env python3
"""
G2FIT NUTRICIÓN - Generador de PDF de Dietas Personalizadas
Uso: python3 generar_pdf_dieta.py '<json_datos>' '<ruta_output>'

Dependencias:
    pip install reportlab pillow requests

Versión: 2.0.0 - Reglas Nutricionista Experto
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
except ImportError:
    print("ERROR: Instala reportlab con: pip install reportlab", file=sys.stderr)
    sys.exit(1)

# ============================================================
# COLORES DE MARCA G2FIT
# ============================================================
COLOR_NAVY     = colors.HexColor('#0F172A')   # Navy oscuro
COLOR_PINK     = colors.HexColor('#FB5FAB')   # Rosa G2Fit
COLOR_PINK_D   = colors.HexColor('#d63c8e')   # Rosa oscuro
COLOR_LIGHT    = colors.HexColor('#FFF0F7')   # Rosa muy claro
COLOR_WHITE    = colors.white
COLOR_DARK     = colors.HexColor('#0F172A')
COLOR_GRAY     = colors.HexColor('#64748B')
COLOR_WARN     = colors.HexColor('#f59e0b')
COLOR_PINK_GRID = colors.HexColor('#f9a8d4')


# ============================================================
# CLASE PRINCIPAL
# ============================================================
class GeneradorPDFDieta:

    def __init__(self, datos: dict, ruta_output: str):
        self.datos = datos
        self.ruta_output = ruta_output
        self.styles = getSampleStyleSheet()
        self._crear_estilos()

    def _crear_estilos(self):
        self.estilo_titulo = ParagraphStyle(
            'Titulo',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=COLOR_NAVY,
            alignment=TA_CENTER,
            spaceAfter=10
        )
        self.estilo_subtitulo = ParagraphStyle(
            'Subtitulo',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=COLOR_NAVY,
            spaceBefore=14,
            spaceAfter=6
        )
        self.estilo_semana = ParagraphStyle(
            'Semana',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=COLOR_WHITE,
            alignment=TA_CENTER,
            backColor=COLOR_PINK,
            spaceBefore=16,
            spaceAfter=6,
            leftIndent=8,
            rightIndent=8,
            borderPad=6
        )
        self.estilo_dia = ParagraphStyle(
            'Dia',
            parent=self.styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=COLOR_PINK_D,
            spaceBefore=10,
            spaceAfter=4
        )
        self.estilo_normal = ParagraphStyle(
            'Normal2',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=COLOR_DARK,
            spaceAfter=4,
            leading=14
        )
        self.estilo_pequeno = ParagraphStyle(
            'Pequeno',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            textColor=COLOR_GRAY,
            spaceAfter=2
        )
        self.estilo_bold = ParagraphStyle(
            'Bold2',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=COLOR_DARK
        )
        self.estilo_disclaimer = ParagraphStyle(
            'Disclaimer',
            parent=self.styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            textColor=COLOR_GRAY,
            alignment=TA_JUSTIFY,
            spaceAfter=4
        )
        self.estilo_alerta = ParagraphStyle(
            'Alerta',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=COLOR_WARN,
            spaceAfter=3
        )

    # ─── GENERACIÓN PRINCIPAL ────────────────────────────────────────────────
    def generar(self) -> bool:
        try:
            Path(self.ruta_output).parent.mkdir(parents=True, exist_ok=True)

            cliente_nombre = self.datos.get('cliente', {}).get('nombre', 'Cliente')
            doc = SimpleDocTemplate(
                self.ruta_output,
                pagesize=A4,
                rightMargin=1.5*cm,
                leftMargin=1.5*cm,
                topMargin=1.8*cm,
                bottomMargin=1.5*cm,
                title=f"Plan Nutricional - {cliente_nombre}",
                author='G2Fit Nutricion'
            )

            contenido = []
            contenido += self._portada()
            contenido.append(PageBreak())
            contenido += self._resumen_nutricional()
            contenido.append(PageBreak())
            contenido += self._plan_4_semanas()
            contenido += self._recomendaciones()
            contenido += self._disclaimer()

            doc.build(contenido, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
            print(f"PDF generado: {self.ruta_output}")
            return True

        except Exception as e:
            print(f"ERROR generando PDF: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            return False

    # ─── HEADER Y FOOTER ────────────────────────────────────────────────────
    def _header_footer(self, canvas_obj, doc):
        canvas_obj.saveState()
        w, h = A4

        # Header navy con línea rosa
        canvas_obj.setFillColor(COLOR_NAVY)
        canvas_obj.rect(0, h - 1.3*cm, w, 1.3*cm, fill=True, stroke=False)
        canvas_obj.setFillColor(COLOR_PINK)
        canvas_obj.rect(0, h - 1.3*cm, w, 0.22*cm, fill=True, stroke=False)

        canvas_obj.setFillColor(COLOR_WHITE)
        canvas_obj.setFont('Helvetica-Bold', 9)
        canvas_obj.drawString(1.5*cm, h - 0.9*cm, 'G2Fit Nutricion')
        cliente_nombre = self.datos.get('cliente', {}).get('nombre', '')
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.drawRightString(w - 1.5*cm, h - 0.9*cm, f'Plan nutricional: {cliente_nombre}')

        # Footer
        canvas_obj.setFillColor(COLOR_GRAY)
        canvas_obj.setFont('Helvetica', 7)
        fecha = self.datos.get('fecha_generacion', '')
        canvas_obj.drawString(1.5*cm, 0.7*cm, f'Confidencial - G2Fit Nutricion - {fecha}')
        canvas_obj.drawRightString(w - 1.5*cm, 0.7*cm, f'Pagina {doc.page}')

        canvas_obj.restoreState()

    # ─── PORTADA ────────────────────────────────────────────────────────────
    def _portada(self) -> list:
        cliente = self.datos.get('cliente', {})
        obj_nut = self.datos.get('objetivos_nutricionales', {})
        calculos = self.datos.get('calculos', {})
        elementos = []

        elementos.append(Spacer(1, 1.5*cm))
        elementos.append(Paragraph('G2FIT NUTRICION', self.estilo_titulo))
        elementos.append(Paragraph(
            'Plan Nutricional Personalizado - Mes Completo (4 Semanas, Lunes a Viernes)',
            ParagraphStyle('SubPrincipal', parent=self.estilo_titulo, fontSize=12, textColor=COLOR_PINK)
        ))
        elementos.append(HRFlowable(width='100%', thickness=2, color=COLOR_PINK, spaceAfter=16))
        elementos.append(Spacer(1, 0.3*cm))

        obj_label = {
            'perder_peso': 'Perdida de peso',
            'ganar_masa': 'Ganancia de masa muscular',
            'definicion': 'Definicion muscular',
            'mantener': 'Mantenimiento de peso'
        }.get(cliente.get('objetivo', ''), cliente.get('objetivo', '-'))

        apellidos = cliente.get('apellidos', '') or ''
        nombre_completo = f"{cliente.get('nombre', '-')} {apellidos}".strip()

        datos_portada = [
            ['DATOS DEL CLIENTE', ''],
            ['Nombre:', nombre_completo],
            ['Email:', cliente.get('email', '-')],
            ['Edad / Sexo:', f"{cliente.get('edad', '-')} anios / {cliente.get('sexo', '-').capitalize()}"],
            ['Peso actual:', f"{cliente.get('peso_actual', '-')} kg"],
            ['Altura:', f"{cliente.get('altura', '-')} cm"],
            ['IMC:', f"{cliente.get('imc', '-')} ({cliente.get('imc_categoria', '-')})"],
            ['Objetivo:', obj_label],
            ['Peso objetivo:', f"{cliente.get('peso_objetivo', 'No especificado')} kg"],
            ['Tiempo objetivo:', cliente.get('tiempo_objetivo', '-') or '-'],
        ]
        tabla_cliente = Table(datos_portada, colWidths=[5*cm, 12*cm])
        tabla_cliente.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_WHITE, COLOR_LIGHT]),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_PINK_GRID),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(tabla_cliente)
        elementos.append(Spacer(1, 0.6*cm))

        cals   = obj_nut.get('calorias')   or (calculos.get('objetivo') or {}).get('calorias', '-')
        prots  = obj_nut.get('proteinas')  or (calculos.get('objetivo') or {}).get('proteinas_g', '-')
        carbs  = obj_nut.get('carbohidratos') or (calculos.get('objetivo') or {}).get('carbohidratos_g', '-')
        grasas = obj_nut.get('grasas')     or (calculos.get('objetivo') or {}).get('grasas_g', '-')
        tmb    = calculos.get('tmb', '-')
        tdee   = calculos.get('tdee', '-')

        datos_obj = [
            ['OBJETIVOS NUTRICIONALES (Mifflin-St Jeor)', ''],
            ['TMB (Metabolismo basal):', f'{tmb} kcal/dia'],
            ['TDEE (Gasto total diario):', f'{tdee} kcal/dia'],
            ['Calorias objetivo:', f'{cals} kcal/dia'],
            ['Proteinas:', f'{prots} g/dia'],
            ['Carbohidratos:', f'{carbs} g/dia'],
            ['Grasas:', f'{grasas} g/dia'],
        ]
        tabla_obj = Table(datos_obj, colWidths=[5*cm, 12*cm])
        tabla_obj.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_PINK),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('SPAN', (0, 0), (-1, 0)),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_WHITE, COLOR_LIGHT]),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_PINK_GRID),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(tabla_obj)
        elementos.append(Spacer(1, 0.5*cm))

        # Restricciones
        alergias = cliente.get('alergias', []) or []
        intolerancias = cliente.get('intolerancias', []) or []
        if alergias or intolerancias:
            rest_data = [['RESTRICCIONES ALIMENTARIAS', '']]
            if alergias:
                rest_data.append(['Alergias:', ', '.join(alergias)])
            if intolerancias:
                rest_data.append(['Intolerancias:', ', '.join(intolerancias)])
            tabla_rest = Table(rest_data, colWidths=[5*cm, 12*cm])
            tabla_rest.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c2d12')),
                ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('SPAN', (0, 0), (-1, 0)),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#fff7ed'), colors.HexColor('#ffedd5')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fdba74')),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            elementos.append(tabla_rest)
            elementos.append(Spacer(1, 0.4*cm))

        # Notas especiales
        notas = (calculos or {}).get('notas_especiales', []) or []
        if notas:
            elementos.append(Paragraph('Consideraciones personalizadas para tu perfil:', self.estilo_bold))
            for nota in notas:
                elementos.append(Paragraph(f'  * {nota}', self.estilo_pequeno))
            elementos.append(Spacer(1, 0.3*cm))

        elementos.append(HRFlowable(width='100%', thickness=1, color=COLOR_PINK_GRID))
        elementos.append(Paragraph(
            f'Plan generado el {self.datos.get("fecha_generacion", "")} - G2Fit Nutricion',
            self.estilo_pequeno
        ))
        return elementos

    # ─── RESUMEN NUTRICIONAL ─────────────────────────────────────────────────
    def _resumen_nutricional(self) -> list:
        elementos = []
        elementos.append(Paragraph('RESUMEN DEL PLAN', self.estilo_subtitulo))
        elementos.append(HRFlowable(width='100%', thickness=2, color=COLOR_PINK, spaceAfter=10))

        cliente  = self.datos.get('cliente', {})
        calculos = self.datos.get('calculos', {})
        obj_nut  = self.datos.get('objetivos_nutricionales', {})

        cals   = obj_nut.get('calorias')      or (calculos.get('objetivo') or {}).get('calorias', '-')
        prots  = obj_nut.get('proteinas')     or (calculos.get('objetivo') or {}).get('proteinas_g', '-')
        carbs  = obj_nut.get('carbohidratos') or (calculos.get('objetivo') or {}).get('carbohidratos_g', '-')
        grasas = obj_nut.get('grasas')        or (calculos.get('objetivo') or {}).get('grasas_g', '-')

        info = [
            ['Duracion total:', '4 semanas (1 mes completo)'],
            ['Estructura:', '2 menus semanales distintos (semana 1=3, semana 2=4)'],
            ['Dias del plan:', 'Lunes a Viernes (5 dias/semana)'],
            ['Comidas por dia:', str(cliente.get('comidas_diarias', 5))],
            ['Calorias diarias:', f'{cals} kcal'],
            ['Proteinas diarias:', f'{prots} g'],
            ['Carbohidratos diarios:', f'{carbs} g'],
            ['Grasas diarias:', f'{grasas} g'],
            ['Alergias respetadas:', ', '.join(cliente.get('alergias', []) or []) or 'Ninguna'],
            ['Intolerancias:', ', '.join(cliente.get('intolerancias', []) or []) or 'Ninguna'],
        ]
        tabla = Table(info, colWidths=[5.5*cm, 11.5*cm])
        tabla.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [COLOR_WHITE, COLOR_LIGHT]),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_PINK_GRID),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.5*cm))

        # Distribución por comida
        dist = (calculos or {}).get('distribucion_por_comida', {}) or {}
        if dist:
            elementos.append(Paragraph('Distribucion de macros por comida', self.estilo_bold))
            elementos.append(Spacer(1, 0.2*cm))
            dist_data = [['Comida', 'Calorias', 'Proteinas', 'Carbos', 'Grasas']]
            for nombre, m in dist.items():
                dist_data.append([
                    nombre,
                    f"{m.get('calorias', '-')} kcal",
                    f"{m.get('proteinas', '-')}g",
                    f"{m.get('carbohidratos', '-')}g",
                    f"{m.get('grasas', '-')}g",
                ])
            tabla_dist = Table(dist_data, colWidths=[4*cm, 3*cm, 3*cm, 3*cm, 3*cm])
            tabla_dist.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_PINK),
                ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_WHITE, COLOR_LIGHT]),
                ('GRID', (0, 0), (-1, -1), 0.3, COLOR_PINK_GRID),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            elementos.append(tabla_dist)
        return elementos

    # ─── PLAN 4 SEMANAS ──────────────────────────────────────────────────────
    def _plan_4_semanas(self) -> list:
        elementos = []
        elementos.append(Paragraph('PLAN DE ALIMENTACION - 4 SEMANAS (LUNES A VIERNES)', self.estilo_subtitulo))
        elementos.append(HRFlowable(width='100%', thickness=2, color=COLOR_PINK, spaceAfter=8))
        elementos.append(Paragraph(
            'El plan consta de 2 menus semanales distintos que se repiten durante el mes: '
            'Semana 1 = Semana 3  |  Semana 2 = Semana 4',
            self.estilo_pequeno
        ))
        elementos.append(Spacer(1, 0.3*cm))

        semanas_base = self.datos.get('plan_semanal', []) or []
        if not semanas_base:
            elementos.append(Paragraph('No hay datos del plan disponibles.', self.estilo_normal))
            return elementos

        def get_dias(sem):
            return sem.get('dias', []) if isinstance(sem, dict) else []

        semana_a = semanas_base[0] if len(semanas_base) > 0 else {}
        semana_b = semanas_base[1] if len(semanas_base) > 1 else semanas_base[0]

        orden = [(1, semana_a, 'A'), (2, semana_b, 'B'), (3, semana_a, 'A'), (4, semana_b, 'B')]
        dias_nombres = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']

        for num_semana, semana_obj, letra in orden:
            if num_semana > 1:
                elementos.append(PageBreak())
            elementos.append(Paragraph(f'SEMANA {num_semana}  (menu {letra})', self.estilo_semana))
            elementos.append(Spacer(1, 0.3*cm))

            dias = get_dias(semana_obj)
            for i, dia in enumerate(dias[:5]):
                nombre_dia = dia.get('nombre_dia') or (dias_nombres[i] if i < 5 else f'Dia {i+1}')
                elementos.append(Paragraph(f'-- {nombre_dia.upper()} --', self.estilo_dia))

                comidas = dia.get('comidas', []) or []
                if not comidas:
                    elementos.append(Paragraph('Sin datos de comidas', self.estilo_pequeno))
                    continue

                tabla_datos = [['Comida', 'Plato / Ingredientes principales', 'Kcal', 'Prot.', 'Carb.', 'Grasa']]
                for comida in comidas:
                    ingr = comida.get('ingredientes', []) or []
                    ingr_str = ', '.join(str(x) for x in ingr[:4])
                    if len(ingr) > 4:
                        ingr_str += '...'
                    nombre_plato = comida.get('nombre', '-')
                    celda_plato = f"{nombre_plato}\n{ingr_str}" if ingr_str else nombre_plato
                    tabla_datos.append([
                        comida.get('tipo', comida.get('nombre', '-')),
                        celda_plato,
                        str(comida.get('calorias', '-')),
                        f"{comida.get('proteinas', '-')}g",
                        f"{comida.get('carbohidratos', '-')}g",
                        f"{comida.get('grasas', '-')}g",
                    ])

                totales = dia.get('totales_dia', {}) or {}
                tabla_datos.append([
                    'TOTAL', '',
                    str(totales.get('calorias', '-')),
                    f"{totales.get('proteinas', '-')}g",
                    f"{totales.get('carbohidratos', '-')}g",
                    f"{totales.get('grasas', '-')}g",
                ])

                tabla = Table(tabla_datos, colWidths=[3*cm, 7.5*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm])
                tabla.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
                    ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [COLOR_WHITE, COLOR_LIGHT]),
                    ('BACKGROUND', (0, -1), (-1, -1), COLOR_PINK),
                    ('TEXTCOLOR', (0, -1), (-1, -1), COLOR_WHITE),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 0.3, COLOR_PINK_GRID),
                    ('PADDING', (0, 0), (-1, -1), 4),
                    ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                elementos.append(tabla)
                elementos.append(Spacer(1, 0.35*cm))

        return elementos

    # ─── RECOMENDACIONES ────────────────────────────────────────────────────
    def _recomendaciones(self) -> list:
        elementos = []
        elementos.append(PageBreak())
        elementos.append(Paragraph('RECOMENDACIONES GENERALES', self.estilo_subtitulo))
        elementos.append(HRFlowable(width='100%', thickness=2, color=COLOR_PINK, spaceAfter=10))

        cliente  = self.datos.get('cliente', {})
        calculos = self.datos.get('calculos', {}) or {}
        peso     = cliente.get('peso_actual', 70) or 70

        recomendaciones = [
            f'Hidratacion: {round(peso * 35)} ml de agua al dia (base {peso} kg x 35 ml).',
            'Distribuye la proteina de forma EQUITATIVA en todas las comidas.',
            'Incluye verduras en todas las comidas principales. Varia los colores: verde, rojo/naranja, blanco.',
            'Prioriza carbohidratos de bajo indice glucemico: arroz integral, quinoa, boniato, avena, pasta integral.',
            'Usa aceite de oliva virgen extra como grasa principal de cocina.',
            'Mantener horarios regulares de comidas para regular el metabolismo.',
            'Las semanas 1 y 3 son el mismo menu; las semanas 2 y 4 son el mismo menu.',
            'Si un dia fallas, continua con normalidad al dia siguiente. La consistencia es lo que importa.',
            'El plan se disenyo para complementarse con tu nivel de actividad fisica habitual.',
            'Descansa 7-9 horas cada noche: el sueno es fundamental para los resultados.',
        ]

        for nota in calculos.get('notas_especiales', []) or []:
            recomendaciones.append(nota)

        for rec in recomendaciones:
            elementos.append(Paragraph(f'* {rec}', self.estilo_normal))

        alertas = calculos.get('alertas', []) or []
        if alertas:
            elementos.append(Spacer(1, 0.3*cm))
            elementos.append(Paragraph('ALERTAS:', self.estilo_alerta))
            for alerta in alertas:
                elementos.append(Paragraph(f'! {alerta}', self.estilo_alerta))

        elementos.append(Spacer(1, 0.5*cm))
        return elementos

    # ─── DISCLAIMER ─────────────────────────────────────────────────────────
    def _disclaimer(self) -> list:
        elementos = []
        elementos.append(HRFlowable(width='100%', thickness=1, color=COLOR_GRAY, spaceAfter=8))
        elementos.append(Paragraph('AVISO LEGAL', ParagraphStyle(
            'DisclaimerTitle', parent=self.estilo_bold, fontSize=9, textColor=COLOR_GRAY
        )))
        texto = (
            'Este plan nutricional ha sido elaborado de forma personalizada por un profesional titulado en '
            'Dietetica y Nutricion. La informacion es confidencial y destinada exclusivamente a la persona '
            'indicada. No constituye consejo medico. Si padeces alguna patologia, consulta con tu medico '
            'antes de iniciar cualquier plan alimenticio. '
            'G2Fit Nutricion no se responsabiliza del uso inadecuado de este documento.'
        )
        elementos.append(Paragraph(texto, self.estilo_disclaimer))
        elementos.append(Paragraph(
            f'(c) {datetime.now().year} G2Fit Nutricion | g2fit.es | Todos los derechos reservados',
            self.estilo_disclaimer
        ))
        return elementos


# ============================================================
# ENTRYPOINT
# ============================================================
def main():
    if len(sys.argv) < 3:
        print("Uso: python3 generar_pdf_dieta.py '<json_datos>' '<ruta_output>'", file=sys.stderr)
        sys.exit(1)

    json_str = sys.argv[1]
    ruta_output = sys.argv[2]

    try:
        datos = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON invalido - {str(e)}", file=sys.stderr)
        sys.exit(1)

    if not datos:
        print("ERROR: Los datos estan vacios", file=sys.stderr)
        sys.exit(1)

    generador = GeneradorPDFDieta(datos, ruta_output)
    exito = generador.generar()

    if exito:
        print(json.dumps({"success": True, "path": ruta_output}))
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
