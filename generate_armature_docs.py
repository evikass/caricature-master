#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор технической документации для каркасов кукольной анимации
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon
from reportlab.graphics import renderPDF
import os

# Регистрация шрифтов
pdfmetrics.registerFont(TTFont('SimHei', '/usr/share/fonts/truetype/chinese/SimHei.ttf'))
pdfmetrics.registerFont(TTFont('Microsoft YaHei', '/usr/share/fonts/truetype/chinese/msyh.ttf'))
pdfmetrics.registerFont(TTFont('Times New Roman', '/usr/share/fonts/truetype/english/Times-New-Roman.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))

registerFontFamily('Microsoft YaHei', normal='Microsoft YaHei', bold='Microsoft YaHei')
registerFontFamily('SimHei', normal='SimHei', bold='SimHei')
registerFontFamily('Times New Roman', normal='Times New Roman', bold='Times New Roman')

# Цвета
BLUE_DARK = colors.HexColor('#1F4E79')
BLUE_LIGHT = colors.HexColor('#2E75B6')
GRAY_LIGHT = colors.HexColor('#F5F5F5')
RED_ACCENT = colors.HexColor('#C00000')

def create_styles():
    """Создание стилей документа"""
    styles = getSampleStyleSheet()
    
    # Стиль заголовка документа
    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName='Microsoft YaHei',
        fontSize=32,
        leading=40,
        alignment=TA_CENTER,
        textColor=BLUE_DARK,
        spaceAfter=20
    ))
    
    # Стиль подзаголовка
    styles.add(ParagraphStyle(
        name='DocSubtitle',
        fontName='SimHei',
        fontSize=16,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.gray,
        spaceAfter=30
    ))
    
    # Заголовок H1
    styles.add(ParagraphStyle(
        name='H1',
        fontName='Microsoft YaHei',
        fontSize=20,
        leading=26,
        alignment=TA_LEFT,
        textColor=BLUE_DARK,
        spaceBefore=20,
        spaceAfter=12
    ))
    
    # Заголовок H2
    styles.add(ParagraphStyle(
        name='H2',
        fontName='Microsoft YaHei',
        fontSize=16,
        leading=22,
        alignment=TA_LEFT,
        textColor=BLUE_LIGHT,
        spaceBefore=16,
        spaceAfter=8
    ))
    
    # Заголовок H3
    styles.add(ParagraphStyle(
        name='H3',
        fontName='Microsoft YaHei',
        fontSize=13,
        leading=18,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=6
    ))
    
    # Основной текст
    styles.add(ParagraphStyle(
        name='Body',
        fontName='SimHei',
        fontSize=11,
        leading=18,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=0,
        spaceAfter=8,
        wordWrap='CJK'
    ))
    
    # Стиль для таблиц
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='SimHei',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        wordWrap='CJK'
    ))
    
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='SimHei',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.white,
        wordWrap='CJK'
    ))
    
    # Подпись к рисунку
    styles.add(ParagraphStyle(
        name='Caption',
        fontName='SimHei',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.gray,
        spaceBefore=6,
        spaceAfter=12
    ))
    
    # Примечание
    styles.add(ParagraphStyle(
        name='Note',
        fontName='SimHei',
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        textColor=colors.gray,
        leftIndent=20,
        spaceBefore=6,
        spaceAfter=6,
        wordWrap='CJK'
    ))
    
    return styles


def create_ball_joint_drawing(width=160*mm, height=100*mm):
    """Создание чертежа шарового соединения"""
    d = Drawing(width, height)
    
    # Центр чертежа
    cx, cy = width/2, height/2
    
    # Размеры
    ball_radius = 15*mm
    socket_outer_radius = 20*mm
    socket_inner_radius = 16*mm
    stem_length = 25*mm
    stem_radius = 4*mm
    
    # === ВИД СПЕРЕДИ (слева) ===
    view1_x = width/4
    
    # Гнездо (внешний контур)
    d.add(Circle(view1_x, cy, socket_outer_radius, 
                 fillColor=GRAY_LIGHT, strokeColor=colors.black, strokeWidth=1))
    
    # Гнездо (внутренний контур - отверстие)
    d.add(Circle(view1_x, cy, socket_inner_radius,
                 fillColor=colors.white, strokeColor=colors.black, strokeWidth=0.5))
    
    # Стержень гнезда
    d.add(Rect(view1_x - stem_radius, cy - socket_outer_radius - stem_length,
               stem_radius*2, stem_length,
               fillColor=GRAY_LIGHT, strokeColor=colors.black, strokeWidth=1))
    
    # Шар (сечение)
    ball_x = view1_x + 50*mm
    d.add(Circle(ball_x, cy, ball_radius,
                 fillColor=BLUE_LIGHT, strokeColor=colors.black, strokeWidth=1))
    
    # Отверстие в шаре
    hole_radius = 2*mm
    d.add(Circle(ball_x, cy, hole_radius,
                 fillColor=colors.white, strokeColor=colors.black, strokeWidth=0.5))
    
    # Размерные линии
    # Диаметр шара
    d.add(Line(ball_x + ball_radius + 5, cy - ball_radius,
               ball_x + ball_radius + 5, cy + ball_radius,
               strokeColor=RED_ACCENT, strokeWidth=0.5))
    d.add(Line(ball_x + ball_radius + 3, cy - ball_radius,
               ball_x + ball_radius + 7, cy - ball_radius,
               strokeColor=RED_ACCENT, strokeWidth=0.5))
    d.add(Line(ball_x + ball_radius + 3, cy + ball_radius,
               ball_x + ball_radius + 7, cy + ball_radius,
               strokeColor=RED_ACCENT, strokeWidth=0.5))
    
    # Подписи
    d.add(String(view1_x, cy + socket_outer_radius + 10, 'Гнездо (Socket)',
                 fontName='SimHei', fontSize=9, textAnchor='middle'))
    d.add(String(ball_x, cy + ball_radius + 10, 'Шар (Ball)',
                 fontName='SimHei', fontSize=9, textAnchor='middle'))
    
    # Размер D
    d.add(String(ball_x + ball_radius + 15, cy, 'D=6мм',
                 fontName='SimHei', fontSize=8, textAnchor='start'))
    
    return d


