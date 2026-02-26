"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     МАСКИ ДЛЯ ДЕТСКИХ ПРАЗДНИКОВ - Blender Python Script                    ║
║     Party Masks for Children                                                ║
║                                                                              ║
║     15 персонажей:                                                           ║
║     - Животные: Волк, Лис, Заяц, Медведь, Рысь, Лягушка, Ворона, Ворон, Белка║
║     - Сказочные: Баба-яга, Кощей, Снегурочка, Дед-Мороз, Леший, Водяной      ║
║                                                                              ║
║     Совместимость: Blender 3.x / 4.x / 5.x                                   ║
║     Для печати на SLA 3D-принтере                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Инструкция:
1. Blender → Scripting → New
2. Вставь скрипт
3. Run Script (Alt+P)
4. Выбери нужную маску в меню

Версия: 1.0
"""

import bpy
import bmesh
import math
from mathutils import Vector, Matrix
import os

# ============================================================================
# ГЛОБАЛЬНЫЕ НАСТРОЙКИ
# ============================================================================

class MaskSettings:
    """Настройки для всех масок"""
    
    # Размер маски (в метрах) - для детей 4-10 лет
    MASK_WIDTH = 0.180      # 180 мм ширина
    MASK_HEIGHT = 0.160     # 160 мм высота
    MASK_DEPTH = 0.045      # 45 мм глубина
    MASK_THICKNESS = 0.003  # 3 мм толщина стенки
    
    # Глаза
    EYE_WIDTH = 0.035       # 35 мм ширина отверстия
    EYE_HEIGHT = 0.025      # 25 мм высота отверстия
    EYE_SPACING = 0.060     # 60 мм расстояние между центрами глаз
    EYE_Y_POSITION = 0.020  # 20 мм от центра вверх
    
    # Нос/дыхание
    NOSE_HOLE_WIDTH = 0.020   # 20 мм
    NOSE_HOLE_HEIGHT = 0.015  # 15 мм
    NOSE_Y_POSITION = -0.020  # 20 мм от центра вниз
    
    # Крепления для резинки
    STRAP_WIDTH = 0.012      # 12 мм ширина паза
    STRAP_HEIGHT = 0.004     # 4 мм высота паза
    STRAP_POSITION = 0.040   # 40 мм от центра по бокам
    
    # Материалы (цвета)
    COLORS = {
        'wolf': (0.45, 0.45, 0.50, 1.0),        # Серый
        'fox': (0.85, 0.55, 0.25, 1.0),         # Рыжий
        'rabbit': (0.95, 0.93, 0.90, 1.0),      # Белый/бежевый
        'bear': (0.40, 0.30, 0.20, 1.0),        # Коричневый
        'lynx': (0.70, 0.65, 0.55, 1.0),        # Светло-серый
        'baba_yaga': (0.55, 0.45, 0.35, 1.0),   # Тёмно-бежевый
        'koschei': (0.60, 0.70, 0.65, 1.0),     # Бледно-зелёный
        'snegurochka': (0.85, 0.92, 0.98, 1.0), # Голубовато-белый
        'ded_moroz': (0.90, 0.20, 0.15, 1.0),   # Красный
        'leshy': (0.30, 0.50, 0.25, 1.0),       # Зелёный
        'vodyanoy': (0.30, 0.55, 0.50, 1.0),    # Болотный
        'frog': (0.40, 0.70, 0.35, 1.0),        # Ярко-зелёный
        'crow': (0.15, 0.15, 0.15, 1.0),        # Чёрный (ворон)
        'raven': (0.20, 0.18, 0.15, 1.0),       # Тёмно-коричневый (ворона)
        'squirrel': (0.75, 0.50, 0.30, 1.0),    # Рыжий (белка)
    }


def clear_scene():
    """Очищает сцену"""
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)


def create_material(name, color):
    """Создаёт материал"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = 0.4
    bsdf.inputs['Metallic'].default_value = 0.1
    return mat


def create_base_mask(name, color):
    """
    Создаёт базовую форму маски (овал лица)
    Возвращает объект маски
    """
    # Создаём UV сферу как основу
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=MaskSettings.MASK_WIDTH * 0.55,
        location=(0, -MaskSettings.MASK_DEPTH * 0.3, 0)
    )
    mask = bpy.context.active_object
    mask.name = name
    
    # Масштабируем под форму лица
    mask.scale = (1.0, MaskSettings.MASK_DEPTH / MaskSettings.MASK_WIDTH, 
                  MaskSettings.MASK_HEIGHT / MaskSettings.MASK_WIDTH)
    
    # Применяем масштаб
    bpy.context.view_layer.objects.active = mask
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Добавляем материал
    mat = create_material(name + "_material", color)
    mask.data.materials.append(mat)
    
    return mask


