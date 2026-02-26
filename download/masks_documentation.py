"""
Техническая документация: Маски для детских праздников
Party Masks Technical Documentation
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

# Регистрация шрифтов
pdfmetrics.registerFont(TTFont('SimHei', '/usr/share/fonts/truetype/chinese/SimHei.ttf'))
pdfmetrics.registerFont(TTFont('Times New Roman', '/usr/share/fonts/truetype/english/Times-New-Roman.ttf'))
registerFontFamily('Times New Roman', normal='Times New Roman', bold='Times New Roman')
registerFontFamily('SimHei', normal='SimHei', bold='SimHei')

output_path = '/home/z/my-project/download/party_masks_technical_guide.pdf'

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
    title='Party_Masks_Technical_Guide',
    author='Z.ai',
    creator='Z.ai',
    subject='Technical documentation for 3D printable party masks'
)

styles = getSampleStyleSheet()

# Стили
cover_title = ParagraphStyle(
    'CoverTitle',
    fontName='Times New Roman',
    fontSize=36,
    leading=44,
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

h1_style = ParagraphStyle(
    'H1Style',
    fontName='Times New Roman',
    fontSize=18,
    leading=24,
    alignment=TA_LEFT,
    spaceBefore=16,
    spaceAfter=10,
    textColor=colors.HexColor('#1F4E79')
)

h2_style = ParagraphStyle(
    'H2Style',
    fontName='Times New Roman',
    fontSize=14,
    leading=20,
    alignment=TA_LEFT,
    spaceBefore=12,
    spaceAfter=8,
    textColor=colors.HexColor('#2E75B6')
)

body_style = ParagraphStyle(
    'BodyStyle',
    fontName='Times New Roman',
    fontSize=11,
    leading=16,
    alignment=TA_JUSTIFY,
    spaceAfter=8
)

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

caption_style = ParagraphStyle(
    'Caption',
    fontName='Times New Roman',
    fontSize=10,
    leading=14,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#555555'),
    spaceBefore=4,
    spaceAfter=14
)

# Цвета таблиц
HEADER_COLOR = colors.HexColor('#1F4E79')
ROW_EVEN = colors.white
ROW_ODD = colors.HexColor('#F5F5F5')

story = []

# ============================================
# ТИТУЛЬНАЯ СТРАНИЦА
# ============================================
story.append(Spacer(1, 80))
story.append(Paragraph("<b>PARTY MASKS</b>", cover_title))
story.append(Paragraph("<b>FOR CHILDREN'S CELEBRATIONS</b>", cover_title))
story.append(Spacer(1, 30))
story.append(Paragraph("Technical Design Guide", cover_subtitle))
story.append(Paragraph("15 Character Masks for SLA 3D Printing", cover_subtitle))
story.append(Spacer(1, 50))

# Список персонажей
characters = """
<b>Animals:</b> Wolf, Fox, Rabbit, Bear, Lynx, Frog, Raven, Crow, Squirrel<br/>
<b>Fairy Tale Characters:</b> Baba Yaga, Koschei, Snegurochka, Ded Moroz, Leshy, Vodyanoy
"""
story.append(Paragraph(characters, ParagraphStyle('Chars', fontName='Times New Roman', fontSize=12, alignment=TA_CENTER, leading=18)))

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
    ("1. Overview", "Purpose and applications"),
    ("2. Technical Specifications", "Dimensions and tolerances for SLA printing"),
    ("3. Animal Masks", "Wolf, Fox, Rabbit, Bear, Lynx, Frog, Raven, Crow, Squirrel"),
    ("4. Fairy Tale Masks", "Baba Yaga, Koschei, Snegurochka, Ded Moroz, Leshy, Vodyanoy"),
    ("5. Printing Guidelines", "SLA printer settings and material recommendations"),
    ("6. Post-Processing", "Finishing and painting instructions"),
    ("7. Using the Blender Script", "How to customize and export models"),
]

for title, desc in toc_items:
    story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle('TOCItem', fontName='Times New Roman', fontSize=11, leading=16, leftIndent=10)))
    story.append(Paragraph(f"<i>{desc}</i>", ParagraphStyle('TOCDesc', fontName='Times New Roman', fontSize=10, leading=14, leftIndent=30, textColor=colors.grey)))
    story.append(Spacer(1, 4))

story.append(PageBreak())

# ============================================
# РАЗДЕЛ 1: ОБЗОР
# ============================================
story.append(Paragraph("<b>1. Overview</b>", h1_style))
story.append(Spacer(1, 10))

story.append(Paragraph("""
This technical guide provides detailed specifications for 15 character masks designed for children's parties, 
school performances, and festive events. Each mask is optimized for SLA (Stereolithography) 3D printing, 
ensuring high detail, smooth surface finish, and comfortable wear for children aged 4-10 years. The masks 
feature standardized dimensions, attachment points for elastic straps, and ventilation holes for extended wear.
""", body_style))

story.append(Paragraph("""
The collection includes two main categories: realistic animal masks (Wolf, Fox, Rabbit, Bear, Lynx, Frog, 
Raven, Crow, Squirrel) and Russian fairy tale characters (Baba Yaga, Koschei, Snegurochka, Ded Moroz, 
Leshy, Vodyanoy). Each design incorporates distinctive features such as ears, horns, beards, or other 
characteristic elements while maintaining printability and structural integrity.
""", body_style))

story.append(Paragraph("<b>1.1 Target Age Group</b>", h2_style))

age_data = [
    [Paragraph("<b>Age Range</b>", table_header), Paragraph("<b>Face Width</b>", table_header), Paragraph("<b>Face Height</b>", table_header), Paragraph("<b>Recommended Mask</b>", table_header)],
    [Paragraph("4-5 years", table_cell_left), Paragraph("120-140 mm", table_cell), Paragraph("130-145 mm", table_cell), Paragraph("Scale: 0.85", table_cell)],
    [Paragraph("6-8 years", table_cell_left), Paragraph("140-160 mm", table_cell), Paragraph("145-155 mm", table_cell), Paragraph("Scale: 0.95", table_cell)],
    [Paragraph("9-10 years", table_cell_left), Paragraph("155-170 mm", table_cell), Paragraph("150-165 mm", table_cell), Paragraph("Scale: 1.0 (default)", table_cell)],
]

age_table = Table(age_data, colWidths=[3*cm, 3.5*cm, 3.5*cm, 4.5*cm])
age_table.setStyle(TableStyle([
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
story.append(Spacer(1, 10))
story.append(age_table)
story.append(Paragraph("Table 1: Age-Appropriate Sizing Guide", caption_style))

# ============================================
# РАЗДЕЛ 2: ТЕХНИЧЕСКИЕ СПЕЦИФИКАЦИИ
# ============================================
story.append(Paragraph("<b>2. Technical Specifications</b>", h1_style))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>2.1 Base Mask Dimensions</b>", h2_style))

dims_data = [
    [Paragraph("<b>Parameter</b>", table_header), Paragraph("<b>Value (mm)</b>", table_header), Paragraph("<b>Notes</b>", table_header)],
    [Paragraph("Overall Width", table_cell_left), Paragraph("180", table_cell), Paragraph("Fits most children 4-10 years", table_cell_left)],
    [Paragraph("Overall Height", table_cell_left), Paragraph("160", table_cell), Paragraph("From forehead to chin", table_cell_left)],
    [Paragraph("Depth (face curve)", table_cell_left), Paragraph("45", table_cell), Paragraph("Comfortable curve for face", table_cell_left)],
    [Paragraph("Wall Thickness", table_cell_left), Paragraph("3.0", table_cell), Paragraph("Minimum for SLA durability", table_cell_left)],
    [Paragraph("Eye Hole Width", table_cell_left), Paragraph("35", table_cell), Paragraph("Elliptical opening", table_cell_left)],
    [Paragraph("Eye Hole Height", table_cell_left), Paragraph("25", table_cell), Paragraph("Allows glasses underneath", table_cell_left)],
    [Paragraph("Eye Spacing", table_cell_left), Paragraph("60", table_cell), Paragraph("Distance between centers", table_cell_left)],
    [Paragraph("Strap Slot Width", table_cell_left), Paragraph("12", table_cell), Paragraph("Fits standard elastic", table_cell_left)],
    [Paragraph("Strap Slot Height", table_cell_left), Paragraph("4", table_cell), Paragraph("Pass-through opening", table_cell_left)],
]

dims_table = Table(dims_data, colWidths=[4*cm, 3*cm, 7.5*cm])
dims_table.setStyle(TableStyle([
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
    ('BACKGROUND', (0, 9), (-1, 9), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(Spacer(1, 10))
story.append(dims_table)
story.append(Paragraph("Table 2: Base Mask Dimensional Specifications", caption_style))

story.append(Paragraph("<b>2.2 SLA Printing Requirements</b>", h2_style))

sla_data = [
    [Paragraph("<b>Parameter</b>", table_header), Paragraph("<b>Minimum</b>", table_header), Paragraph("<b>Recommended</b>", table_header)],
    [Paragraph("Layer Height", table_cell_left), Paragraph("0.025 mm", table_cell), Paragraph("0.05-0.1 mm", table_cell)],
    [Paragraph("Exposure Time", table_cell_left), Paragraph("6-8 sec", table_cell), Paragraph("8-12 sec (base)", table_cell)],
    [Paragraph("Support Density", table_cell_left), Paragraph("40%", table_cell), Paragraph("50-60%", table_cell)],
    [Paragraph("Print Orientation", table_cell_left), Paragraph("45 deg tilt", table_cell), Paragraph("Face up, 15-30 deg", table_cell)],
    [Paragraph("Hollow Print", table_cell_left), Paragraph("Yes", table_cell), Paragraph("2-3mm walls, 2mm holes", table_cell)],
]

sla_table = Table(sla_data, colWidths=[4.5*cm, 4*cm, 5.5*cm])
sla_table.setStyle(TableStyle([
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
story.append(sla_table)
story.append(Paragraph("Table 3: SLA Printer Settings", caption_style))

# ============================================
# РАЗДЕЛ 3: МАСКИ ЖИВОТНЫХ
# ============================================
story.append(Paragraph("<b>3. Animal Masks</b>", h1_style))
story.append(Spacer(1, 10))

story.append(Paragraph("""
The animal mask collection features nine distinctive designs, each capturing the essential characteristics 
of the creature while maintaining wearability and printability. All animal masks share a common base form 
with species-specific modifications to ears, nose, teeth, and facial features.
""", body_style))

story.append(Paragraph("<b>3.1 Wolf Mask</b>", h2_style))
story.append(Paragraph("""
The Wolf mask features pointed ears, an elongated snout, prominent fangs, and fierce eyebrows. The design 
emphasizes the predatory nature while remaining child-friendly. Ears are positioned at 20-degree angles 
with internal supports for durability during active play.
""", body_style))

wolf_data = [
    [Paragraph("<b>Feature</b>", table_header), Paragraph("<b>Specification</b>", table_header), Paragraph("<b>Notes</b>", table_header)],
    [Paragraph("Ear Type", table_cell_left), Paragraph("Pointed, 35mm tall", table_cell), Paragraph("Reinforced base", table_cell_left)],
    [Paragraph("Nose", table_cell_left), Paragraph("Elongated, 15mm", table_cell), Paragraph("Black coloring recommended", table_cell_left)],
    [Paragraph("Teeth", table_cell_left), Paragraph("Fangs, 12mm", table_cell), Paragraph("Optional feature", table_cell_left)],
    [Paragraph("Base Color", table_cell_left), Paragraph("Gray (0.45, 0.45, 0.50)", table_cell), Paragraph("Airbrush or paint", table_cell_left)],
]

wolf_table = Table(wolf_data, colWidths=[4*cm, 4.5*cm, 6*cm])
wolf_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, -1), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(Spacer(1, 8))
story.append(wolf_table)
story.append(Paragraph("Table 4: Wolf Mask Specifications", caption_style))

story.append(Paragraph("<b>3.2 Fox Mask</b>", h2_style))
story.append(Paragraph("""
The Fox mask showcases large triangular ears with pink inner details, a pointed snout with black nose, 
and distinctive white muzzle markings. The orange-red color scheme makes this mask particularly popular 
for autumn festivals and forest-themed events.
""", body_style))

story.append(Paragraph("<b>3.3 Rabbit Mask</b>", h2_style))
story.append(Paragraph("""
The Rabbit mask features characteristic long ears (up to 75mm extended), a small pink nose, prominent 
front teeth, and rounded cheeks. The design includes internal ear supports to prevent drooping during wear. 
White or cream base color with pink accents.
""", body_style))

story.append(Paragraph("<b>3.4 Bear Mask</b>", h2_style))
story.append(Paragraph("""
The Bear mask presents a friendly brown bear face with small rounded ears, a large black nose, and 
extended muzzle. The robust construction suits active play. Recommended in brown with cream muzzle 
and black nose detail.
""", body_style))

story.append(Paragraph("<b>3.5 Lynx Mask</b>", h2_style))
story.append(Paragraph("""
The Lynx mask is distinguished by tufted ears with black tips, distinctive facial ruff (side whiskers), 
and spotted fur texture on the face surface. The most complex animal mask in the collection, featuring 
multiple small detail elements.
""", body_style))

story.append(Paragraph("<b>3.6 Frog Mask</b>", h2_style))
story.append(Paragraph("""
The Frog mask features bulging eyes positioned above the face plane, a wide mouth, and textured skin 
with small warts. Bright green base color with yellow accents. Eye openings are positioned to allow 
clear downward vision.
""", body_style))

story.append(Paragraph("<b>3.7 Raven and Crow Masks</b>", h2_style))
story.append(Paragraph("""
The Raven mask (black) features a curved beak and head feather tufts. The Crow mask (gray-brown) has 
a shorter beak and simpler feather arrangement. Both include textured feather patterns on the face 
surface for painting guidance.
""", body_style))

story.append(Paragraph("<b>3.8 Squirrel Mask</b>", h2_style))
story.append(Paragraph("""
The Squirrel mask displays large pointed ears with tufts, fluffy white cheeks, and a small black nose. 
The design captures the curious, energetic expression characteristic of squirrels. Orange-brown base 
with white cheek accents.
""", body_style))

# ============================================
# РАЗДЕЛ 4: МАСКИ СКАЗОЧНЫХ ПЕРСОНАЖЕЙ
# ============================================
story.append(Paragraph("<b>4. Fairy Tale Character Masks</b>", h1_style))
story.append(Spacer(1, 10))

story.append(Paragraph("""
Russian fairy tale characters form a unique category of masks designed for traditional celebrations, 
school performances, and New Year festivities. These designs incorporate distinctive elements like 
horns, beards, crowns, and magical accessories.
""", body_style))

story.append(Paragraph("<b>4.1 Baba Yaga Mask</b>", h2_style))

yaga_data = [
    [Paragraph("<b>Feature</b>", table_header), Paragraph("<b>Specification</b>", table_header), Paragraph("<b>Notes</b>", table_header)],
    [Paragraph("Hair", table_cell_left), Paragraph("Wild, disheveled", table_cell), Paragraph("5 spike elements", table_cell_left)],
    [Paragraph("Nose", table_cell_left), Paragraph("Hooked, 50mm long", table_cell), Paragraph("Distinctive feature", table_cell_left)],
    [Paragraph("Warts", table_cell_left), Paragraph("2-3 small bumps", table_cell), Paragraph("On nose and cheek", table_cell_left)],
    [Paragraph("Eyebrows", table_cell_left), Paragraph("Bushy, angled down", table_cell), Paragraph("Fierce expression", table_cell_left)],
    [Paragraph("Base Color", table_cell_left), Paragraph("Dark beige/olive", table_cell), Paragraph("Weathered appearance", table_cell_left)],
]

yaga_table = Table(yaga_data, colWidths=[4*cm, 4.5*cm, 6*cm])
yaga_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, -1), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(Spacer(1, 8))
story.append(yaga_table)
story.append(Paragraph("Table 5: Baba Yaga Mask Specifications", caption_style))

story.append(Paragraph("<b>4.2 Koschei the Deathless Mask</b>", h2_style))
story.append(Paragraph("""
The Koschei mask represents the skeletal villain from Russian folklore. Features include short horns, 
a thin goatee beard, angular mustache, and hollow cheekbones. The pale green-gray base color emphasizes 
the undead appearance. Suitable for older children (8+).
""", body_style))

story.append(Paragraph("<b>4.3 Snegurochka (Snow Maiden) Mask</b>", h2_style))
story.append(Paragraph("""
The Snegurochka mask portrays the granddaughter of Ded Moroz with delicate feminine features. Includes 
braided hair elements on the sides and a small crown or kokoshnik headdress element. Pale blue-white 
base with silver or pearl accents.
""", body_style))

story.append(Paragraph("<b>4.4 Ded Moroz (Grandfather Frost) Mask</b>", h2_style))

moroz_data = [
    [Paragraph("<b>Feature</b>", table_header), Paragraph("<b>Specification</b>", table_header), Paragraph("<b>Notes</b>", table_header)],
    [Paragraph("Beard", table_cell_left), Paragraph("Full, white, 60mm", table_cell), Paragraph("Textured surface", table_cell_left)],
    [Paragraph("Mustache", table_cell_left), Paragraph("Thick, white", table_cell), Paragraph("Curled tips", table_cell_left)],
    [Paragraph("Eyebrows", table_cell_left), Paragraph("Bushy, white", table_cell), Paragraph("Matching beard", table_cell_left)],
    [Paragraph("Hat", table_cell_left), Paragraph("Pointed, red", table_cell), Paragraph("Optional 3D element", table_cell_left)],
    [Paragraph("Cheeks", table_cell_left), Paragraph("Rosy pink circles", table_cell), Paragraph("Jolly expression", table_cell_left)],
    [Paragraph("Base Color", table_cell_left), Paragraph("Red with white trim", table_cell), Paragraph("Traditional colors", table_cell_left)],
]

moroz_table = Table(moroz_data, colWidths=[4*cm, 4.5*cm, 6*cm])
moroz_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, -1), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(Spacer(1, 8))
story.append(moroz_table)
story.append(Paragraph("Table 6: Ded Moroz Mask Specifications", caption_style))

story.append(Paragraph("<b>4.5 Leshy (Forest Spirit) Mask</b>", h2_style))
story.append(Paragraph("""
The Leshy mask embodies the forest guardian with branching antler-like horns, wild leaf-textured hair, 
a mossy beard, and green-brown coloring. Horns are designed with support-friendly geometry. The most 
complex fairy tale mask with multiple organic elements.
""", body_style))

story.append(Paragraph("<b>4.6 Vodyanoy (Water Spirit) Mask</b>", h2_style))
story.append(Paragraph("""
The Vodyanoy mask represents the water dwelling spirit with gills on cheeks, bulging frog-like eyes, 
a flat hat element, and flowing hair/beard suggesting water movement. Green-blue swamp color scheme 
with darker accents.
""", body_style))

# ============================================
# РАЗДЕЛ 5: ПЕЧАТЬ
# ============================================
story.append(Paragraph("<b>5. Printing Guidelines</b>", h1_style))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>5.1 Material Recommendations</b>", h2_style))

material_data = [
    [Paragraph("<b>Material Type</b>", table_header), Paragraph("<b>Properties</b>", table_header), Paragraph("<b>Best For</b>", table_header)],
    [Paragraph("Standard Resin", table_cell_left), Paragraph("Good detail, brittle", table_cell), Paragraph("Display masks", table_cell_left)],
    [Paragraph("Tough Resin", table_cell_left), Paragraph("Impact resistant", table_cell), Paragraph("Active play", table_cell_left)],
    [Paragraph("Skin-Safe Resin", table_cell_left), Paragraph("Biocompatible", table_cell), Paragraph("Extended wear", table_cell_left)],
    [Paragraph("Water-Washable", table_cell_left), Paragraph("Easy cleanup", table_cell), Paragraph("Beginners", table_cell_left)],
]

material_table = Table(material_data, colWidths=[4*cm, 5*cm, 5.5*cm])
material_table.setStyle(TableStyle([
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
]))
story.append(Spacer(1, 8))
story.append(material_table)
story.append(Paragraph("Table 7: Resin Material Selection Guide", caption_style))

story.append(Paragraph("<b>5.2 Print Orientation</b>", h2_style))

story.append(Paragraph("""
Optimal print orientation minimizes support marks on visible surfaces. Position the mask face-up at a 
15-30 degree angle from horizontal. This orientation reduces the need for supports on facial features 
while maintaining good layer adhesion. Add drainage holes at the bottom edge when printing hollow.
""", body_style))

story.append(Paragraph("<b>5.3 Support Strategy</b>", h2_style))

story.append(Paragraph("""
Use medium-density supports (50-60%) with heavy supports under protruding elements like ears and horns. 
Light supports suffice for the main face surface. Critical areas (eyes, nose, mouth) should have minimal 
supports to preserve detail. Post-cure supports before removal to prevent surface damage.
""", body_style))

# ============================================
# РАЗДЕЛ 6: ПОСТОБРАБОТКА
# ============================================
story.append(Paragraph("<b>6. Post-Processing</b>", h1_style))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>6.1 Surface Finishing Steps</b>", h2_style))

steps = [
    "1. Remove supports while resin is still slightly flexible (before final cure)",
    "2. Rinse in IPA (99%) for 10-15 minutes",
    "3. Cure under UV light for 5-10 minutes (check manufacturer guidelines)",
    "4. Sand support marks with 400-600 grit sandpaper",
    "5. Apply primer spray for better paint adhesion",
    "6. Paint with acrylic paints (recommended for child-safe finish)",
    "7. Apply clear coat sealer for durability",
    "8. Attach elastic strap through side slots",
]

for step in steps:
    story.append(Paragraph(step, body_style))

story.append(Paragraph("<b>6.2 Painting Recommendations</b>", h2_style))

paint_data = [
    [Paragraph("<b>Paint Type</b>", table_header), Paragraph("<b>Application</b>", table_header), Paragraph("<b>Safety</b>", table_header)],
    [Paragraph("Acrylic", table_cell_left), Paragraph("Brush or airbrush", table_cell), Paragraph("Water-based, safe for children", table_cell_left)],
    [Paragraph("Enamel", table_cell_left), Paragraph("Brush application", table_cell), Paragraph("Requires ventilation, durable", table_cell_left)],
    [Paragraph("Spray Paint", table_cell_left), Paragraph("Base coat only", table_cell), Paragraph("Use outdoors, wear mask", table_cell_left)],
]

paint_table = Table(paint_data, colWidths=[4*cm, 5*cm, 5.5*cm])
paint_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HEADER_COLOR),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('BACKGROUND', (0, 1), (-1, 1), ROW_EVEN),
    ('BACKGROUND', (0, 2), (-1, 2), ROW_ODD),
    ('BACKGROUND', (0, 3), (-1, 3), ROW_EVEN),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(Spacer(1, 8))
story.append(paint_table)
story.append(Paragraph("Table 8: Paint Selection Guide", caption_style))

# ============================================
# РАЗДЕЛ 7: ИСПОЛЬЗОВАНИЕ СКРИПТА
# ============================================
story.append(Paragraph("<b>7. Using the Blender Script</b>", h1_style))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>7.1 Running the Script</b>", h2_style))

blender_steps = [
    "1. Open Blender (version 3.0 or later)",
    "2. Navigate to Scripting workspace (top menu bar)",
    "3. Click 'New' to create a new text block",
    "4. Copy the entire 'party_masks_blender.py' script",
    "5. Paste into the text editor",
    "6. Press 'Run Script' (Alt+P) or click the play button",
    "7. All 15 masks will appear in the viewport",
]

for step in blender_steps:
    story.append(Paragraph(step, body_style))

story.append(Paragraph("<b>7.2 Exporting for Printing</b>", h2_style))

story.append(Paragraph("""
After generating the models, export individual masks in STL format for your slicer software. Select 
the desired mask, then use File > Export > Stl (.stl). Set the scale factor to 1000 (meters to 
millimeters) for correct sizing in most slicer applications.
""", body_style))

story.append(Paragraph("<b>7.3 Customization Options</b>", h2_style))

story.append(Paragraph("""
The script includes adjustable parameters at the top of the file. Key values that can be modified 
include overall mask dimensions, eye hole sizes, and strap slot dimensions. When modifying, maintain 
proportional relationships to preserve the character's distinctive appearance.
""", body_style))

# Сборка документа
doc.build(story)
print(f"PDF created: {output_path}")