def create_hinge_joint_drawing(width=160*mm, height=80*mm):
    """Создание чертежа шарнирного соединения (петля)"""
    d = Drawing(width, height)
    
    cx, cy = width/2, height/2
    
    # Параметры
    outer_radius = 8*mm
    inner_radius = 5*mm
    thickness = 4*mm
    gap = 0.3*mm
    
    # Часть A (с пазом)
    part_a_x = width/4
    d.add(Circle(part_a_x, cy, outer_radius,
                 fillColor=GRAY_LIGHT, strokeColor=colors.black, strokeWidth=1))
    d.add(Circle(part_a_x, cy, inner_radius,
                 fillColor=colors.white, strokeColor=colors.black, strokeWidth=0.5))
    
    # Часть B (выступ)
    part_b_x = width*3/4
    d.add(Circle(part_b_x, cy, inner_radius - 0.5*mm,
                 fillColor=BLUE_LIGHT, strokeColor=colors.black, strokeWidth=1))
    
    # Стрелка показывающая соединение
    d.add(Line(part_a_x + outer_radius + 5, cy,
               part_b_x - inner_radius - 5, cy,
               strokeColor=colors.gray, strokeWidth=0.5, strokeDashArray=[3,3]))
    
    # Подписи
    d.add(String(part_a_x, cy - outer_radius - 10, 'Часть A',
                 fontName='SimHei', fontSize=9, textAnchor='middle'))
    d.add(String(part_b_x, cy - outer_radius - 10, 'Часть B',
                 fontName='SimHei', fontSize=9, textAnchor='middle'))
    
    return d