def add_eye_holes(mask):
    """Добавляет отверстия для глаз"""
    eye_w = MaskSettings.EYE_WIDTH
    eye_h = MaskSettings.EYE_HEIGHT
    spacing = MaskSettings.EYE_SPACING / 2
    y_pos = MaskSettings.EYE_Y_POSITION
    
    for side in [-1, 1]:
        # Создаём эллипс для глаза
        bpy.ops.mesh.primitive_cylinder_add(
            radius=eye_w / 2,
            depth=MaskSettings.MASK_DEPTH * 3,
            location=(side * spacing, y_pos, 0)
        )
        eye = bpy.context.active_object
        eye.scale = (1.0, eye_h / eye_w, 1.0)
        
        # Применяем boolean разницу
        modifier = mask.modifiers.new(name=f"Eye_{side}", type='BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = eye
        bpy.context.view_layer.objects.active = mask
        bpy.ops.object.modifier_apply(modifier=f"Eye_{side}")
        
        # Удаляем временный объект
        bpy.data.objects.remove(eye, do_unlink=True)


def add_nose_hole(mask):
    """Добавляет отверстие для носа/дыхания"""
    nose_w = MaskSettings.NOSE_HOLE_WIDTH
    nose_h = MaskSettings.NOSE_HOLE_HEIGHT
    y_pos = MaskSettings.NOSE_Y_POSITION
    
    # Создаём овальное отверстие
    bpy.ops.mesh.primitive_cylinder_add(
        radius=nose_w / 2,
        depth=MaskSettings.MASK_DEPTH * 3,
        location=(0, y_pos, 0)
    )
    nose = bpy.context.active_object
    nose.scale = (1.0, nose_h / nose_w, 1.0)
    
    # Boolean разница
    modifier = mask.modifiers.new(name="Nose", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = nose
    bpy.context.view_layer.objects.active = mask
    bpy.ops.object.modifier_apply(modifier="Nose")
    
    bpy.data.objects.remove(nose, do_unlink=True)


def add_strap_slots(mask):
    """Добавляет пазы для резинки"""
    strap_w = MaskSettings.STRAP_WIDTH
    strap_h = MaskSettings.STRAP_HEIGHT
    position = MaskSettings.STRAP_POSITION
    
    for side in [-1, 1]:
        # Создаём паз
        bpy.ops.mesh.primitive_cube_add(size=1)
        slot = bpy.context.active_object
        slot.scale = (strap_w * 2, strap_h * 2, MaskSettings.MASK_THICKNESS * 2)
        slot.location = (side * position, 0, MaskSettings.MASK_THICKNESS)
        
        # Boolean разница
        modifier = mask.modifiers.new(name=f"Strap_{side}", type='BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = slot
        bpy.context.view_layer.objects.active = mask
        bpy.ops.object.modifier_apply(modifier=f"Strap_{side}")
        
        bpy.data.objects.remove(slot, do_unlink=True)


def add_ears(mask, ear_type='rounded', size=0.04, position=(0.06, 0.08, 0.02), rotation=(0, 0, 15)):
    """
    Добавляет уши к маске
    
    ear_type: 'rounded', 'pointed', 'long', 'bear', 'cat'
    """
    ear_scale = size
    pos_x, pos_y, pos_z = position
    rot_x, rot_y, rot_z = rotation
    
    for side in [-1, 1]:
        if ear_type == 'rounded':
            # Круглые уши (мышь, заяц)
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=ear_scale,
                location=(side * pos_x, pos_y, pos_z)
            )
        elif ear_type == 'pointed':
            # Острые уши (волк, лиса, белка)
            bpy.ops.mesh.primitive_cone_add(
                radius1=ear_scale * 0.6,
                radius2=0,
                depth=ear_scale * 2,
                location=(side * pos_x, pos_y, pos_z)
            )
        elif ear_type == 'long':
            # Длинные уши (заяц)
            bpy.ops.mesh.primitive_cone_add(
                radius1=ear_scale * 0.4,
                radius2=0,
                depth=ear_scale * 3,
                location=(side * pos_x, pos_y + ear_scale, pos_z)
            )
        elif ear_type == 'bear':
            # Круглые маленькие уши (медведь)
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=ear_scale * 0.6,
                location=(side * pos_x, pos_y, pos_z)
            )
        elif ear_type == 'cat':
            # Кошачьи уши с кисточками (рысь)
            bpy.ops.mesh.primitive_cone_add(
                radius1=ear_scale * 0.5,
                radius2=ear_scale * 0.15,
                depth=ear_scale * 2,
                location=(side * pos_x, pos_y, pos_z)
            )
        
        ear = bpy.context.active_object
        ear.name = f"Ear_{side}"
        ear.rotation_euler = (math.radians(rot_x), math.radians(rot_y), 
                              math.radians(rot_z * side))
        
        # Присоединяем к маске
        ear.data.materials.append(mask.data.materials[0])


def add_nose(mask, nose_type='small', size=0.02, position=(0, 0.02, 0.04), color=None):
    """
    Добавляет нос к маске
    
    nose_type: 'small', 'button', 'long', 'bear', 'pig'
    """
    pos_x, pos_y, pos_z = position
    
    if nose_type == 'small':
        # Маленький круглый нос
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=size,
            location=(pos_x, pos_y, pos_z)
        )
    elif nose_type == 'button':
        # Пуговка (кошка, лиса)
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=size * 1.2,
            location=(pos_x, pos_y, pos_z)
        )
        # Ноздри
        for side in [-1, 1]:
            bpy.ops.mesh.primitive_cylinder_add(
                radius=size * 0.2,
                depth=size * 0.5,
                location=(pos_x + side * size * 0.3, pos_y, pos_z + size * 0.3)
            )
            nostril = bpy.context.active_object
            nostril.rotation_euler = (math.radians(90), 0, 0)
    elif nose_type == 'long':
        # Длинный нос (волк, собака)
        bpy.ops.mesh.primitive_cone_add(
            radius1=size * 0.8,
            radius2=size * 0.3,
            depth=size * 3,
            location=(pos_x, pos_y, pos_z + size)
        )
    elif nose_type == 'bear':
        # Медвежий нос (большой плоский)
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=size * 1.5,
            location=(pos_x, pos_y, pos_z)
        )
        nose_obj = bpy.context.active_object
        nose_obj.scale = (1.0, 0.6, 0.8)
    
    nose_obj = bpy.context.active_object
    nose_obj.name = "Nose"
    
    # Создаём материал для носа (обычно чёрный)
    if color is None:
        color = (0.1, 0.1, 0.1, 1.0)  # Чёрный
    nose_mat = create_material("Nose_material", color)
    nose_obj.data.materials.append(nose_mat)


