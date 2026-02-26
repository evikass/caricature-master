"""
Техническая документация: Детальный каркас кисти руки
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
import os

# Регистрация шрифтов
pdfmetrics.registerFont(TTFont('Times New Roman', '/usr/share/fonts/truetype/english/Times-New-Roman.ttf'))
registerFontFamily('Times New Roman', normal='Times New Roman', bold='Times New Roman')

output_path = '/home/z/my-project/download/hand_armature_guide.pdf'

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
    title='Hand_Armature_Technical_Guide',
    author='Z.ai',
    creator='Z.ai',
    subject='Detailed hand armature for stop-motion animation'
)

styles = getSampleStyleSheet()

# Стили
cover_title = ParagraphStyle('CoverTitle', fontName='Times New Roman', fontSize=28, leading=36, alignment=TA_CENTER, spaceAfter=20)
cover_subtitle = ParagraphStyle('CoverSubtitle', fontName='Times New Roman', fontSize=16, leading=22, alignment=TA_CENTER, spaceAfter=40)
h1_style = ParagraphStyle('H1', fontName='Times New Roman', fontSize=18, leading=24, alignment=TA_LEFT, spaceBefore=16, spaceAfter=10, textColor=colors.HexColor('#1F4E79'))
h2_style = ParagraphStyle('H2', fontName='Times New Roman', fontSize=14, leading=20, alignment=TA_LEFT, spaceBefore=12, spaceAfter=8, textColor=colors.HexColor('#2E75B6'))
h3_style = ParagraphStyle('H3', fontName='Times New Roman', fontSize=12, leading=16, alignment=TA_LEFT, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor('#404040'))
body_style = ParagraphStyle('Body', fontName='Times New Roman', fontSize=10.5, leading=15, alignment=TA_JUSTIFY, spaceAfter=8)
table_header = ParagraphStyle('TableHeader', fontName='Times New Roman', fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.white)
table_cell = ParagraphStyle('TableCell', fontName='Times New Roman', fontSize=9, leading=12, alignment=TA_CENTER)
table_cell_left = ParagraphStyle('TableCellLeft', fontName='Times New Roman', fontSize=9, leading=12, alignment=TA_LEFT)
caption_style = ParagraphStyle('Caption', fontName='Times New Roman', fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.HexColor('#555555'), spaceBefore=4, spaceAfter=12)

HEADER_COLOR = colors.HexColor('#1F4E79')
ROW_EVEN = colors.white
ROW_ODD = colors.HexColor('#F5F5F5')

story = []

# Титульная страница
story.append(Spacer(1, 80))
story.append(Paragraph("<b>DETAILED HAND ARMATURE</b>", cover_title))
story.append(Paragraph("<b>FOR STOP-MOTION ANIMATION</b>", cover_title))
story.append(Spacer(1, 30))
story.append(Paragraph("Technical Design & 3D Printing Guide", cover_subtitle))
story.append(Spacer(1, 40))
story.append(Paragraph("Ball-and-Socket Joint System", ParagraphStyle('Info', fontName='Times New Roman', fontSize=14, alignment=TA_CENTER)))
story.append(Paragraph("5 Fingers with 14 Articulated Joints", ParagraphStyle('Info', fontName='Times New Roman', fontSize=14, alignment=TA_CENTER)))
story.append(Spacer(1, 60))
story.append(Paragraph("Version 2.0 | 2025", ParagraphStyle('Date', fontName='Times New Roman', fontSize=12, alignment=TA_CENTER, textColor=colors.grey)))
story.append(PageBreak())

# Раздел 1
story.append(Paragraph("<b>1. Overview</b>", h1_style))
story.append(Spacer(1, 8))

story.append(Paragraph("""
The hand is one of the most expressive parts of a stop-motion puppet, requiring precise articulation 
for gestures, object manipulation, and emotional communication. This armature design provides independent 
control over each finger segment through a ball-and-socket joint system, enabling natural movement and 
stable pose retention during animation.
""", body_style))

story.append(Paragraph("""
Unlike simplified hand designs that group multiple fingers together, this detailed armature treats each 
finger as a separate mechanical system with its own joint hierarchy. This approach allows for complex 
hand poses such as typing, playing instruments, or subtle emotional gestures that would be impossible 
with less sophisticated constructions.
""", body_style))

# Раздел 2
story.append(Paragraph("<b>2. Joint Anatomy</b>", h1_style))
story.append(Spacer(1, 8))

story.append(Paragraph("<b>2.1 Ball-and-Socket Structure</b>", h2_style))

story.append(Paragraph("""
Each joint consists of three primary components: a precision ball, a matching socket, and an optional 
tensioning mechanism. The ball rotates freely within the socket while friction between the surfaces 
maintains the selected position. This design provides smooth, natural movement in all directions while 
preventing unwanted drift between animation frames.
""", body_style))

joint_data = [
    [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Material</b>", table_header), Paragraph("<b>Size Range</b>", table_header), Paragraph("<b>Function</b>", table_header)],
    [Paragraph("Joint Ball", table_cell_left), Paragraph("Tough/Engineering Resin", table_cell_left), Paragraph("2.5-4.0 mm diameter", table_cell_left), Paragraph("Rotating element", table_cell_left)],
    [Paragraph("Joint Socket", table_cell_left), Paragraph("Standard/Tough Resin", table_cell_left), Paragraph("3.0-5.0 mm ID", table_cell_left), Paragraph("Captures ball, provides friction", table_cell_left)],
    [Paragraph("Bone Segment", table_cell_left), Paragraph("Standard Resin", table_cell_left), Paragraph("2.0 mm diameter", table_cell_left), Paragraph("Connects adjacent joints", table_cell_left)],
    [Paragraph("Palm Base", table_cell_left), Paragraph("Standard Resin", table_cell_left), Paragraph("48 x 24 x 15 mm", table_cell_left), Paragraph("Anchors finger assemblies", table_cell_left)],
    [Paragraph("Wrist Joint", table_cell_left), Paragraph("Engineering Resin", table_cell_left), Paragraph("3.9 mm diameter", table_cell_left), Paragraph("Connects hand to arm", table_cell_left)],
]

joint_table = Table(joint_data, colWidths=[3.5*cm, 4*cm, 3.5*cm, 4*cm])
joint_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), ROW_ODD),
    ('BACKGROUND', (0, 5), (-1, 5), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 10))
story.append(joint_table)
story.append(Paragraph("Table 1: Hand Armature Component Specifications", caption_style))

# Раздел 3
story.append(Paragraph("<b>3. Finger Specifications</b>", h1_style))
story.append(Spacer(1, 8))

story.append(Paragraph("<b>3.1 Joint Count per Finger</b>", h2_style))

finger_data = [
    [Paragraph("<b>Finger</b>", table_header), Paragraph("<b>Joints</b>", table_header), Paragraph("<b>Bones</b>", table_header), Paragraph("<b>Total Length</b>", table_header), Paragraph("<b>Range of Motion</b>", table_header)],
    [Paragraph("Thumb", table_cell_left), Paragraph("2 IP + CMC", table_cell), Paragraph("2", table_cell), Paragraph("70% of Middle", table_cell), Paragraph("Opposition + Flexion", table_cell_left)],
    [Paragraph("Index", table_cell_left), Paragraph("3 (MCP, PIP, DIP)", table_cell), Paragraph("3", table_cell), Paragraph("95% of Middle", table_cell), Paragraph("Flexion + Adduction", table_cell_left)],
    [Paragraph("Middle", table_cell_left), Paragraph("3 (MCP, PIP, DIP)", table_cell), Paragraph("3", table_cell), Paragraph("Reference (100%)", table_cell), Paragraph("Flexion Only", table_cell_left)],
    [Paragraph("Ring", table_cell_left), Paragraph("3 (MCP, PIP, DIP)", table_cell), Paragraph("3", table_cell), Paragraph("95% of Middle", table_cell), Paragraph("Flexion Only", table_cell_left)],
    [Paragraph("Pinky", table_cell_left), Paragraph("3 (MCP, PIP, DIP)", table_cell), Paragraph("3", table_cell), Paragraph("80% of Middle", table_cell), Paragraph("Flexion + Abduction", table_cell_left)],
]

finger_table = Table(finger_data, colWidths=[2.5*cm, 3.5*cm, 2*cm, 3.5*cm, 4*cm])
finger_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), ROW_ODD),
    ('BACKGROUND', (0, 5), (-1, 5), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 10))
story.append(finger_table)
story.append(Paragraph("Table 2: Finger Joint Configuration", caption_style))

story.append(Paragraph("<b>3.2 Segment Lengths (6 cm Hand Scale)</b>", h2_style))

length_data = [
    [Paragraph("<b>Finger</b>", table_header), Paragraph("<b>Proximal</b>", table_header), Paragraph("<b>Middle</b>", table_header), Paragraph("<b>Distal</b>", table_header), Paragraph("<b>Total</b>", table_header)],
    [Paragraph("Thumb", table_cell_left), Paragraph("11 mm", table_cell), Paragraph("10 mm", table_cell), Paragraph("-", table_cell), Paragraph("21 mm", table_cell)],
    [Paragraph("Index", table_cell_left), Paragraph("14 mm", table_cell), Paragraph("10 mm", table_cell), Paragraph("8 mm", table_cell), Paragraph("32 mm", table_cell)],
    [Paragraph("Middle", table_cell_left), Paragraph("15 mm", table_cell), Paragraph("11 mm", table_cell), Paragraph("9 mm", table_cell), Paragraph("35 mm", table_cell)],
    [Paragraph("Ring", table_cell_left), Paragraph("14 mm", table_cell), Paragraph("10 mm", table_cell), Paragraph("8 mm", table_cell), Paragraph("32 mm", table_cell)],
    [Paragraph("Pinky", table_cell_left), Paragraph("11 mm", table_cell), Paragraph("8 mm", table_cell), Paragraph("6 mm", table_cell), Paragraph("25 mm", table_cell)],
]

length_table = Table(length_data, colWidths=[2.5*cm, 3*cm, 3*cm, 3*cm, 3*cm])
length_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), ROW_ODD),
    ('BACKGROUND', (0, 5), (-1, 5), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 10))
story.append(length_table)
story.append(Paragraph("Table 3: Bone Segment Lengths", caption_style))

# Раздел 4
story.append(Paragraph("<b>4. Printing Guidelines</b>", h1_style))
story.append(Spacer(1, 8))

story.append(Paragraph("<b>4.1 SLA Printer Requirements</b>", h2_style))

print_data = [
    [Paragraph("<b>Parameter</b>", table_header), Paragraph("<b>Minimum</b>", table_header), Paragraph("<b>Recommended</b>", table_header), Paragraph("<b>Notes</b>", table_header)],
    [Paragraph("XY Resolution", table_cell_left), Paragraph("35 microns", table_cell), Paragraph("50 microns", table_cell), Paragraph("Finer for better joint fit", table_cell_left)],
    [Paragraph("Layer Height", table_cell_left), Paragraph("25 microns", table_cell), Paragraph("50 microns", table_cell), Paragraph("Affects vertical tolerances", table_cell_left)],
    [Paragraph("Build Volume", table_cell_left), Paragraph("68 x 68 mm", table_cell), Paragraph("120 x 68 mm", table_cell), Paragraph("For full hand kit", table_cell_left)],
    [Paragraph("Resin Type", table_cell_left), Paragraph("Standard", table_cell), Paragraph("Tough/Engineering", table_cell), Paragraph("Joints need durability", table_cell_left)],
]

print_table = Table(print_data, colWidths=[3.5*cm, 3*cm, 3.5*cm, 5*cm])
print_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), ROW_ODD),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 10))
story.append(print_table)
story.append(Paragraph("Table 4: SLA Printing Requirements", caption_style))

story.append(Paragraph("<b>4.2 Orientation Guidelines</b>", h2_style))

story.append(Paragraph("""
Proper print orientation significantly affects joint quality. Balls should be printed with their 
polar axis vertical to minimize layer lines on the friction surface. Sockets benefit from angled 
orientation (30-45 degrees) to reduce suction cup effects and ensure uniform curing of interior 
surfaces. Bone segments can be printed horizontally for faster build times.
""", body_style))

# Раздел 5
story.append(Paragraph("<b>5. Post-Processing</b>", h1_style))
story.append(Spacer(1, 8))

story.append(Paragraph("<b>5.1 Cleaning Procedure</b>", h2_style))

steps = [
    "1. Remove parts from build plate using plastic scraper",
    "2. Submerge in 99% IPA for 10-15 minutes (or 5 min in ultrasonic cleaner)",
    "3. Remove supports while resin is still soft (before UV cure)",
    "4. Rinse in fresh IPA for 2 minutes to remove residue",
    "5. Air dry or use compressed air for internal socket areas",
    "6. UV cure according to resin specifications (typically 10-30 minutes)",
]

for step in steps:
    story.append(Paragraph(step, body_style))

story.append(Paragraph("<b>5.2 Joint Fitting</b>", h2_style))

story.append(Paragraph("""
After curing, test fit each ball in its corresponding socket. If friction is too high, lightly sand 
the ball surface with 600-800 grit sandpaper in a circular motion. Apply a small amount of silicone 
grease or PTFE dry lubricant to improve movement while maintaining pose stability. The ideal joint 
should move smoothly but require deliberate force to change position.
""", body_style))

# Раздел 6
story.append(Paragraph("<b>6. Part Count Summary</b>", h1_style))
story.append(Spacer(1, 8))

count_data = [
    [Paragraph("<b>Part Type</b>", table_header), Paragraph("<b>Quantity</b>", table_header), Paragraph("<b>Per Finger</b>", table_header), Paragraph("<b>Total</b>", table_header)],
    [Paragraph("Joint Balls", table_cell_left), Paragraph("3 per finger + tips", table_cell), Paragraph("14", table_cell), Paragraph("15 (+ 1 wrist)", table_cell)],
    [Paragraph("Sockets", table_cell_left), Paragraph("2 per finger", table_cell), Paragraph("10", table_cell), Paragraph("11 (+ 1 wrist)", table_cell)],
    [Paragraph("Bone Segments", table_cell_left), Paragraph("2-3 per finger", table_cell), Paragraph("13", table_cell), Paragraph("13", table_cell)],
    [Paragraph("Palm Base", table_cell_left), Paragraph("-", table_cell), Paragraph("-", table_cell), Paragraph("1", table_cell)],
    [Paragraph("Wrist Assembly", table_cell_left), Paragraph("-", table_cell), Paragraph("-", table_cell), Paragraph("2 (ball + socket)", table_cell)],
]

count_table = Table(count_data, colWidths=[3.5*cm, 4*cm, 3*cm, 3.5*cm])
count_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), ROW_ODD),
    ('BACKGROUND', (0, 5), (-1, 5), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 10))
story.append(count_table)
story.append(Paragraph("Table 5: Complete Part Inventory", caption_style))

# Раздел 7
story.append(Paragraph("<b>7. Using the Blender Script</b>", h1_style))
story.append(Spacer(1, 8))

story.append(Paragraph("""
The provided Python script generates all hand armature components directly in Blender. Two modes 
are available: assembled hand for preview and part kit for printing. The script creates properly 
dimensioned balls, sockets, and bones with correct tolerances for SLA printing.
""", body_style))

story.append(Paragraph("<b>Script Execution:</b>", h3_style))

script_steps = [
    "1. Open Blender (3.x / 4.x / 5.x)",
    "2. Go to Scripting workspace",
    "3. Create new text block (Ctrl+N)",
    "4. Paste script content",
    "5. Run Script (Alt+P)",
    "6. Export: File -> Export -> STL",
]

for step in script_steps:
    story.append(Paragraph(step, body_style))

story.append(Paragraph("<b>Adjustable Parameters:</b>", h3_style))

story.append(Paragraph("""
The script includes configurable settings at the top of the file: HAND_SCALE controls overall size 
(default 60mm), JOINT_BALL_RADIUS sets ball diameter (default 3mm), and JOINT_TOLERANCE adjusts 
the gap between ball and socket (default 0.2mm). Modify these values before running the script to 
customize for different puppet sizes or printer characteristics.
""", body_style))

# Сборка документа
doc.build(story)
print(f"PDF created: {output_path}")