def create_armature_skeleton_drawing(width=160*mm, height=180*mm):
    """Создание схемы гуманоидного каркаса"""
    d = Drawing(width, height)
    
    # Центр
    cx = width/2
    
    # Пропорции тела (в мм)
    head_r = 12*mm
    neck_h = 8*mm
    torso_w = 35*mm
    torso_h = 40*mm
    pelvis_w = 25*mm
    pelvis_h = 15*mm
    
    # Масштаб для размещения на чертеже
    scale = 1.2
    y_start = height - 20*mm
    
    # Координаты joints
    joints = {
        'head': (cx, y_start - head_r*scale),
        'neck': (cx, y_start - 2*head_r*scale - neck_h*scale/2),
        'shoulder_L': (cx - torso_w*scale/2 - 5*mm, y_start - 2*head_r*scale - 10*mm),
        'shoulder_R': (cx + torso_w*scale/2 + 5*mm, y_start - 2*head_r*scale - 10*mm),
        'elbow_L': (cx - torso_w*scale/2 - 25*mm, y_start - 2*head_r*scale - 25*mm),
        'elbow_R': (cx + torso_w*scale/2 + 25*mm, y_start - 2*head_r*scale - 25*mm),
        'wrist_L': (cx - torso_w*scale/2 - 45*mm, y_start - 2*head_r*scale - 40*mm),
        'wrist_R': (cx + torso_w*scale/2 + 45*mm, y_start - 2*head_r*scale - 40*mm),
        'hip_L': (cx - 10*mm, y_start - 2*head_r*scale - torso_h*scale - neck_h*scale),
        'hip_R': (cx + 10*mm, y_start - 2*head_r*scale - torso_h*scale - neck_h*scale),
        'knee_L': (cx - 10*mm, y_start - 2*head_r*scale - torso_h*scale - neck_h*scale - 35*mm),
        'knee_R': (cx + 10*mm, y_start - 2*head_r*scale - torso_h*scale - neck_h*scale - 35*mm),
        'ankle_L': (cx - 10*mm, y_start - 2*head_r*scale - torso_h*scale - neck_h*scale - 70*mm),
        'ankle_R': (cx + 10*mm, y_start - 2*head_r*scale - torso_h*scale - neck_h*scale - 70*mm),
    }
    
    # Рисуем голову
    d.add(Circle(joints['head'][0], joints['head'][1], head_r*scale,
                 fillColor=GRAY_LIGHT, strokeColor=colors.black, strokeWidth=1))
    d.add(String(joints['head'][0], joints['head'][1], 'Г',
                 fontName='SimHei', fontSize=10, textAnchor='middle'))
    
    # Шея
    neck_y = (joints['head'][1] + joints['neck'][1])/2
    d.add(Rect(cx - 3*mm, neck_y - neck_h*scale/2, 6*mm, neck_h*scale,
               fillColor=GRAY_LIGHT, strokeColor=colors.black, strokeWidth=1))
    
    # Торс
    torso_top = joints['neck'][1] - 5*mm
    torso_bottom = torso_top - torso_h*scale
    d.add(Rect(cx - torso_w*scale/2, torso_bottom, torso_w*scale, torso_h*scale,
               fillColor=GRAY_LIGHT, strokeColor=colors.black, strokeWidth=1))
    d.add(String(cx, (torso_top + torso_bottom)/2, 'Торс',
                 fontName='SimHei', fontSize=8, textAnchor='middle'))
    
    # Таз
    pelvis_top = torso_bottom
    pelvis_bottom = pelvis_top - pelvis_h*scale
    d.add(Rect(cx - pelvis_w*scale/2, pelvis_bottom, pelvis_w*scale, pelvis_h*scale,
               fillColor=GRAY_LIGHT, strokeColor=colors.black, strokeWidth=1))
    
    # Кости конечностей (линии)
    bone_color = BLUE_LIGHT
    bone_width = 2
    
    # Руки
    for side in ['L', 'R']:
        sign = -1 if side == 'L' else 1
        # Плечо -> локоть
        d.add(Line(joints[f'shoulder_{side}'][0], joints[f'shoulder_{side}'][1],
                   joints[f'elbow_{side}'][0], joints[f'elbow_{side}'][1],
                   strokeColor=bone_color, strokeWidth=bone_width))
        # Локоть -> запястье
        d.add(Line(joints[f'elbow_{side}'][0], joints[f'elbow_{side}'][1],
                   joints[f'wrist_{side}'][0], joints[f'wrist_{side}'][1],
                   strokeColor=bone_color, strokeWidth=bone_width))
    
    # Ноги
    for side in ['L', 'R']:
        # Бедро -> колено
        d.add(Line(joints[f'hip_{side}'][0], joints[f'hip_{side}'][1],
                   joints[f'knee_{side}'][0], joints[f'knee_{side}'][1],
                   strokeColor=bone_color, strokeWidth=bone_width))
        # Колено -> лодыжка
        d.add(Line(joints[f'knee_{side}'][0], joints[f'knee_{side}'][1],
                   joints[f'ankle_{side}'][0], joints[f'ankle_{side}'][1],
                   strokeColor=bone_color, strokeWidth=bone_width))
    
    # Суставы (кружочки)
    joint_radius = 3*mm
    for name, pos in joints.items():
        if name != 'head':
            d.add(Circle(pos[0], pos[1], joint_radius,
                         fillColor=RED_ACCENT, strokeColor=colors.black, strokeWidth=0.5))
    
    # Подписи суставов
    d.add(String(joints['shoulder_L'][0] - 15, joints['shoulder_L'][1] + 10, 
                 'Плечо', fontName='SimHei', fontSize=7, textAnchor='middle'))
    d.add(String(joints['elbow_L'][0] - 15, joints['elbow_L'][1], 
                 'Локоть', fontName='SimHei', fontSize=7, textAnchor='end'))
    d.add(String(joints['hip_L'][0] - 15, joints['hip_L'][1], 
                 'Бедро', fontName='SimHei', fontSize=7, textAnchor='end'))
    d.add(String(joints['knee_L'][0] - 15, joints['knee_L'][1], 
                 'Колено', fontName='SimHei', fontSize=7, textAnchor='end'))
    
    # Легенда
    legend_y = 15*mm
    d.add(Rect(10*mm, legend_y - 3*mm, 6*mm, 6*mm, fillColor=RED_ACCENT, strokeColor=colors.black, strokeWidth=0.5))
    d.add(String(20*mm, legend_y, 'Сустав (Ball/Socket)', fontName='SimHei', fontSize=8))
    
    d.add(Line(80*mm, legend_y, 90*mm, legend_y, strokeColor=bone_color, strokeWidth=2))
    d.add(String(95*mm, legend_y, 'Кость (Strut)', fontName='SimHei', fontSize=8))
    
    return d