def add_horns(mask, horn_type='short', size=0.03, position=(0.05, 0.10, 0.01)):
    """Добавляет рога"""
    pos_x, pos_y, pos_z = position
    
    for side in [-1, 1]:
        if horn_type == 'short':
            # Короткие рога (кощей, баран)
            bpy.ops.mesh.primitive_cone_add(
                radius1=size * 0.5,
                radius2=0,
                depth=size * 2,
                location=(side * pos_x, pos_y, pos_z)
            )
        elif horn_type == 'curved':
            # Изогнутые рога (демон, чёрт)
            bpy.ops.mesh.primitive_torus_add(
                major_radius=size,
                minor_radius=size * 0.2,
                location=(side * pos_x, pos_y, pos_z)
            )
        
        horn = bpy.context.active_object
        horn.name = f"Horn_{side}"
        horn.rotation_euler = (math.radians(30), 0, math.radians(20 * side))
        
        # Материал для рогов
        horn_mat = create_material("Horn_material", (0.3, 0.25, 0.2, 1.0))
        horn.data.materials.append(horn_mat)


def add_beard(mask, beard_type='full', size=0.06, position=(0, -0.04, 0.03)):
    """Добавляет бороду"""
    pos_x, pos_y, pos_z = position
    
    if beard_type == 'full':
        # Полная борода (Дед Мороз)
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=size,
            location=(pos_x, pos_y, pos_z)
        )
        beard = bpy.context.active_object
        beard.scale = (1.2, 0.6, 1.0)
    elif beard_type == 'goatee':
        # Козлиная бородка (Кощей, чёрт)
        bpy.ops.mesh.primitive_cone_add(
            radius1=size * 0.5,
            radius2=size * 0.1,
            depth=size * 1.5,
            location=(pos_x, pos_y - size * 0.5, pos_z)
        )
    elif beard_type == 'bushy':
        # Пышная борода (Леший)
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=size * 1.2,
            location=(pos_x, pos_y, pos_z)
        )
    
    beard = bpy.context.active_object
    beard.name = "Beard"
    
    # Материал бороды (белый или серый)
    beard_mat = create_material("Beard_material", (0.95, 0.95, 0.95, 1.0))
    beard.data.materials.append(beard_mat)


def add_mustache(mask, size=0.03, position=(0, 0.0, 0.03)):
    """Добавляет усы"""
    pos_x, pos_y, pos_z = position
    
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=size * 0.3,
            depth=size * 2,
            location=(side * pos_x * 2, pos_y, pos_z)
        )
        mustache = bpy.context.active_object
        mustache.rotation_euler = (math.radians(90), math.radians(30 * side), 0)
        mustache.name = f"Mustache_{side}"
        
        mustache_mat = create_material("Mustache_material", (0.3, 0.25, 0.2, 1.0))
        mustache.data.materials.append(mustache_mat)


def add_hair(mask, hair_type='wild', size=0.04, position=(0, 0.08, 0.02)):
    """Добавляет волосы/гриву"""
    pos_x, pos_y, pos_z = position
    
    if hair_type == 'wild':
        # Дикие волосы (Баба-яга, Леший)
        for i in range(5):
            angle = (i - 2) * 15
            bpy.ops.mesh.primitive_cone_add(
                radius1=size * 0.3,
                radius2=size * 0.05,
                depth=size * 2,
                location=(pos_x + (i - 2) * size * 0.4, pos_y, pos_z)
            )
            hair = bpy.context.active_object
            hair.rotation_euler = (math.radians(20 + i * 5), 0, 0)
            hair.data.materials.append(mask.data.materials[0])
    elif hair_type == 'braided':
        # Косы (Снегурочка)
        for side in [-1, 1]:
            for j in range(3):
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=size * 0.15,
                    depth=size * 3,
                    location=(side * size * 2, -size * j * 0.5, pos_z + side * size * 0.5)
                )
                braid = bpy.context.active_object
                braid.rotation_euler = (0, 0, math.radians(side * 15))
                braid_mat = create_material("Hair_material", (0.9, 0.85, 0.7, 1.0))
                braid.data.materials.append(braid_mat)
    elif hair_type == 'bushy':
        # Пышные волосы (Водяной)
        for i in range(8):
            angle = i * 45
            rad = math.radians(angle)
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=size * 0.5,
                location=(pos_x + math.cos(rad) * size, 
                         pos_y + math.sin(rad) * size * 0.3, 
                         pos_z)
            )
            hair = bpy.context.active_object
            hair.data.materials.append(mask.data.materials[0])


