"""
Техническая документация: Каркасы для кукольной анимации
Puppet Armatures Technical Documentation
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether
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
pdfmetrics.registerFont(TTFont('SimHei', '/usr/share/fonts/truetype/chinese/SimHei.ttf'))
pdfmetrics.registerFont(TTFont('Times New Roman', '/usr/share/fonts/truetype/english/Times-New-Roman.ttf'))
registerFontFamily('Times New Roman', normal='Times New Roman', bold='Times New Roman')
registerFontFamily('SimHei', normal='SimHei', bold='SimHei')

# Выходной файл
output_path = '/home/z/my-project/download/puppet_armatures_technical_guide.pdf'

# Создание документа
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
    title='Puppet_Armatures_Technical_Guide',
    author='Z.ai',
    creator='Z.ai',
    subject='Technical documentation for stop-motion puppet armatures'
)

# Стили
styles = getSampleStyleSheet()

# Титульный стиль
cover_title = ParagraphStyle(
    'CoverTitle',
    fontName='Times New Roman',
    fontSize=32,
    leading=40,
    alignment=TA_CENTER,
    spaceAfter=20
)

cover_subtitle = ParagraphStyle(
    'CoverSubtitle',
    fontName='Times New Roman',
    fontSize=18,
    leading=24,
    alignment=TA_CENTER,
    spaceAfter=40
)

# Заголовки
h1_style = ParagraphStyle(
    'H1Style',
    fontName='Times New Roman',
    fontSize=20,
    leading=26,
    alignment=TA_LEFT,
    spaceBefore=20,
    spaceAfter=12,
    textColor=colors.HexColor('#1F4E79')
)

h2_style = ParagraphStyle(
    'H2Style',
    fontName='Times New Roman',
    fontSize=16,
    leading=22,
    alignment=TA_LEFT,
    spaceBefore=16,
    spaceAfter=8,
    textColor=colors.HexColor('#2E75B6')
)

h3_style = ParagraphStyle(
    'H3Style',
    fontName='Times New Roman',
    fontSize=13,
    leading=18,
    alignment=TA_LEFT,
    spaceBefore=12,
    spaceAfter=6,
    textColor=colors.HexColor('#404040')
)

# Основной текст
body_style = ParagraphStyle(
    'BodyStyle',
    fontName='Times New Roman',
    fontSize=11,
    leading=16,
    alignment=TA_JUSTIFY,
    spaceAfter=8
)

# Стиль для таблиц
table_header = ParagraphStyle(
    'TableHeader',
    fontName='Times New Roman',
    fontSize=10,
    leading=14,
    alignment=TA_CENTER,
    textColor=colors.white
)

table_cell = ParagraphStyle(
    'TableCell',
    fontName='Times New Roman',
    fontSize=9,
    leading=12,
    alignment=TA_CENTER
)

table_cell_left = ParagraphStyle(
    'TableCellLeft',
    fontName='Times New Roman',
    fontSize=9,
    leading=12,
    alignment=TA_LEFT
)

# Подписи
caption_style = ParagraphStyle(
    'Caption',
    fontName='Times New Roman',
    fontSize=10,
    leading=14,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#555555'),
    spaceBefore=4,
    spaceAfter=16
)

# Цвета таблиц
HEADER_COLOR = colors.HexColor('#1F4E79')
ROW_EVEN = colors.white
ROW_ODD = colors.HexColor('#F5F5F5')

story = []

# ============================================
# ТИТУЛЬНАЯ СТРАНИЦА
# ============================================
story.append(Spacer(1, 100))
story.append(Paragraph("<b>PUPPET ARMATURES</b>", cover_title))
story.append(Paragraph("<b>FOR STOP-MOTION ANIMATION</b>", cover_title))
story.append(Spacer(1, 30))
story.append(Paragraph("Technical Design Guide", cover_subtitle))
story.append(Paragraph("3D Printable Models for SLA Printing", cover_subtitle))
story.append(Spacer(1, 60))
story.append(Paragraph("Blender Python Script Included", ParagraphStyle('Info', fontName='Times New Roman', fontSize=14, alignment=TA_CENTER)))
story.append(Spacer(1, 20))
story.append(Paragraph("Version 1.0 | 2025", ParagraphStyle('Date', fontName='Times New Roman', fontSize=12, alignment=TA_CENTER, textColor=colors.grey)))
story.append(PageBreak())

# ============================================
# СОДЕРЖАНИЕ
# ============================================
story.append(Paragraph("<b>TABLE OF CONTENTS</b>", h1_style))
story.append(Spacer(1, 12))

toc_items = [
    ("1. Introduction to Puppet Armatures", "Overview and applications"),
    ("2. Technical Requirements for SLA Printing", "Parameters and tolerances"),
    ("3. Type 1: Wire Armature (Basic)", "Simple construction for beginners"),
    ("4. Type 2: Ball-and-Socket Armature (Professional)", "Advanced joint system"),
    ("5. Type 3: Modular Armature", "Interchangeable components"),
    ("6. Type 4: Hand Armature", "Detailed finger articulation"),
    ("7. Type 5: Universal Joints Set", "Custom building blocks"),
    ("8. Assembly Instructions", "Step-by-step guide"),
    ("9. Material Recommendations", "Resin types and properties"),
    ("10. Using the Blender Script", "How to generate and export models"),
]

for title, desc in toc_items:
    story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle('TOCItem', fontName='Times New Roman', fontSize=11, leading=16, leftIndent=10)))
    story.append(Paragraph(f"<i>{desc}</i>", ParagraphStyle('TOCDesc', fontName='Times New Roman', fontSize=10, leading=14, leftIndent=30, textColor=colors.grey)))
    story.append(Spacer(1, 4))

story.append(PageBreak())

# ============================================
# РАЗДЕЛ 1: ВВЕДЕНИЕ
# ============================================
story.append(Paragraph("<b>1. Introduction to Puppet Armatures</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("""
A puppet armature is the internal skeleton of a stop-motion puppet that provides structural support and enables 
controlled movement during animation. Unlike traditional ball-joint dolls or action figures, stop-motion armatures 
must maintain their pose precisely between frames without drifting or settling. This requires carefully designed 
friction joints that can be tightened or adjusted as needed throughout the animation process.
""", body_style))

story.append(Paragraph("""
The art of stop-motion animation has evolved significantly since its early days in the 20th century. Modern 
armatures combine traditional craftsmanship with advanced manufacturing techniques, including 3D printing. 
SLA (Stereolithography) printing offers exceptional precision for creating small, detailed components that 
would be difficult or impossible to machine using traditional methods. This technology democratizes access 
to professional-quality armatures, allowing independent animators and small studios to create sophisticated 
puppet mechanisms without expensive machining equipment.
""", body_style))

story.append(Paragraph("<b>Key Functions of an Armature:</b>", h3_style))

functions_data = [
    [Paragraph("<b>Function</b>", table_header), Paragraph("<b>Description</b>", table_header), Paragraph("<b>Importance</b>", table_header)],
    [Paragraph("Structural Support", table_cell_left), Paragraph("Maintains puppet shape under gravity", table_cell_left), Paragraph("Critical", table_cell)],
    [Paragraph("Pose Control", table_cell_left), Paragraph("Allows animator to position limbs precisely", table_cell_left), Paragraph("Critical", table_cell)],
    [Paragraph("Friction Retention", table_cell_left), Paragraph("Holds position between frames", table_cell_left), Paragraph("Critical", table_cell)],
    [Paragraph("Attachment Points", table_cell_left), Paragraph("Connects to puppet exterior materials", table_cell_left), Paragraph("High", table_cell)],
    [Paragraph("Replaceability", table_cell_left), Paragraph("Allows part replacement if damaged", table_cell_left), Paragraph("Medium", table_cell)],
]

functions_table = Table(functions_data, colWidths=[3.5*cm, 7*cm, 2.5*cm])
functions_table.setStyle(TableStyle([
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
story.append(Spacer(1, 12))
story.append(functions_table)
story.append(Paragraph("Table 1: Core Functions of Stop-Motion Armatures", caption_style))

# ============================================
# РАЗДЕЛ 2: ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ
# ============================================
story.append(Paragraph("<b>2. Technical Requirements for SLA Printing</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("""
SLA printing uses a UV laser to cure liquid photopolymer resin layer by layer, creating highly detailed parts 
with smooth surface finishes. However, this process has specific limitations that must be considered when 
designing armature components. Understanding these constraints is essential for creating functional joints 
that operate smoothly after printing and post-processing.
""", body_style))

story.append(Paragraph("<b>2.1 Minimum Dimensions</b>", h2_style))

dims_data = [
    [Paragraph("<b>Parameter</b>", table_header), Paragraph("<b>Minimum Value</b>", table_header), Paragraph("<b>Recommended</b>", table_header), Paragraph("<b>Notes</b>", table_header)],
    [Paragraph("Wall thickness", table_cell_left), Paragraph("0.4 mm", table_cell), Paragraph("0.8-1.0 mm", table_cell), Paragraph("Thinner walls may fail during printing", table_cell_left)],
    [Paragraph("Pin/hole diameter", table_cell_left), Paragraph("0.5 mm", table_cell), Paragraph("1.0-2.0 mm", table_cell), Paragraph("Critical for joint pivots", table_cell_left)],
    [Paragraph("Gap between parts", table_cell_left), Paragraph("0.1 mm", table_cell), Paragraph("0.2-0.3 mm", table_cell), Paragraph("Allows movement after curing", table_cell_left)],
    [Paragraph("Ball joint diameter", table_cell_left), Paragraph("3 mm", table_cell), Paragraph("4-8 mm", table_cell), Paragraph("Smaller balls wear quickly", table_cell_left)],
    [Paragraph("Support contact area", table_cell_left), Paragraph("N/A", table_cell), Paragraph(">2 mm", table_cell), Paragraph("Larger areas leave marks", table_cell_left)],
]

dims_table = Table(dims_data, colWidths=[3.5*cm, 3*cm, 3*cm, 4.5*cm])
dims_table.setStyle(TableStyle([
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
story.append(Spacer(1, 12))
story.append(dims_table)
story.append(Paragraph("Table 2: SLA Printing Dimension Constraints", caption_style))

story.append(Paragraph("<b>2.2 Joint Tolerance Calculations</b>", h2_style))

story.append(Paragraph("""
Proper joint tolerance is crucial for functional ball-and-socket connections. The gap between the ball and 
socket must be large enough to allow smooth rotation but small enough to maintain friction for pose retention. 
Our recommended formula accounts for resin shrinkage during curing, which typically ranges from 1-5% depending 
on the material and printing parameters used.
""", body_style))

story.append(Paragraph("""
<b>Socket Inner Diameter</b> = Ball Diameter + 2 x (Tolerance + Shrinkage Compensation)
<br/><br/>
Where:<br/>
- Tolerance = 0.15-0.25 mm (minimum gap for movement)<br/>
- Shrinkage Compensation = 0.02-0.05 mm per mm of dimension<br/>
- For a 6 mm ball: Socket ID = 6 + 2 x (0.2 + 0.15) = 6.7 mm
""", body_style))

# ============================================
# РАЗДЕЛ 3: ПРОВОЛОЧНЫЙ КАРКАС
# ============================================
story.append(Paragraph("<b>3. Type 1: Wire Armature (Basic)</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("""
The wire armature represents the most accessible entry point into stop-motion puppet construction. This design 
uses a continuous wire skeleton that runs through the entire puppet body, with cross-bars at the shoulders 
and pelvis providing width and stability. While simpler than ball-and-socket designs, wire armatures remain 
widely used in professional animation studios for secondary characters and creatures where extreme precision 
is not required.
""", body_style))

story.append(Paragraph("<b>3.1 Design Specifications</b>", h2_style))

wire_specs = [
    [Paragraph("<b>Component</b>", table_header), Paragraph("<b>Dimension (15 cm puppet)</b>", table_header), Paragraph("<b>Material</b>", table_header)],
    [Paragraph("Spine wire", table_cell_left), Paragraph("2.0 mm diameter, 120 mm length", table_cell_left), Paragraph("Aluminum or steel", table_cell)],
    [Paragraph("Shoulder bar", table_cell_left), Paragraph("2.4 mm diameter, 60 mm length", table_cell_left), Paragraph("Aluminum or steel", table_cell)],
    [Paragraph("Pelvis bar", table_cell_left), Paragraph("2.4 mm diameter, 45 mm length", table_cell_left), Paragraph("Aluminum or steel", table_cell)],
    [Paragraph("Arm wires", table_cell_left), Paragraph("1.5 mm diameter, 52 mm each", table_cell_left), Paragraph("Aluminum", table_cell)],
    [Paragraph("Leg wires", table_cell_left), Paragraph("2.0 mm diameter, 67 mm each", table_cell_left), Paragraph("Steel or aluminum", table_cell)],
    [Paragraph("Head loop", table_cell_left), Paragraph("2.0 mm diameter, 25 mm ring", table_cell_left), Paragraph("Aluminum", table_cell)],
]

wire_table = Table(wire_specs, colWidths=[4*cm, 5.5*cm, 4*cm])
wire_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), ROW_ODD),
    ('BACKGROUND', (0, 5), (-1, 5), ROW_EVEN),
    ('BACKGROUND', (0, 6), (-1, 6), ROW_ODD),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 12))
story.append(wire_table)
story.append(Paragraph("Table 3: Wire Armature Component Specifications", caption_style))

story.append(Paragraph("<b>3.2 Advantages and Limitations</b>", h2_style))

story.append(Paragraph("""
<b>Advantages:</b> Low cost, simple construction, easy repairs, lightweight, flexible posing, no special tools 
required. Wire armatures can be built in a single day with basic materials from a hardware store. The 
continuous wire construction eliminates loose parts that could fail during animation sessions.
""", body_style))

story.append(Paragraph("""
<b>Limitations:</b> Wire fatigue after repeated bending, limited pose precision, gradual drift in positions, 
difficulty maintaining extreme poses. Aluminum wire typically lasts 50-100 animation cycles before showing 
signs of fatigue, while steel wire lasts longer but is harder to bend smoothly.
""", body_style))

# ============================================
# РАЗДЕЛ 4: BALL-AND-SOCKET КАРКАС
# ============================================
story.append(Paragraph("<b>4. Type 2: Ball-and-Socket Armature (Professional)</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("""
The ball-and-socket armature represents the professional standard for stop-motion animation. Each joint 
consists of a precision-ground ball captured in a socket, creating a connection that can rotate in any 
direction while providing adjustable friction. This design allows animators to make subtle incremental 
adjustments to poses while maintaining absolute position stability between frames.
""", body_style))

story.append(Paragraph("<b>4.1 Joint Anatomy</b>", h2_style))

story.append(Paragraph("""
Each ball-and-socket joint comprises three primary components working together: the ball (spherical head 
attached to one bone segment), the socket (hemispherical cup attached to the adjacent segment), and the 
tensioning mechanism (typically a spring or screw system that adjusts clamping pressure). The friction 
between ball and socket determines how firmly the joint holds its position.
""", body_style))

joint_specs = [
    [Paragraph("<b>Joint Location</b>", table_header), Paragraph("<b>Ball Diameter</b>", table_header), Paragraph("<b>Socket Depth</b>", table_header), Paragraph("<b>Friction Range</b>", table_header)],
    [Paragraph("Hip joints", table_cell_left), Paragraph("6 mm", table_cell), Paragraph("4.5 mm (75%)", table_cell), Paragraph("High", table_cell)],
    [Paragraph("Knee joints", table_cell_left), Paragraph("6 mm", table_cell), Paragraph("4.5 mm (75%)", table_cell), Paragraph("Medium", table_cell)],
    [Paragraph("Ankle joints", table_cell_left), Paragraph("4 mm", table_cell), Paragraph("3.0 mm (75%)", table_cell), Paragraph("Medium", table_cell)],
    [Paragraph("Shoulder joints", table_cell_left), Paragraph("6 mm", table_cell), Paragraph("4.5 mm (75%)", table_cell), Paragraph("Medium", table_cell)],
    [Paragraph("Elbow joints", table_cell_left), Paragraph("4 mm", table_cell), Paragraph("3.0 mm (75%)", table_cell), Paragraph("Medium", table_cell)],
    [Paragraph("Wrist joints", table_cell_left), Paragraph("4 mm", table_cell), Paragraph("2.5 mm (62%)", table_cell), Paragraph("Low", table_cell)],
    [Paragraph("Neck joint", table_cell_left), Paragraph("6 mm", table_cell), Paragraph("4.0 mm (67%)", table_cell), Paragraph("Medium", table_cell)],
]

joint_table = Table(joint_specs, colWidths=[3.5*cm, 3*cm, 3.5*cm, 3.5*cm])
joint_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), ROW_ODD),
    ('BACKGROUND', (0, 5), (-1, 5), ROW_EVEN),
    ('BACKGROUND', (0, 6), (-1, 6), ROW_ODD),
    ('BACKGROUND', (0, 7), (-1, 7), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 12))
story.append(joint_table)
story.append(Paragraph("Table 4: Ball-and-Socket Joint Specifications", caption_style))

story.append(Paragraph("<b>4.2 Body Proportions</b>", h2_style))

proportions_data = [
    [Paragraph("<b>Body Segment</b>", table_header), Paragraph("<b>Percentage of Height</b>", table_header), Paragraph("<b>15 cm Puppet (mm)</b>", table_header)],
    [Paragraph("Head height", table_cell_left), Paragraph("15%", table_cell), Paragraph("22.5 mm", table_cell)],
    [Paragraph("Neck", table_cell_left), Paragraph("3%", table_cell), Paragraph("4.5 mm", table_cell)],
    [Paragraph("Torso", table_cell_left), Paragraph("20%", table_cell), Paragraph("30 mm", table_cell)],
    [Paragraph("Pelvis", table_cell_left), Paragraph("5%", table_cell), Paragraph("7.5 mm", table_cell)],
    [Paragraph("Upper arm", table_cell_left), Paragraph("12%", table_cell), Paragraph("18 mm", table_cell)],
    [Paragraph("Forearm + hand", table_cell_left), Paragraph("12%", table_cell), Paragraph("18 mm", table_cell)],
    [Paragraph("Thigh", table_cell_left), Paragraph("15%", table_cell), Paragraph("22.5 mm", table_cell)],
    [Paragraph("Shin + foot", table_cell_left), Paragraph("15%", table_cell), Paragraph("22.5 mm", table_cell)],
]

prop_table = Table(proportions_data, colWidths=[4*cm, 4.5*cm, 5*cm])
prop_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), ROW_ODD),
    ('BACKGROUND', (0, 5), (-1, 5), ROW_EVEN),
    ('BACKGROUND', (0, 6), (-1, 6), ROW_ODD),
    ('BACKGROUND', (0, 7), (-1, 7), ROW_EVEN),
    ('BACKGROUND', (0, 8), (-1, 8), ROW_ODD),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 12))
story.append(prop_table)
story.append(Paragraph("Table 5: Human Proportion Standards for Puppet Design", caption_style))

# ============================================
# РАЗДЕЛ 5: МОДУЛЬНЫЙ КАРКАС
# ============================================
story.append(Paragraph("<b>5. Type 3: Modular Armature System</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("""
The modular armature system provides maximum flexibility by separating each functional component into 
individually printable parts. This approach allows animators to replace damaged sections, customize 
proportions, or experiment with different joint configurations without reprinting the entire armature. 
Modular designs also facilitate scaling, as components can be adjusted independently.
""", body_style))

story.append(Paragraph("<b>5.1 Module Categories</b>", h2_style))

modules_data = [
    [Paragraph("<b>Module</b>", table_header), Paragraph("<b>Components</b>", table_header), Paragraph("<b>Connection Type</b>", table_header)],
    [Paragraph("Pelvis Module", table_cell_left), Paragraph("Central block, hip mounts, spine receiver", table_cell_left), Paragraph("Threaded M2/M3", table_cell)],
    [Paragraph("Chest Module", table_cell_left), Paragraph("Ribcage block, shoulder mounts, neck receiver", table_cell_left), Paragraph("Threaded M2/M3", table_cell)],
    [Paragraph("Head Module", table_cell_left), Paragraph("Skull dome, jaw pivots, neck rod", table_cell_left), Paragraph("Press-fit or screw", table_cell)],
    [Paragraph("Leg Modules (x2)", table_cell_left), Paragraph("Thigh, knee, shin, ankle, foot segments", table_cell_left), Paragraph("Ball-and-socket", table_cell)],
    [Paragraph("Arm Modules (x2)", table_cell_left), Paragraph("Upper arm, elbow, forearm, wrist, hand", table_cell_left), Paragraph("Ball-and-socket", table_cell)],
]

modules_table = Table(modules_data, colWidths=[3.5*cm, 6*cm, 4*cm])
modules_table.setStyle(TableStyle([
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
story.append(Spacer(1, 12))
story.append(modules_table)
story.append(Paragraph("Table 6: Modular System Component Overview", caption_style))

# ============================================
# РАЗДЕЛ 6: КАРКАС КИСТИ
# ============================================
story.append(Paragraph("<b>6. Type 4: Hand Armature (Detailed Finger Articulation)</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("""
Hand animation is one of the most challenging aspects of stop-motion puppetry. Characters frequently need 
to interact with props, gesture expressively, or grip objects naturally. A dedicated hand armature provides 
individual control over each finger segment, enabling nuanced performances that would be impossible with 
simplified hand designs.
""", body_style))

story.append(Paragraph("<b>6.1 Finger Joint Configuration</b>", h2_style))

finger_data = [
    [Paragraph("<b>Finger</b>", table_header), Paragraph("<b>Joints</b>", table_header), Paragraph("<b>Total Length</b>", table_header), Paragraph("<b>Range of Motion</b>", table_header)],
    [Paragraph("Thumb", table_cell_left), Paragraph("2 IP joints + CMC", table_cell), Paragraph("70% of middle", table_cell), Paragraph("Opposition + flexion", table_cell)],
    [Paragraph("Index", table_cell_left), Paragraph("3 joints (MCP, PIP, DIP)", table_cell), Paragraph("95% of middle", table_cell), Paragraph("Flexion + adduction", table_cell)],
    [Paragraph("Middle", table_cell_left), Paragraph("3 joints (MCP, PIP, DIP)", table_cell), Paragraph("Reference (100%)", table_cell), Paragraph("Flexion only", table_cell)],
    [Paragraph("Ring", table_cell_left), Paragraph("3 joints (MCP, PIP, DIP)", table_cell), Paragraph("95% of middle", table_cell), Paragraph("Flexion only", table_cell)],
    [Paragraph("Pinky", table_cell_left), Paragraph("3 joints (MCP, PIP, DIP)", table_cell), Paragraph("80% of middle", table_cell), Paragraph("Flexion + abduction", table_cell)],
]

finger_table = Table(finger_data, colWidths=[2.5*cm, 4*cm, 3.5*cm, 4*cm])
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
story.append(Spacer(1, 12))
story.append(finger_table)
story.append(Paragraph("Table 7: Finger Joint Anatomy for Animation", caption_style))

# ============================================
# РАЗДЕЛ 7: УНИВЕРСАЛЬНЫЕ ШАРНИРЫ
# ============================================
story.append(Paragraph("<b>7. Type 5: Universal Joints Set</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("""
For animators who prefer to design their own custom armatures, the Universal Joints Set provides a 
collection of standardized components that can be mixed and matched. This approach is ideal for creating 
non-humanoid characters, creatures, or specialized mechanisms that don't fit standard proportions.
""", body_style))

story.append(Paragraph("<b>7.1 Available Component Sizes</b>", h2_style))

joints_data = [
    [Paragraph("<b>Size Name</b>", table_header), Paragraph("<b>Ball Diameter</b>", table_header), Paragraph("<b>Socket ID</b>", table_header), Paragraph("<b>Recommended Use</b>", table_header)],
    [Paragraph("Small", table_cell_left), Paragraph("4 mm", table_cell), Paragraph("4.4 mm", table_cell), Paragraph("Fingers, toes, facial features", table_cell_left)],
    [Paragraph("Medium", table_cell_left), Paragraph("6 mm", table_cell), Paragraph("6.5 mm", table_cell), Paragraph("Elbows, knees, wrists", table_cell_left)],
    [Paragraph("Large", table_cell_left), Paragraph("8 mm", table_cell), Paragraph("8.6 mm", table_cell), Paragraph("Hips, shoulders, spine", table_cell_left)],
]

joints_table = Table(joints_data, colWidths=[3*cm, 3*cm, 3*cm, 5*cm])
joints_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 12))
story.append(joints_table)
story.append(Paragraph("Table 8: Universal Joint Component Specifications", caption_style))

# ============================================
# РАЗДЕЛ 8: ИНСТРУКЦИИ ПО СБОРКЕ
# ============================================
story.append(Paragraph("<b>8. Assembly Instructions</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("<b>8.1 Post-Printing Preparation</b>", h2_style))

story.append(Paragraph("""
Before assembly, all printed parts require proper post-processing to ensure optimal joint performance. 
This includes UV curing, support removal, and surface finishing. The quality of post-processing directly 
affects joint friction and long-term durability of the armature.
""", body_style))

assembly_steps = [
    "1. Remove prints from build plate carefully using a plastic scraper",
    "2. Submerge parts in IPA (99% isopropyl alcohol) for 10-15 minutes",
    "3. Use ultrasonic cleaner for complex parts with internal channels",
    "4. Remove supports while resin is still soft (before final cure)",
    "5. Sand mating surfaces with 400-600 grit sandpaper",
    "6. UV cure for 10-30 minutes depending on resin type",
    "7. Apply silicone-based lubricant to ball surfaces before assembly",
    "8. Test joint friction and adjust with fine sandpaper if needed",
]

for step in assembly_steps:
    story.append(Paragraph(step, body_style))

story.append(Paragraph("<b>8.2 Joint Assembly Sequence</b>", h2_style))

story.append(Paragraph("""
Assemble joints in a systematic order, starting from the pelvis and working outward. This ensures proper 
alignment and allows for adjustments during the build process. Keep all fasteners and tools organized 
before beginning assembly.
""", body_style))

sequence_data = [
    [Paragraph("<b>Step</b>", table_header), Paragraph("<b>Action</b>", table_header), Paragraph("<b>Tools Required</b>", table_header)],
    [Paragraph("1", table_cell), Paragraph("Assemble pelvis block with hip sockets", table_cell_left), Paragraph("M2 hex key, pliers", table_cell)],
    [Paragraph("2", table_cell), Paragraph("Attach leg segments to hip joints", table_cell_left), Paragraph("Hex key, silicone grease", table_cell)],
    [Paragraph("3", table_cell), Paragraph("Connect knee and ankle joints", table_cell_left), Paragraph("Pliers, alignment jig", table_cell)],
    [Paragraph("4", table_cell), Paragraph("Attach spine to pelvis", table_cell_left), Paragraph("M2 screwdriver", table_cell)],
    [Paragraph("5", table_cell), Paragraph("Mount chest block on spine", table_cell_left), Paragraph("Hex key", table_cell)],
    [Paragraph("6", table_cell), Paragraph("Install shoulder joints", table_cell_left), Paragraph("Pliers, grease", table_cell)],
    [Paragraph("7", table_cell), Paragraph("Attach arm segments", table_cell_left), Paragraph("Alignment tools", table_cell)],
    [Paragraph("8", table_cell), Paragraph("Connect neck and head", table_cell_left), Paragraph("M2 screwdriver", table_cell)],
]

seq_table = Table(sequence_data, colWidths=[1.5*cm, 7*cm, 5*cm])
seq_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('BACKGROUND', (0, 4), (-1, 4), ROW_ODD),
    ('BACKGROUND', (0, 5), (-1, 5), ROW_EVEN),
    ('BACKGROUND', (0, 6), (-1, 6), ROW_ODD),
    ('BACKGROUND', (0, 7), (-1, 7), ROW_EVEN),
    ('BACKGROUND', (0, 8), (-1, 8), ROW_ODD),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 12))
story.append(seq_table)
story.append(Paragraph("Table 9: Assembly Sequence for Complete Armature", caption_style))

# ============================================
# РАЗДЕЛ 9: МАТЕРИАЛЫ
# ============================================
story.append(Paragraph("<b>9. Material Recommendations</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("<b>9.1 Resin Types for Armature Parts</b>", h2_style))

resin_data = [
    [Paragraph("<b>Resin Type</b>", table_header), Paragraph("<b>Properties</b>", table_header), Paragraph("<b>Best For</b>", table_header), Paragraph("<b>Notes</b>", table_header)],
    [Paragraph("Standard", table_cell_left), Paragraph("Good detail, moderate strength", table_cell_left), Paragraph("Bones, structural parts", table_cell_left), Paragraph("May brittle over time", table_cell_left)],
    [Paragraph("Tough", table_cell_left), Paragraph("High impact resistance", table_cell_left), Paragraph("Joint components", table_cell_left), Paragraph("Requires longer cure", table_cell_left)],
    [Paragraph("Flexible", table_cell_left), Paragraph("Elastic, rubber-like", table_cell_left), Paragraph("Socket interiors", table_cell_left), Paragraph("Limited precision", table_cell_left)],
    [Paragraph("Engineering", table_cell_left), Paragraph("Heat resistant, strong", table_cell_left), Paragraph("High-wear joints", table_cell_left), Paragraph("Higher cost", table_cell_left)],
    [Paragraph("Dental", table_cell_left), Paragraph("Extreme precision", table_cell_left), Paragraph("Small ball joints", table_cell_left), Paragraph("Specialized equipment", table_cell_left)],
]

resin_table = Table(resin_data, colWidths=[2.5*cm, 4*cm, 3.5*cm, 3.5*cm])
resin_table.setStyle(TableStyle([
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
story.append(Spacer(1, 12))
story.append(resin_table)
story.append(Paragraph("Table 10: Resin Selection Guide for Armature Components", caption_style))

# ============================================
# РАЗДЕЛ 10: ИСПОЛЬЗОВАНИЕ СКРИПТА
# ============================================
story.append(Paragraph("<b>10. Using the Blender Script</b>", h1_style))
story.append(Spacer(1, 12))

story.append(Paragraph("<b>10.1 Installation and Setup</b>", h2_style))

story.append(Paragraph("""
The provided Python script generates all five armature types directly in Blender. Follow these steps to 
load and execute the script within Blender's Python environment. The script is compatible with Blender 
3.0 and later versions.
""", body_style))

blender_steps = [
    "1. Open Blender (version 3.0 or later recommended)",
    "2. Navigate to the Scripting workspace (top menu bar)",
    "3. Click 'New' to create a new text block",
    "4. Copy the entire contents of 'puppet_armatures_blender.py'",
    "5. Paste into the text editor",
    "6. Press 'Run Script' (Alt+P) or click the play button",
    "7. Wait for model generation (typically 5-10 seconds)",
    "8. All armatures will appear in the 3D viewport",
]

for step in blender_steps:
    story.append(Paragraph(step, body_style))

story.append(Paragraph("<b>10.2 Export Options</b>", h2_style))

story.append(Paragraph("""
After generating models, export them for 3D printing using Blender's built-in exporters. STL format is 
recommended for SLA printers, though OBJ with metric units also works well. When exporting, ensure the 
scale factor is set correctly for your printer's expected units (typically millimeters).
""", body_style))

export_data = [
    [Paragraph("<b>Format</b>", table_header), Paragraph("<b>Use Case</b>", table_header), Paragraph("<b>Scale Setting</b>", table_header)],
    [Paragraph("STL", table_cell_left), Paragraph("Most SLA slicers (Chitubox, Lychee)", table_cell_left), Paragraph("x1000 (m to mm)", table_cell)],
    [Paragraph("OBJ", table_cell_left), Paragraph("Autodesk applications, Formlabs PreForm", table_cell_left), Paragraph("x1000 (m to mm)", table_cell)],
    [Paragraph("3MF", table_cell_left), Paragraph("Modern slicers with unit support", table_cell_left), Paragraph("x1000 (m to mm)", table_cell)],
    [Paragraph("AMF", table_cell_left), Paragraph("Multi-material printers", table_cell_left), Paragraph("x1000 (m to mm)", table_cell)],
]

export_table = Table(export_data, colWidths=[2.5*cm, 6*cm, 5*cm])
export_table.setStyle(TableStyle([
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
story.append(Spacer(1, 12))
story.append(export_table)
story.append(Paragraph("Table 11: Export Format Recommendations", caption_style))

story.append(Paragraph("<b>10.3 Customization Tips</b>", h2_style))

story.append(Paragraph("""
The script includes adjustable parameters at the top of the file. Key values that can be modified include 
the overall puppet scale (default 15 cm), ball joint diameters for different body parts, and tolerance 
values for joint fit. When modifying these values, maintain proportional relationships between components 
to ensure proper assembly.
""", body_style))

story.append(Paragraph("""
Key parameters to adjust:<br/>
- <b>DOLL_SCALE</b>: Overall puppet height in meters (default: 0.15 for 15 cm puppet)<br/>
- <b>MIN_WALL_THICKNESS</b>: Minimum printable wall (default: 0.001 m = 1 mm)<br/>
- <b>JOINT_TOLERANCE</b>: Gap between ball and socket (default: 0.0002 m = 0.2 mm)<br/>
- <b>BALL_SMALL/MEDIUM/LARGE</b>: Joint ball diameters in meters
""", body_style))

# Сборка документа
doc.build(story)
print(f"PDF created: {output_path}")