def create_dimension_table(styles):
    """Создание таблицы размеров компонентов"""
    
    header_style = styles['TableHeader']
    cell_style = styles['TableCell']
    
    data = [
        [Paragraph('<b>Компонент</b>', header_style),
         Paragraph('<b>Параметр</b>', header_style),
         Paragraph('<b>Значение (мм)</b>', header_style),
         Paragraph('<b>Примечание</b>', header_style)],
        
        [Paragraph('Шаровой сустав', cell_style),
         Paragraph('D шара', cell_style),
         Paragraph('6.0', cell_style),
         Paragraph('Стандартный', cell_style)],
        
        [Paragraph('', cell_style),
         Paragraph('D гнезда внутр.', cell_style),
         Paragraph('6.15', cell_style),
         Paragraph('Зазор 0.15мм', cell_style)],
        
        [Paragraph('', cell_style),
         Paragraph('Толщина стенки', cell_style),
         Paragraph('1.5', cell_style),
         Paragraph('Минимум для SLA', cell_style)],
        
        [Paragraph('Кость/стержень', cell_style),
         Paragraph('Диаметр', cell_style),
         Paragraph('2.5 - 4.0', cell_style),
         Paragraph('Зависит от размера', cell_style)],
        
        [Paragraph('', cell_style),
         Paragraph('Отверстие', cell_style),
         Paragraph('1.0', cell_style),
         Paragraph('Под проволоку', cell_style)],
        
        [Paragraph('Шарнир (hinge)', cell_style),
         Paragraph('D внешний', cell_style),
         Paragraph('8.0', cell_style),
         Paragraph('', cell_style)],
        
        [Paragraph('', cell_style),
         Paragraph('D внутренний', cell_style),
         Paragraph('5.0', cell_style),
         Paragraph('', cell_style)],
        
        [Paragraph('Торс', cell_style),
         Paragraph('Ширина', cell_style),
         Paragraph('25 - 40', cell_style),
         Paragraph('', cell_style)],
        
        [Paragraph('', cell_style),
         Paragraph('Высота', cell_style),
         Paragraph('35 - 50', cell_style),
         Paragraph('', cell_style)],
    ]
    
    table = Table(data, colWidths=[3*cm, 3.5*cm, 3*cm, 4*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),
        ('BACKGROUND', (0, 2), (-1, 2), GRAY_LIGHT),
        ('BACKGROUND', (0, 3), (-1, 3), colors.white),
        ('BACKGROUND', (0, 4), (-1, 4), GRAY_LIGHT),
        ('BACKGROUND', (0, 5), (-1, 5), colors.white),
        ('BACKGROUND', (0, 6), (-1, 6), GRAY_LIGHT),
        ('BACKGROUND', (0, 7), (-1, 7), colors.white),
        ('BACKGROUND', (0, 8), (-1, 8), GRAY_LIGHT),
        ('BACKGROUND', (0, 9), (-1, 9), colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    return table


def create_print_settings_table(styles):
    """Таблица настроек печати для SLA"""
    
    header_style = styles['TableHeader']
    cell_style = styles['TableCell']
    
    data = [
        [Paragraph('<b>Параметр</b>', header_style),
         Paragraph('<b>Рекомендуемое значение</b>', header_style),
         Paragraph('<b>Примечание</b>', header_style)],
        
        [Paragraph('Слой печати', cell_style),
         Paragraph('0.025 - 0.05 мм', cell_style),
         Paragraph('Высокое разрешение', cell_style)],
        
        [Paragraph('Зазор для движения', cell_style),
         Paragraph('0.15 - 0.20 мм', cell_style),
         Paragraph('Для свободного хода', cell_style)],
        
        [Paragraph('Толщина стенки мин.', cell_style),
         Paragraph('1.0 - 1.5 мм', cell_style),
         Paragraph('Зависит от смолы', cell_style)],
        
        [Paragraph('Поддержки', cell_style),
         Paragraph('Лёгкие/Средние', cell_style),
         Paragraph('Минимизировать следы', cell_style)],
        
        [Paragraph('Ориентация', cell_style),
         Paragraph('Суставы вниз', cell_style),
         Paragraph('Лучшее качество', cell_style)],
        
        [Paragraph('Постобработка', cell_style),
         Paragraph('UV + Промывка', cell_style),
         Paragraph('По инструкции смолы', cell_style)],
    ]
    
    table = Table(data, colWidths=[4*cm, 5*cm, 5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),
        ('BACKGROUND', (0, 2), (-1, 2), GRAY_LIGHT),
        ('BACKGROUND', (0, 3), (-1, 3), colors.white),
        ('BACKGROUND', (0, 4), (-1, 4), GRAY_LIGHT),
        ('BACKGROUND', (0, 5), (-1, 5), colors.white),
        ('BACKGROUND', (0, 6), (-1, 6), GRAY_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    return table


def build_document():
    """Сборка PDF документа"""
    
    output_path = '/home/z/my-project/download/puppet_armature_guide.pdf'
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title='Puppet Armature Guide',
        author='Z.ai',
        creator='Z.ai',
        subject='Техническое руководство по каркасам для кукольной анимации'
    )
    
    styles = create_styles()
    story = []
    
    # ===== ТИТУЛЬНАЯ СТРАНИЦА =====
    story.append(Spacer(1, 50*mm))
    story.append(Paragraph('КАРКАСЫ ДЛЯ КУКОЛЬНОЙ АНИМАЦИИ', styles['DocTitle']))
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph('Техническое руководство и чертежи<br/>для 3D-печати на SLA принтерах', styles['DocSubtitle']))
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph('Версия 1.0', styles['DocSubtitle']))
    story.append(Paragraph('Super Z AI Assistant', styles['DocSubtitle']))
    story.append(PageBreak())
    
    # ===== СОДЕРЖАНИЕ =====
    story.append(Paragraph('СОДЕРЖАНИЕ', styles['H1']))
    story.append(Spacer(1, 5*mm))
    
    toc_items = [
        ('1. Введение', 'Обзор технологии и область применения'),
        ('2. Типы шарнирных соединений', 'Шаровые, шарнирные и универсальные суставы'),
        ('3. Компоненты каркаса', 'Детальное описание всех частей'),
        ('4. Технические чертежи', 'Геометрия и размеры'),
        ('5. Настройки SLA печати', 'Рекомендации по печати'),
        ('6. Сборка и монтаж', 'Инструкции по сборке'),
        ('7. Blender скрипт', 'Использование генератора моделей'),
    ]
    
    for title, desc in toc_items:
        story.append(Paragraph(f'<b>{title}</b>', styles['Body']))
        story.append(Paragraph(f'    {desc}', styles['Note']))
    
    story.append(PageBreak())
    
    # ===== 1. ВВЕДЕНИЕ =====
    story.append(Paragraph('1. ВВЕДЕНИЕ', styles['H1']))
    
    story.append(Paragraph(
        'Каркасы для кукольной анимации (puppet armatures) представляют собой сложные механические системы, '
        'обеспечивающие подвижность и устойчивость анимационных кукол. Качественный каркас является основой '
        'любого stop-motion проекта, позволяя аниматору точно позиционировать персонажа и фиксировать '
        'необходимые позы на протяжении множества кадров съёмки. Современные технологии SLA 3D-печати '
        'открывают новые возможности для создания прецизионных шарнирных соединений с точностью до 25 микрон.',
        styles['Body']
    ))
    
    story.append(Paragraph(
        'Данное руководство содержит полную техническую документацию для самостоятельного изготовления '
        'каркасов кукол различной сложности: от простых моделей для начинающих аниматоров до профессиональных '
        'систем с большим количеством степеней свободы. Все чертежи и модели оптимизированы для печати на '
        'SLA принтерах с учётом особенностей фотополимерных смол и требований к минимальной толщине стенок. '
        'Прилагаемый Blender Python скрипт позволяет генерировать готовые 3D модели с настраиваемыми параметрами.',
        styles['Body']
    ))
    
    story.append(Paragraph('1.1 Область применения', styles['H2']))
    story.append(Paragraph(
        'Разработанные каркасы предназначены для использования в следующих областях кукольной анимации: '
        'создание stop-motion фильмов и сериалов с покадровой съёмкой; производство рекламных роликов '
        'с анимированными персонажами; театральные постановки с кукольными актёрами; художественные '
        'инсталляции и интерактивные экспонаты; образовательные проекты по анимации; прототипирование '
        'персонажей для последующего тиражирования. Модульная система соединений позволяет адаптировать '
        'базовые конструкции под конкретные требования проекта.',
        styles['Body']
    ))
    
    story.append(Paragraph('1.2 Преимущества SLA технологии', styles['H2']))
    story.append(Paragraph(
        'Стереолитографическая 3D-печать (SLA) обладает рядом критических преимуществ для производства '
        'шарнирных соединений кукольных каркасов. Высокое разрешение печати (до 25 мкм) обеспечивает '
        'прецизионную геометрию шаровых и шарнирных сочленений, критически важную для плавности движения. '
        'Фотополимерные смолы позволяют создавать детали с гладкой поверхностью без слоистости, характерной '
        'для FDM печати, что существенно снижает трение в суставах. Возможность печати сложных геометрий '
        'с внутренними полостями позволяет создавать лёгкие, но прочные компоненты с продуманной топологией. '
        'Разнообразие материалов включает прочные, гибкие и износостойкие смолы для различных типов нагрузки.',
        styles['Body']
    ))
    
    story.append(PageBreak())
    
    # ===== 2. ТИПЫ ШАРНИРНЫХ СОЕДИНЕНИЙ =====
    story.append(Paragraph('2. ТИПЫ ШАРНИРНЫХ СОЕДИНЕНИЙ', styles['H1']))
    
    story.append(Paragraph('2.1 Шаровые соединения (Ball-and-Socket)', styles['H2']))
    story.append(Paragraph(
        'Шаровые соединения представляют собой наиболее универсальный тип суставов для кукольной анимации. '
        'Конструкция состоит из сферического элемента (шара) и охватывающего его гнезда с hemisphere cut. '
        'Такая геометрия обеспечивает три степени свободы: сгибание-разгибание, отведение-приведение, '
        'и вращение вокруг продольной оси. Плавность движения и сила удержания позиции регулируются '
        'соотношением диаметров шара и гнезда, а также трением поверхностей. Для типичных кукол высотой '
        '200-300 мм оптимальный диаметр шара составляет 4-8 мм с зазором 0.15-0.20 мм для свободного хода.',
        styles['Body']
    ))
    
    story.append(Paragraph(
        'Применение шаровых соединений: шейный отдел (обеспечивает поворот и наклон головы); плечевые суставы '
        '(максимальная подвижность руки); тазобедренные суставы (поддержка веса и движение ноги); запястные '
        'и голеностопные суставы (точная ориентация кисти и стопы). Ключевое преимущество шаровых соединений — '
        'компактность при большом диапазоне движений, что критично для кукольных персонажей ограниченного размера.',
        styles['Body']
    ))
    
    # Чертёж шарового соединения
    story.append(Spacer(1, 5*mm))
    ball_drawing = create_ball_joint_drawing()
    story.append(ball_drawing)
    story.append(Paragraph('Рис. 1. Шаровое соединение (Ball-and-Socket Joint): гнездо с входным отверстием и шар', 
                           styles['Caption']))
    
    story.append(Paragraph('2.2 Шарнирные соединения (Hinge Joints)', styles['H2']))
    story.append(Paragraph(
        'Шарнирные соединения ограничивают движение одной плоскостью, обеспечивая сгибание и разгибание '
        'вокруг фиксированной оси. Конструкция состоит из двух сопрягаемых цилиндрических элементов: '
        'внешнего с пазом и внутреннего с выступом. Одноосевая геометрия обеспечивает более высокую '
        'жёсткость в направлении перпендикулярном оси вращения по сравнению с шаровыми соединениями '
        'аналогичного размера. Это делает шарниры оптимальным выбором для суставов с преобладающим '
        'плоским движением: локтевых, коленных, фаланг пальцев. Типичный диаметр шарнира для локтя '
        'куклы 250 мм составляет 6-8 мм с толщиной элементов 3-4 мм.',
        styles['Body']
    ))
    
    # Чертёж шарнирного соединения
    story.append(Spacer(1, 5*mm))
    hinge_drawing = create_hinge_joint_drawing()
    story.append(hinge_drawing)
    story.append(Paragraph('Рис. 2. Шарнирное соединение (Hinge Joint): части A и B для одноплоскостного движения',
                           styles['Caption']))
    
    story.append(PageBreak())
    
    # ===== 3. КОМПОНЕНТЫ КАРКАСА =====
    story.append(Paragraph('3. КОМПОНЕНТЫ КАРКАСА', styles['H1']))
    
    story.append(Paragraph('3.1 Осевой скелет (Axial Skeleton)', styles['H2']))
    story.append(Paragraph(
        'Осевой скелет составляет структурную основу куклы и включает голову, шею, торс и таз. '
        'Голова выполняется в виде полой сферы или эллипсоида с креплением для лицевой пластины '
        '(replacement face system) или подвижной челюсти. Шейный модуль содержит шаровое соединение '
        'с вертикальным стержнем, проходящим через торс к тазу — эта конструкция обеспечивает '
        'жёсткость позвоночника при сохранении подвижности шеи. Торс изготавливается из лёгкого '
        'каркаса с монтажными площадками для плечевых и тазобедренных суставов. Таз служит центральным '
        'узлом соединения ног и поддержки всей конструкции в вертикальном положении.',
        styles['Body']
    ))
    
    story.append(Paragraph('3.2 Верхние конечности', styles['H2']))
    story.append(Paragraph(
        'Верхняя конечность состоит из плечевого сустава (шаровой), плечевой кости (стержень), '
        'локтевого сустава (шарнирный или шаровый), лучевой кости (стержень), запястного сустава '
        '(шаровой) и кисти. Плечевой сустав монтируется на торсе с возможностью регулировки положения '
        'в пределах 10-15 мм для настройки пропорций. Плечевая и лучевая кости изготавливаются из '
        'полых стержней диаметром 3-4 мм с внутренним каналом для проводки арматуры. Кисть выполняется '
        'как единый модуль с суставами пальцев либо снабжается сменными положениями (replacement hands). '
        'Общая длина руки для куклы 250 мм составляет 90-110 мм от плеча до кончиков пальцев.',
        styles['Body']
    ))
    
    story.append(Paragraph('3.3 Нижние конечности', styles['H2']))
    story.append(Paragraph(
        'Нижняя конечность обеспечивает опорную функцию и включает тазобедренный сустав (шаровой), '
        'бедренную кость (стержень), коленный сустав (шарнирный), большеберцовую кость (стержень), '
        'голеностопный сустав (шаровой) и стопу. Тазобедренные суставы несут основную нагрузку веса '
        'куклы и требуют увеличенного диаметра шара (8-10 мм для куклы 250 мм). Коленный сустав '
        'выполняется шарнирным с ограничителем разгибания для естественности позы. Стопа изготавливается '
        'с плоской опорной поверхностью и креплением для магнитов или штифтов для фиксации на съёмочной '
        'площадке. Общая длина ноги составляет 100-130 мм для куклы высотой 250 мм.',
        styles['Body']
    ))
    
    # Чертёж полного каркаса
    story.append(Spacer(1, 5*mm))
    skeleton_drawing = create_armature_skeleton_drawing()
    story.append(skeleton_drawing)
    story.append(Paragraph('Рис. 3. Схема гуманоидного каркаса с обозначением основных суставов',
                           styles['Caption']))
    
    story.append(PageBreak())
    
    # ===== 4. ТЕХНИЧЕСКИЕ ЧЕРТЕЖИ =====
    story.append(Paragraph('4. ТЕХНИЧЕСКИЕ ЧЕРТЕЖИ', styles['H1']))
    
    story.append(Paragraph('4.1 Размеры компонентов', styles['H2']))
    story.append(Paragraph(
        'В таблице ниже приведены рекомендуемые размеры компонентов для куклы высотой 200-250 мм. '
        'Для других масштабов следует пропорционально изменить все линейные размеры. Критически '
        'важно соблюдать зазоры между подвижными частями: увеличение зазора снижает точность '
        'позиционирования, уменьшение — приводит к заеданию. Все размеры указаны в миллиметрах.',
        styles['Body']
    ))
    
    story.append(Spacer(1, 5*mm))
    story.append(create_dimension_table(styles))
    story.append(Paragraph('Таблица 1. Размеры компонентов каркаса', styles['Caption']))
    
    story.append(Paragraph('4.2 Допуски и посадки', styles['H2']))
    story.append(Paragraph(
        'Для обеспечения работоспособности шарнирных соединений критически важен правильный выбор '
        'допусков. Шаровые соединения требуют зазора 0.15-0.20 мм между диаметром шара и внутренним '
        'диаметром гнезда. Меньший зазор приводит к заклиниванию, больший — к избыточному люфту. '
        'Для SLA печати необходимо учитывать усадку материала: типичная усадка фотополимерных смол '
        'составляет 0.5-1.0% в зависимости от состава и режима пост-обработки. Рекомендуется изготавливать '
        'тестовые образцы для калибровки конкретного принтера и материала перед печатью основных деталей.',
        styles['Body']
    ))
    
    story.append(PageBreak())
    
    # ===== 5. НАСТРОЙКИ SLA ПЕЧАТИ =====
    story.append(Paragraph('5. НАСТРОЙКИ SLA ПЕЧАТИ', styles['H1']))
    
    story.append(Paragraph('5.1 Рекомендуемые параметры', styles['H2']))
    story.append(Paragraph(
        'Оптимизация параметров печати критически влияет на качество шарнирных соединений. '
        'Толщина слоя определяет точность геометрии: для суставов рекомендуется 25-50 мкм. '
        'Время экспозиции подбирается под конкретную смолу с учётом требуемой твёрдости поверхности. '
        'Плотность поддержек выбирается минимально достаточной для предотвращения деформаций, '
        'поскольку следы от поддержек на рабочих поверхностях суставов могут нарушить плавность хода.',
        styles['Body']
    ))
    
    story.append(Spacer(1, 5*mm))
    story.append(create_print_settings_table(styles))
    story.append(Paragraph('Таблица 2. Рекомендуемые параметры SLA печати', styles['Caption']))
    
    story.append(Paragraph('5.2 Ориентация деталей на платформе', styles['H2']))
    story.append(Paragraph(
        'Правильная ориентация деталей при печати существенно влияет на качество шарнирных поверхностей. '
        'Рекомендуется располагать суставы так, чтобы рабочие поверхности (шары, внутренние поверхности '
        'гнёзд) были направлены вверх или в стороны, но не вниз. Это минимизирует количество поддержек '
        'на критических поверхностях. Угол наклона 30-45 градусов часто даёт оптимальный баланс между '
        'качеством поверхности и сложностью поддержки. Для полых деталей необходимо предусмотреть '
        'дренажные отверстия диаметром 2-3 мм для вытекания неотверждённой смолы.',
        styles['Body']
    ))
    
    story.append(Paragraph('5.3 Пост-обработка', styles['H2']))
    story.append(Paragraph(
        'После печати детали требуют промывки в изопропиловом спирте (IPA) для удаления остатков '
        'жидкой смолы. Время промывки: 10-15 минут в свежем IPA с последующим ополаскиванием. '
        'После промывки детали сушат на воздухе или обдувают сжатым воздухом. Дополнительная '
        'UV-полимеризация завершает процесс отверждения: время и интенсивность подбираются под '
        'конкретный материал. Важно не переполимеризовать детали — избыточное UV-воздействие '
        'приводит к повышенной хрупкости. Шлифовка рабочих поверхностей суставов мелкой наждачной '
        'бумагой (P600-P1000) улучшает плавность хода, но требует аккуратности для сохранения геометрии.',
        styles['Body']
    ))
    
    story.append(PageBreak())
    
    # ===== 6. СБОРКА И МОНТАЖ =====
    story.append(Paragraph('6. СБОРКА И МОНТАЖ', styles['H1']))
    
    story.append(Paragraph('6.1 Подготовка деталей', styles['H2']))
    story.append(Paragraph(
        'Перед сборкой все напечатанные детали необходимо проверить на наличие дефектов: '
        'трещин, непропечатанных участков, искажений геометрии. Рабочие поверхности суставов '
        'осматривают на предмет следов от поддержек и при необходимости зачищают. Отверстия '
        'под арматуру проверяют калибровочным стержнем. Для смазки шарниров рекомендуется '
        'использовать сухую тефлоновую смазку или силиконовый спрей — жидкие масла могут '
        'вытекать и оставлять следы на съёмочной площадке.',
        styles['Body']
    ))
    
    story.append(Paragraph('6.2 Последовательность сборки', styles['H2']))
    story.append(Paragraph(
        'Рекомендуемая последовательность сборки гуманоидного каркаса: (1) Сборка осевого скелета — '
        'соединение головы, шеи, торса и таза с прокладкой арматурного стержня; (2) Монтаж плечевых '
        'суставов на торсе с регулировкой ширины плеч; (3) Сборка рук — последовательное соединение '
        'плечо-локоть-предплечье-запястье-кисть; (4) Монтаж собранных рук на плечевые суставы; '
        '(5) Установка тазобедренных суставов в таз с регулировкой угла разведения; (6) Сборка ног — '
        'бедро-колено-голень-голеностоп-стопа; (7) Монтаж собранных ног на тазобедренные суставы; '
        '(8) Финальная регулировка всех суставов и проверка диапазона движений.',
        styles['Body']
    ))
    
    story.append(Paragraph('6.3 Усиление каркаса', styles['H2']))
    story.append(Paragraph(
        'Для кукол с большим весом или при необходимости дополнительной жёсткости применяется '
        'усиление каркаса. Основной метод — прокладка металлической арматуры через внутренние '
        'каналы костей-стержней. Используются проволока из нержавеющей стали диаметром 0.8-1.5 мм, '
        'прутки из титанового сплава, или углепластиковые стержни. Арматура крепится в суставах '
        'эпоксидным клеем или механическими замками. Альтернативный метод — заливка полостей '
        'эпоксидной смолой с наполнителем для увеличения прочности без значительного прироста веса.',
        styles['Body']
    ))
    
    story.append(PageBreak())
    
    # ===== 7. BLENDER СКРИПТ =====
    story.append(Paragraph('7. BLENDER СКРИПТ', styles['H1']))
    
    story.append(Paragraph('7.1 Обзор генератора моделей', styles['H2']))
    story.append(Paragraph(
        'Прилагаемый Python скрипт для Blender 3D позволяет генерировать готовые 3D модели каркасов '
        'с настраиваемыми параметрами. Скрипт поддерживает три типа каркасов: гуманоидный (полный '
        'набор суставов для человекоподобного персонажа), упрощённый (минимум деталей для начинающих), '
        'и четвероногий (собака/кошка). Все модели автоматически разбиваются на части, организуются '
        'в коллекции по категориям, и снабжаются материалами для визуализации. Размеры компонентов '
        'вычисляются на основе масштабного коэффициента, что позволяет легко адаптировать каркас под '
        'требуемый размер куклы.',
        styles['Body']
    ))
    
    story.append(Paragraph('7.2 Инструкция по использованию', styles['H2']))
    story.append(Paragraph(
        'Для работы со скриптом необходимо: (1) Установить Blender версии 3.0 или выше; (2) Открыть '
        'файл blender_puppet_armature.py в редакторе скриптов Blender (вкладка Scripting); '
        '(3) Нажать Run Script (Alt+P) для генерации модели; (4) При необходимости изменить параметры '
        'в блоке PuppetArmatureSettings и перезапустить скрипт; (5) Для экспорта в STL установить '
        'export_stl=True и указать путь output_dir; (6) Сохранить сгенерированные файлы для печати. '
        'Скрипт автоматически очищает сцену перед генерацией, поэтому сохраните важные данные заранее.',
        styles['Body']
    ))
    
    story.append(Paragraph('7.3 Настраиваемые параметры', styles['H2']))
    story.append(Paragraph(
        'Класс PuppetArmatureSettings содержит все настраиваемые параметры каркаса. '
        'scale_factor — общий масштаб модели (1.0 = кукла высотой ~200 мм); '
        'ball_radius — радиус шаров в суставах (стандарт 3.0 мм); '
        'socket_gap — зазор между шаром и гнездом (0.15 мм для SLA); '
        'bone_diameter — диаметр костей-стержней (2.5 мм); '
        'bone_hole_diameter — диаметр отверстия под арматуру (1.0 мм). '
        'Изменение этих параметров автоматически пересчитывает все зависимые размеры при генерации.',
        styles['Body']
    ))
    
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph('Приложение: Файлы проекта', styles['H2']))
    story.append(Paragraph(
        '• blender_puppet_armature.py — Python скрипт генератора для Blender<br/>'
        '• puppet_armature_guide.pdf — данное техническое руководство<br/>'
        '• STL файлы отдельных компонентов (генерируются скриптом)',
        styles['Body']
    ))
    
    # Сборка документа
    doc.build(story)
    
    return output_path


if __name__ == '__main__':
    output = build_document()
    print(f"PDF документ создан: {output}")