def add_crown(mask, size=0.04, position=(0, 0.09, 0.02)):
    """Добавляет корону/венец"""
    pos_x, pos_y, pos_z = position
    
    # Основа короны
    bpy.ops.mesh.primitive_cylinder_add(
        radius=size * 1.2,
        depth=size * 0.5,
        location=(pos_x, pos_y, pos_z)
    )
    crown_base = bpy.context.active_object
    
    # Зубцы короны
    for i in range(5):
        angle = i * 72
        rad = math.radians(angle)
        bpy.ops.mesh.primitive_cone_add(
            radius1=size * 0.2,
            radius2=0,
            depth=size * 0.8,
            location=(pos_x + math.cos(rad) * size * 0.8,
                     pos_y + math.sin(rad) * size * 0.8,
                     pos_z + size * 0.4)
        )
        tooth = bpy.context.active_object
        tooth.data.materials.append(crown_base.data.materials[0])
    
    crown_mat = create_material("Crown_material", (0.85, 0.75, 0.2, 1.0))  # Золотой
    crown_base.data.materials.append(crown_mat)


def add_hat(mask, hat_type='pointed', size=0.06, position=(0, 0.08, 0.0)):
    """Добавляет шляпу"""
    pos_x, pos_y, pos_z = position
    
    if hat_type == 'pointed':
        # Остроконечная шляпа (Дед Мороз, Снегурочка)
        bpy.ops.mesh.primitive_cone_add(
            radius1=size * 0.8,
            radius2=0,
            depth=size * 2,
            location=(pos_x, pos_y + size * 0.5, pos_z)
        )
        hat = bpy.context.active_object
        hat.rotation_euler = (math.radians(-10), 0, 0)
    elif hat_type == 'wizard':
        # Шляпа волшебника
        bpy.ops.mesh.primitive_cone_add(
            radius1=size,
            radius2=0,
            depth=size * 2.5,
            location=(pos_x, pos_y + size * 0.7, pos_z)
        )
        hat = bpy.context.active_object
        hat.rotation_euler = (math.radians(-5), 0, math.radians(10))
    elif hat_type == 'flat':
        # Плоская шляпа (Водяной)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=size * 1.2,
            depth=size * 0.3,
            location=(pos_x, pos_y, pos_z)
        )
        hat = bpy.context.active_object
    
    hat.name = "Hat"
    hat_mat = create_material("Hat_material", (0.8, 0.2, 0.15, 1.0))
    hat.data.materials.append(hat_mat)


def add_teeth(mask, teeth_type='visible', size=0.015, position=(0, -0.035, 0.02)):
    """Добавляет зубы"""
    pos_x, pos_y, pos_z = position
    
    if teeth_type == 'visible':
        # Видимые зубы (кролик, бобр)
        for i in range(2):
            bpy.ops.mesh.primitive_cube_add(
                size=size,
                location=(pos_x + (i - 0.5) * size * 0.8, pos_y, pos_z + size * 0.5)
            )
            tooth = bpy.context.active_object
            tooth.scale = (0.5, 1.0, 2.0)
            tooth_mat = create_material("Tooth_material", (0.95, 0.95, 0.95, 1.0))
            tooth.data.materials.append(tooth_mat)
    elif teeth_type == 'fangs':
        # Клыки (волк, вампир)
        for side in [-1, 1]:
            bpy.ops.mesh.primitive_cone_add(
                radius1=size * 0.3,
                radius2=0,
                depth=size * 2,
                location=(side * size * 1.5, pos_y, pos_z)
            )
            fang = bpy.context.active_object
            fang_mat = create_material("Fang_material", (0.95, 0.95, 0.95, 1.0))
            fang.data.materials.append(fang_mat)


def add_beak(mask, beak_type='short', size=0.03, position=(0, 0.02, 0.04)):
    """Добавляет клюв (для птиц)"""
    pos_x, pos_y, pos_z = position
    
    if beak_type == 'short':
        # Короткий клюв (ворона, воробей)
        bpy.ops.mesh.primitive_cone_add(
            radius1=size * 0.6,
            radius2=size * 0.3,
            depth=size * 2,
            location=(pos_x, pos_y, pos_z + size * 0.8)
        )
    elif beak_type == 'long':
        # Длинный клюв (аист, цапля)
        bpy.ops.mesh.primitive_cone_add(
            radius1=size * 0.4,
            radius2=size * 0.1,
            depth=size * 4,
            location=(pos_x, pos_y, pos_z + size * 1.5)
        )
    elif beak_type == 'curved':
        # Изогнутый клюв (ворон, попугай)
        bpy.ops.mesh.primitive_torus_add(
            major_radius=size * 1.2,
            minor_radius=size * 0.25,
            location=(pos_x, pos_y, pos_z + size)
        )
    
    beak = bpy.context.active_object
    beak.name = "Beak"
    beak.rotation_euler = (math.radians(90), 0, 0)
    
    # Материал клюва
    beak_mat = create_material("Beak_material", (0.15, 0.12, 0.1, 1.0))
    beak.data.materials.append(beak_mat)


def add_eyebrows(mask, brow_type='bushy', size=0.02, position=(0.05, 0.045, 0.02)):
    """Добавляет брови"""
    pos_x, pos_y, pos_z = position
    
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=size * 0.4,
            depth=size * 3,
            location=(side * pos_x, pos_y, pos_z)
        )
        brow = bpy.context.active_object
        brow.rotation_euler = (math.radians(90), 0, math.radians(15 * side))
        brow.name = f"Eyebrow_{side}"
        
        brow_mat = create_material("Brow_material", (0.3, 0.25, 0.2, 1.0))
        brow.data.materials.append(brow_mat)


def add_warts(mask, count=3, size=0.008, positions=None):
    """Добавляет бородавки (лягушка, ведьма)"""
    if positions is None:
        positions = [
            (0.03, 0.0, 0.04),
            (-0.02, -0.01, 0.03),
            (0.0, 0.02, 0.035),
        ]
    
    for i, pos in enumerate(positions[:count]):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=size,
            location=pos
        )
        wart = bpy.context.active_object
        wart.name = f"Wart_{i}"
        wart.data.materials.append(mask.data.materials[0])


# ============================================================================
# СОЗДАНИЕ КОНКРЕТНЫХ МАСОК
# ============================================================================

def create_wolf_mask():
    """Маска Волка"""
    color = MaskSettings.COLORS['wolf']
    mask = create_base_mask("Wolf_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Острые уши
    add_ears(mask, ear_type='pointed', size=0.035, position=(0.055, 0.08, 0.02), rotation=(10, 0, 20))
    
    # Длинный нос
    add_nose(mask, nose_type='long', size=0.015, position=(0, 0.01, 0.05), color=(0.1, 0.1, 0.1, 1.0))
    
    # Клыки
    add_teeth(mask, teeth_type='fangs', size=0.012, position=(0, -0.035, 0.025))
    
    # Брови
    add_eyebrows(mask, brow_type='bushy', size=0.015, position=(0.05, 0.05, 0.03))
    
    return mask


def create_fox_mask():
    """Маска Лиса"""
    color = MaskSettings.COLORS['fox']
    mask = create_base_mask("Fox_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Большие острые уши
    add_ears(mask, ear_type='pointed', size=0.04, position=(0.055, 0.085, 0.02), rotation=(5, 0, 25))
    
    # Острый нос
    add_nose(mask, nose_type='button', size=0.012, position=(0, 0.01, 0.045), color=(0.1, 0.1, 0.1, 1.0))
    
    # Белая мордочка (добавляем белую область)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, location=(0, -0.01, 0.03))
    muzzle = bpy.context.active_object
    muzzle.scale = (1.0, 0.5, 0.6)
    white_mat = create_material("White_muzzle", (0.95, 0.95, 0.95, 1.0))
    muzzle.data.materials.append(white_mat)
    
    return mask


def create_rabbit_mask():
    """Маска Зайца"""
    color = MaskSettings.COLORS['rabbit']
    mask = create_base_mask("Rabbit_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Длинные уши
    add_ears(mask, ear_type='long', size=0.025, position=(0.035, 0.09, 0.0), rotation=(0, 10, 5))
    
    # Маленький нос
    add_nose(mask, nose_type='button', size=0.01, position=(0, 0.015, 0.04), color=(0.9, 0.7, 0.75, 1.0))
    
    # Заячьи зубы
    add_teeth(mask, teeth_type='visible', size=0.01, position=(0, -0.032, 0.025))
    
    # Щёчки
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=(side * 0.04, 0.0, 0.025))
        cheek = bpy.context.active_object
        cheek.scale = (0.8, 0.6, 0.5)
        cheek.data.materials.append(mask.data.materials[0])
    
    return mask


def create_bear_mask():
    """Маска Медведя"""
    color = MaskSettings.COLORS['bear']
    mask = create_base_mask("Bear_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Маленькие круглые уши
    add_ears(mask, ear_type='bear', size=0.025, position=(0.06, 0.07, 0.01))
    
    # Большой нос
    add_nose(mask, nose_type='bear', size=0.02, position=(0, 0.01, 0.045), color=(0.1, 0.1, 0.1, 1.0))
    
    # Морда
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(0, -0.01, 0.035))
    muzzle = bpy.context.active_object
    muzzle.scale = (1.0, 0.5, 0.6)
    muzzle.data.materials.append(mask.data.materials[0])
    
    return mask


def create_lynx_mask():
    """Маска Рыси"""
    color = MaskSettings.COLORS['lynx']
    mask = create_base_mask("Lynx_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Уши с кисточками
    add_ears(mask, ear_type='cat', size=0.035, position=(0.055, 0.085, 0.02), rotation=(5, 0, 20))
    
    # Боковая грива (бакенбарды)
    for side in [-1, 1]:
        for i in range(3):
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.015,
                location=(side * 0.07, 0.03 - i * 0.015, 0.02)
            )
            mane = bpy.context.active_object
            mane.scale = (1.0, 0.8, 0.6)
            mane.data.materials.append(mask.data.materials[0])
    
    # Нос
    add_nose(mask, nose_type='button', size=0.012, position=(0, 0.01, 0.04), color=(0.2, 0.15, 0.15, 1.0))
    
    return mask


def create_baba_yaga_mask():
    """Маска Бабы-яги"""
    color = MaskSettings.COLORS['baba_yaga']
    mask = create_base_mask("BabaYaga_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Дикие волосы
    add_hair(mask, hair_type='wild', size=0.035, position=(0, 0.07, 0.0))
    
    # Большой крючковатый нос
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.015,
        radius2=0.008,
        depth=0.05,
        location=(0, 0.02, 0.055)
    )
    nose = bpy.context.active_object
    nose.rotation_euler = (math.radians(-20), 0, 0)
    nose_mat = create_material("Witch_nose", (0.5, 0.4, 0.35, 1.0))
    nose.data.materials.append(nose_mat)
    
    # Бородавка
    add_warts(mask, count=2, size=0.006, positions=[(0.025, 0.01, 0.04), (-0.02, 0.0, 0.03)])
    
    # Брови
    add_eyebrows(mask, brow_type='bushy', size=0.018, position=(0.05, 0.05, 0.03))
    
    # Морщинки (линии)
    # Подбородок
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.015, location=(0, -0.04, 0.015))
    chin = bpy.context.active_object
    chin.scale = (1.2, 0.6, 0.4)
    chin.data.materials.append(mask.data.materials[0])
    
    return mask


def create_koschei_mask():
    """Маска Кощея Бессмертного"""
    color = MaskSettings.COLORS['koschei']
    mask = create_base_mask("Koschei_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Короткие рога
    add_horns(mask, horn_type='short', size=0.02, position=(0.04, 0.09, 0.01))
    
    # Козлиная бородка
    add_beard(mask, beard_type='goatee', size=0.025, position=(0, -0.035, 0.015))
    
    # Тонкие усы
    add_mustache(mask, size=0.02, position=(0, 0.0, 0.025))
    
    # Острые брови
    add_eyebrows(mask, brow_type='bushy', size=0.012, position=(0.05, 0.05, 0.03))
    
    # Впалые щёки (кости)
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.015, location=(side * 0.05, -0.01, 0.02))
        cheek = bpy.context.active_object
        cheek.scale = (1.0, 0.4, 0.8)
        cheek_mat = create_material("Cheek_bone", (0.55, 0.65, 0.6, 1.0))
        cheek.data.materials.append(cheek_mat)
    
    return mask


def create_snegurochka_mask():
    """Маска Снегурочки"""
    color = MaskSettings.COLORS['snegurochka']
    mask = create_base_mask("Snegurochka_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Косы
    add_hair(mask, hair_type='braided', size=0.025, position=(0.06, 0.05, 0.0))
    
    # Венец/корона
    add_crown(mask, size=0.03, position=(0, 0.08, 0.0))
    
    # Маленький носик
    add_nose(mask, nose_type='small', size=0.008, position=(0, 0.01, 0.035), color=(0.95, 0.85, 0.85, 1.0))
    
    # Румяные щёчки
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012, location=(side * 0.045, 0.0, 0.025))
        cheek = bpy.context.active_object
        cheek.scale = (0.8, 0.5, 0.4)
        blush_mat = create_material("Blush", (0.95, 0.7, 0.7, 1.0))
        cheek.data.materials.append(blush_mat)
    
    return mask


def create_ded_moroz_mask():
    """Маска Деда Мороза"""
    color = MaskSettings.COLORS['ded_moroz']
    mask = create_base_mask("DedMoroz_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Большая белая борода
    add_beard(mask, beard_type='full', size=0.05, position=(0, -0.03, 0.0))
    
    # Усы
    add_mustache(mask, size=0.025, position=(0, 0.0, 0.025))
    
    # Шапка
    add_hat(mask, hat_type='pointed', size=0.05, position=(0, 0.08, 0.0))
    
    # Румяные щёки
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=(side * 0.05, 0.01, 0.025))
        cheek = bpy.context.active_object
        cheek.scale = (1.0, 0.6, 0.5)
        blush_mat = create_material("Blush", (0.95, 0.75, 0.7, 1.0))
        cheek.data.materials.append(blush_mat)
    
    # Брови белые
    add_eyebrows(mask, brow_type='bushy', size=0.02, position=(0.05, 0.05, 0.03))
    # Перекрашиваем брови в белый
    for obj in bpy.data.objects:
        if "Eyebrow" in obj.name and len(obj.data.materials) > 0:
            obj.data.materials[0] = create_material("White_brow", (0.95, 0.95, 0.95, 1.0))
    
    return mask


def create_leshy_mask():
    """Маска Лешего"""
    color = MaskSettings.COLORS['leshy']
    mask = create_base_mask("Leshy_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Рога (ветвистые)
    for side in [-1, 1]:
        # Основной рог
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.012,
            radius2=0.003,
            depth=0.07,
            location=(side * 0.04, 0.09, 0.01)
        )
        horn = bpy.context.active_object
        horn.rotation_euler = (math.radians(30), 0, math.radians(15 * side))
        horn_mat = create_material("Antler", (0.35, 0.3, 0.2, 1.0))
        horn.data.materials.append(horn_mat)
        
        # Ответвления
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.008,
            radius2=0.002,
            depth=0.04,
            location=(side * 0.055, 0.1, 0.03)
        )
        branch = bpy.context.active_object
        branch.rotation_euler = (math.radians(20), math.radians(30 * side), 0)
        branch.data.materials.append(horn_mat)
    
    # Пышная борода из листьев/мха
    add_beard(mask, beard_type='bushy', size=0.045, position=(0, -0.025, 0.01))
    
    # Дикие волосы
    add_hair(mask, hair_type='wild', size=0.03, position=(0, 0.07, 0.0))
    
    # Брови
    add_eyebrows(mask, brow_type='bushy', size=0.02, position=(0.05, 0.05, 0.03))
    
    # Нос
    add_nose(mask, nose_type='button', size=0.015, position=(0, 0.01, 0.04), color=(0.3, 0.45, 0.25, 1.0))
    
    return mask


def create_vodyanoy_mask():
    """Маска Водяного"""
    color = MaskSettings.COLORS['vodyanoy']
    mask = create_base_mask("Vodyanoy_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Плоская шляпа
    add_hat(mask, hat_type='flat', size=0.045, position=(0, 0.075, 0.0))
    
    # Пышные волосы (водоросли)
    add_hair(mask, hair_type='bushy', size=0.04, position=(0, 0.06, 0.0))
    
    # Борода (водоросли)
    add_beard(mask, beard_type='bushy', size=0.05, position=(0, -0.035, 0.0))
    
    # Жабры на щеках
    for side in [-1, 1]:
        for i in range(3):
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.003,
                depth=0.015,
                location=(side * 0.055, 0.015 - i * 0.008, 0.025)
            )
            gill = bpy.context.active_object
            gill.rotation_euler = (0, math.radians(90), 0)
            gill_mat = create_material("Gill", (0.35, 0.55, 0.5, 1.0))
            gill.data.materials.append(gill_mat)
    
    # Выпученные глаза (налегающие)
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.012,
            location=(side * 0.03, 0.04, 0.045)
        )
        eye_bulge = bpy.context.active_object
        eye_bulge.scale = (1.0, 0.8, 0.6)
        eye_mat = create_material("Bulge_eye", (0.9, 0.95, 0.9, 1.0))
        eye_bulge.data.materials.append(eye_mat)
    
    return mask


def create_frog_mask():
    """Маска Лягушки"""
    color = MaskSettings.COLORS['frog']
    mask = create_base_mask("Frog_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Большие выпуклые глаза
    for side in [-1, 1]:
        # Основание глаза
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.022,
            location=(side * 0.04, 0.05, 0.035)
        )
        eye_base = bpy.context.active_object
        
        # Зрачок
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.012,
            location=(side * 0.04, 0.055, 0.045)
        )
        pupil = bpy.context.active_object
        pupil_mat = create_material("Pupil", (0.1, 0.15, 0.1, 1.0))
        pupil.data.materials.append(pupil_mat)
        
        eye_base.data.materials.append(mask.data.materials[0])
    
    # Широкий рот
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.04,
        depth=0.01,
        location=(0, -0.025, 0.02)
    )
    mouth = bpy.context.active_object
    mouth.scale = (1.5, 0.2, 0.5)
    mouth.rotation_euler = (math.radians(90), 0, 0)
    mouth_mat = create_material("Mouth", (0.25, 0.45, 0.2, 1.0))
    mouth.data.materials.append(mouth_mat)
    
    # Бородавки
    add_warts(mask, count=5, size=0.006, positions=[
        (0.03, 0.02, 0.04), (-0.025, 0.015, 0.038), 
        (0.0, 0.03, 0.035), (0.04, -0.01, 0.03), (-0.03, 0.0, 0.032)
    ])
    
    return mask


def create_raven_mask():
    """Маска Ворона (чёрный ворон)"""
    color = MaskSettings.COLORS['crow']
    mask = create_base_mask("Raven_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Изогнутый клюв
    add_beak(mask, beak_type='curved', size=0.025, position=(0, 0.01, 0.04))
    
    # Перья на голове
    for i in range(5):
        angle = (i - 2) * 20
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.008,
            radius2=0.002,
            depth=0.035,
            location=(angle * 0.001, 0.065 + abs(i-2) * 0.003, 0.01)
        )
        feather = bpy.context.active_object
        feather.rotation_euler = (math.radians(40 - abs(i-2) * 10), 0, math.radians(angle * 0.3))
        feather.data.materials.append(mask.data.materials[0])
    
    # Перья по бокам
    for side in [-1, 1]:
        for j in range(3):
            bpy.ops.mesh.primitive_cone_add(
                radius1=0.006,
                radius2=0.001,
                depth=0.03,
                location=(side * 0.06, 0.04 - j * 0.015, 0.01)
            )
        feather = bpy.context.active_object
        feather.rotation_euler = (math.radians(30), math.radians(side * 20), 0)
        feather.data.materials.append(mask.data.materials[0])
    
    return mask


def create_crow_mask():
    """Маска Вороны (серая)"""
    color = MaskSettings.COLORS['raven']
    mask = create_base_mask("Crow_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Короткий клюв
    add_beak(mask, beak_type='short', size=0.022, position=(0, 0.015, 0.04))
    
    # Перья на голове
    for i in range(4):
        angle = (i - 1.5) * 25
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.007,
            radius2=0.002,
            depth=0.03,
            location=(angle * 0.0008, 0.06, 0.01)
        )
        feather = bpy.context.active_object
        feather.rotation_euler = (math.radians(35), 0, math.radians(angle * 0.2))
        feather.data.materials.append(mask.data.materials[0])
    
    # Серое пятно на груди
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.025, location=(0, -0.02, 0.02))
    chest = bpy.context.active_object
    chest.scale = (1.2, 0.4, 0.5)
    chest_mat = create_material("Gray_chest", (0.5, 0.5, 0.48, 1.0))
    chest.data.materials.append(chest_mat)
    
    return mask


def create_squirrel_mask():
    """Маска Белки"""
    color = MaskSettings.COLORS['squirrel']
    mask = create_base_mask("Squirrel_Mask", color)
    add_eye_holes(mask)
    add_nose_hole(mask)
    add_strap_slots(mask)
    
    # Большие уши с кисточками
    add_ears(mask, ear_type='pointed', size=0.03, position=(0.04, 0.085, 0.015), rotation=(5, 0, 15))
    
    # Кисточки на ушах
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.005,
            radius2=0.001,
            depth=0.02,
            location=(side * 0.04, 0.1, 0.02)
        )
        tuft = bpy.context.active_object
        tuft.data.materials.append(mask.data.materials[0])
    
    # Маленький нос
    add_nose(mask, nose_type='button', size=0.01, position=(0, 0.01, 0.04), color=(0.2, 0.15, 0.1, 1.0))
    
    # Пушистые щёчки
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=(side * 0.04, 0.0, 0.025))
        cheek = bpy.context.active_object
        cheek.scale = (0.9, 0.7, 0.5)
        white_mat = create_material("White_cheek", (0.95, 0.93, 0.9, 1.0))
        cheek.data.materials.append(white_mat)
    
    # Большие глаза
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.01,
            location=(side * 0.03, 0.035, 0.045)
        )
        eye_shine = bpy.context.active_object
        eye_mat = create_material("Eye_shine", (0.1, 0.08, 0.05, 1.0))
        eye_shine.data.materials.append(eye_mat)
    
    return mask


# ============================================================================
# МЕНЮ И ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

MASK_FUNCTIONS = {
    '1': ('Волк / Wolf', create_wolf_mask),
    '2': ('Лис / Fox', create_fox_mask),
    '3': ('Заяц / Rabbit', create_rabbit_mask),
    '4': ('Медведь / Bear', create_bear_mask),
    '5': ('Рысь / Lynx', create_lynx_mask),
    '6': ('Баба-яга / Baba Yaga', create_baba_yaga_mask),
    '7': ('Кощей / Koschei', create_koschei_mask),
    '8': ('Снегурочка / Snegurochka', create_snegurochka_mask),
    '9': ('Дед Мороз / Ded Moroz', create_ded_moroz_mask),
    '10': ('Леший / Leshy', create_leshy_mask),
    '11': ('Водяной / Vodyanoy', create_vodyanoy_mask),
    '12': ('Лягушка / Frog', create_frog_mask),
    '13': ('Ворон / Raven', create_raven_mask),
    '14': ('Ворона / Crow', create_crow_mask),
    '15': ('Белка / Squirrel', create_squirrel_mask),
}


def create_all_masks():
    """Создаёт все маски в ряд"""
    clear_scene()
    
    spacing = 0.22  # Расстояние между масками
    total = len(MASK_FUNCTIONS)
    start_x = -(total - 1) * spacing / 2
    
    for i, (key, (name, func)) in enumerate(MASK_FUNCTIONS.items()):
        mask = func()
        mask.location.x = start_x + i * spacing
        print(f"Created: {name}")
    
    setup_scene()
    print(f"\n✓ Created {total} masks!")


def create_selected_mask(mask_key):
    """Создаёт выбранную маску"""
    clear_scene()
    
    if mask_key in MASK_FUNCTIONS:
        name, func = MASK_FUNCTIONS[mask_key]
        mask = func()
        setup_scene()
        print(f"\n✓ Created: {name}")
    else:
        print(f"Invalid selection: {mask_key}")


def setup_scene():
    """Настраивает сцену"""
    # Свет
    bpy.ops.object.light_add(type='SUN', location=(2, -3, 4))
    key = bpy.context.active_object
    key.data.energy = 2.5
    
    bpy.ops.object.light_add(type='SUN', location=(-2, -2, 3))
    fill = bpy.context.active_object
    fill.data.energy = 1.5
    
    bpy.ops.object.light_add(type='SUN', location=(0, 3, 2))
    back = bpy.context.active_object
    back.data.energy = 1.0
    
    # Камера
    bpy.ops.object.camera_add(location=(0, -0.5, 0.15))
    cam = bpy.context.active_object
    direction = Vector((0, 0, 0)) - Vector(cam.location)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    
    # Render
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 64


def main():
    """Главная функция"""
    print("\n" + "="*60)
    print("  МАСКИ ДЛЯ ДЕТСКИХ ПРАЗДНИКОВ / PARTY MASKS")
    print("="*60)
    print("\nВыберите маску для создания:")
    for key, (name, _) in MASK_FUNCTIONS.items():
        print(f"  {key}. {name}")
    print("  A. Создать ВСЕ маски")
    print("="*60)
    
    # По умолчанию создаём все маски
    # Для выбора конкретной маски измените строку ниже:
    # create_selected_mask('1')  # для одной маски
    create_all_masks()  # для всех масок


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    main()
