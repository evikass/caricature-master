"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     КАРКАСЫ ДЛЯ КУКОЛЬНОЙ АНИМАЦИИ - Blender Python Script                   ║
║     Puppet Armatures for Stop-Motion Animation                               ║
║                                                                              ║
║     Совместимость: Blender 3.x / 4.x / 5.x                                   ║
║     Для печати на SLA 3D-принтере                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Инструкция по использованию:
1. Открой Blender
2. Перейди: Scripting (в верхнем меню)
3. Создай новый текстовый блок (Ctrl+N или кнопка "New")
4. Скопируй этот скрипт
5. Нажми "Run Script" (Alt+P или кнопка Play)
6. Модели появятся в сцене

Автор: AI Assistant
Версия: 2.0 (исправленная для Blender 5.x)
"""

import bpy
import bmesh
import math
from mathutils import Vector, Matrix
import os

# ============================================================================
# ГЛОБАЛЬНЫЕ НАСТРОЙКИ
# ============================================================================

class ArmatureSettings:
    """Глобальные настройки для всех каркасов"""
    
    # Масштаб куклы (в метрах)
    DOLL_SCALE = 0.15  # 15 см - стандартная кукла
    
    # Параметры для SLA печати
    MIN_WALL_THICKNESS = 0.001  # 1 мм в метрах
    JOINT_TOLERANCE = 0.0002    # 0.2 мм зазор
    
    # Размеры шариков для шарниров
    BALL_SMALL = 0.004   # 4 мм - пальцы
    BALL_MEDIUM = 0.006  # 6 мм - локти, колени
    BALL_LARGE = 0.008   # 8 мм - таз, плечи
    
    # Проволока
    WIRE_DIAMETER = 0.002  # 2 мм
    
    # Материалы
    JOINT_COLOR = (0.8, 0.2, 0.1, 1.0)  # Красный для шарниров
    BONE_COLOR = (0.3, 0.3, 0.4, 1.0)    # Серый для "костей"
    WIRE_COLOR = (0.2, 0.2, 0.3, 1.0)    # Тёмно-серый для проволоки


def clear_scene():
    """Очищает сцену перед созданием новых объектов"""
    # Удаляем все объекты
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    
    # Удаляем все материалы
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)


def create_material(name, color):
    """Создаёт материал с заданным цветом"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = 0.8
    bsdf.inputs['Roughness'].default_value = 0.3
    return mat


def create_sphere(location, radius, name, material=None):
    """Создаёт сферу в указанной позиции"""
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    
    if material:
        obj.data.materials.append(material)
    
    return obj


def create_cylinder(start, end, radius, name, material=None):
    """Создаёт цилиндр между двумя точками"""
    direction = Vector(end) - Vector(start)
    length = direction.length
    
    if length < 0.0001:
        length = 0.001  # Минимальная длина
    
    # Создаём цилиндр
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=length,
        location=((Vector(start) + Vector(end)) / 2)
    )
    obj = bpy.context.active_object
    obj.name = name
    
    # Поворачиваем к конечной точке
    direction.normalize()
    up = Vector((0, 0, 1))
    
    # Проверяем, что direction не равен up или -up
    dot = up.dot(direction)
    if abs(dot) < 0.9999:
        angle = math.acos(max(-1, min(1, dot)))
        axis = up.cross(direction).normalized()
        if axis.length > 0:
            obj.rotation_mode = 'AXIS_ANGLE'
            obj.rotation_axis_angle = (angle, axis.x, axis.y, axis.z)
    elif dot < 0:
        # direction = -up, поворот на 180 градусов вокруг X
        obj.rotation_euler = (math.pi, 0, 0)
    
    if material:
        obj.data.materials.append(material)
    
    return obj


def create_torus(location, major_radius, minor_radius, name, material=None):
    """Создаёт тор (кольцо)"""
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major_radius,
        minor_radius=minor_radius,
        location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    
    if material:
        obj.data.materials.append(material)
    
    return obj


# ============================================================================
# ТИП 1: БАЗОВЫЙ ПРОВОЛОЧНЫЙ КАРКАС
# ============================================================================

def create_wire_armature(scale=None):
    """
    Создаёт базовый проволочный каркас для куклы
    
    Простой каркас из проволоки для начинающих аниматоров.
    Проволока проходит через всё тело, образуя единую конструкцию.
    
    Параметры:
        scale: масштаб куклы (по умолчанию 15 см)
    """
    if scale is None:
        scale = ArmatureSettings.DOLL_SCALE
    
    wire_r = ArmatureSettings.WIRE_DIAMETER / 2
    mat = create_material("WireMaterial", ArmatureSettings.WIRE_COLOR)
    
    objects = []
    
    # Пропорции тела (относительные)
    head_h = scale * 0.25
    neck_h = scale * 0.05
    torso_h = scale * 0.3
    pelvis_h = scale * 0.08
    arm_len = scale * 0.35
    leg_len = scale * 0.45
    
    # === Позвоночник ===
    spine_bottom = (0, 0, leg_len)
    spine_top = (0, 0, leg_len + pelvis_h + torso_h + neck_h + head_h)
    spine = create_cylinder(spine_bottom, spine_top, wire_r, "Spine", mat)
    objects.append(spine)
    
    # === Тазовая кость (перекладина) ===
    pelvis_y = leg_len + pelvis_h * 0.5
    hip_width = scale * 0.15
    pelvis = create_cylinder(
        (-hip_width, 0, pelvis_y),
        (hip_width, 0, pelvis_y),
        wire_r * 1.2, "Pelvis", mat
    )
    objects.append(pelvis)
    
    # === Плечевая кость ===
    shoulder_y = leg_len + pelvis_h + torso_h
    shoulder_width = scale * 0.2
    shoulder = create_cylinder(
        (-shoulder_width, 0, shoulder_y),
        (shoulder_width, 0, shoulder_y),
        wire_r * 1.2, "Shoulder", mat
    )
    objects.append(shoulder)
    
    # === Левая рука ===
    l_arm_1 = create_cylinder(
        (-shoulder_width, 0, shoulder_y),
        (-shoulder_width - scale * 0.08, 0, shoulder_y - arm_len * 0.3),
        wire_r, "L_UpperArm", mat
    )
    objects.append(l_arm_1)
    
    l_arm_2 = create_cylinder(
        (-shoulder_width - scale * 0.08, 0, shoulder_y - arm_len * 0.3),
        (-shoulder_width - scale * 0.12, 0, shoulder_y - arm_len),
        wire_r, "L_Forearm", mat
    )
    objects.append(l_arm_2)
    
    # === Правая рука ===
    r_arm_1 = create_cylinder(
        (shoulder_width, 0, shoulder_y),
        (shoulder_width + scale * 0.08, 0, shoulder_y - arm_len * 0.3),
        wire_r, "R_UpperArm", mat
    )
    objects.append(r_arm_1)
    
    r_arm_2 = create_cylinder(
        (shoulder_width + scale * 0.08, 0, shoulder_y - arm_len * 0.3),
        (shoulder_width + scale * 0.12, 0, shoulder_y - arm_len),
        wire_r, "R_Forearm", mat
    )
    objects.append(r_arm_2)
    
    # === Левая нога ===
    l_leg_1 = create_cylinder(
        (-hip_width * 0.6, 0, pelvis_y),
        (-hip_width * 0.6, 0, leg_len * 0.5),
        wire_r * 1.1, "L_Thigh", mat
    )
    objects.append(l_leg_1)
    
    l_leg_2 = create_cylinder(
        (-hip_width * 0.6, 0, leg_len * 0.5),
        (-hip_width * 0.6, 0, 0),
        wire_r * 1.1, "L_Shin", mat
    )
    objects.append(l_leg_2)
    
    # === Правая нога ===
    r_leg_1 = create_cylinder(
        (hip_width * 0.6, 0, pelvis_y),
        (hip_width * 0.6, 0, leg_len * 0.5),
        wire_r * 1.1, "R_Thigh", mat
    )
    objects.append(r_leg_1)
    
    r_leg_2 = create_cylinder(
        (hip_width * 0.6, 0, leg_len * 0.5),
        (hip_width * 0.6, 0, 0),
        wire_r * 1.1, "R_Shin", mat
    )
    objects.append(r_leg_2)
    
    # === Голова (петля) ===
    head_r = scale * 0.08
    head_torus = create_torus(
        (0, 0, leg_len + pelvis_h + torso_h + neck_h + head_h * 0.4),
        head_r,
        wire_r,
        "Head_Loop", mat
    )
    objects.append(head_torus)
    
    # Объединяем все объекты
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    
    result = bpy.context.active_object
    result.name = "Wire_Armature_15cm"
    
    return result


# ============================================================================
# ТИП 2: BALL-AND-SOCKET КАРКАС (ПРОФЕССИОНАЛЬНЫЙ)
# ============================================================================

def create_ball_socket_armature(scale=None):
    """
    Создаёт профессиональный каркас с шарнирными соединениями
    
    Ball-and-socket joints обеспечивают плавное движение во всех
    направлениях и надёжную фиксацию позы.
    
    Параметры:
        scale: масштаб куклы (по умолчанию 15 см)
    
    Возвращает:
        Список всех созданных объектов
    """
    if scale is None:
        scale = ArmatureSettings.DOLL_SCALE
    
    mat_joint = create_material("JointMaterial", ArmatureSettings.JOINT_COLOR)
    mat_bone = create_material("BoneMaterial", ArmatureSettings.BONE_COLOR)
    
    objects = []
    
    # Размеры
    ball_small = ArmatureSettings.BALL_SMALL
    ball_medium = ArmatureSettings.BALL_MEDIUM
    ball_large = ArmatureSettings.BALL_LARGE
    
    # Пропорции тела
    head_h = scale * 0.25
    torso_h = scale * 0.3
    pelvis_h = scale * 0.08
    arm_len = scale * 0.35
    leg_len = scale * 0.45
    
    base_z = leg_len
    
    # === ТАЗОВЫЙ ПОЯС ===
    pelvis_z = base_z + pelvis_h * 0.5
    hip_width = scale * 0.15
    
    # Центральный блок таза
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, pelvis_z))
    pelvis_block = bpy.context.active_object
    pelvis_block.scale = (hip_width * 2, scale * 0.04, pelvis_h)
    pelvis_block.name = "Pelvis_Block"
    pelvis_block.data.materials.append(mat_joint)
    objects.append(pelvis_block)
    
    # Шаровые шарниры для бёдер
    l_hip_ball = create_sphere((-hip_width * 0.8, 0, pelvis_z), ball_medium, "L_Hip_Ball", mat_joint)
    r_hip_ball = create_sphere((hip_width * 0.8, 0, pelvis_z), ball_medium, "R_Hip_Ball", mat_joint)
    objects.extend([l_hip_ball, r_hip_ball])
    
    # === ПОЗВОНОЧНИК ===
    spine_bottom = (0, 0, pelvis_z + pelvis_h * 0.4)
    spine_top = (0, 0, base_z + pelvis_h + torso_h * 0.5)
    
    # Позвонки как цилиндры
    for i in range(5):
        z1 = spine_bottom[2] + (spine_top[2] - spine_bottom[2]) * i / 5
        z2 = spine_bottom[2] + (spine_top[2] - spine_bottom[2]) * (i + 1) / 5
        vertebra = create_cylinder((0, 0, z1), (0, 0, z2), ball_small * 0.8, f"Vertebra_{i+1}", mat_bone)
        objects.append(vertebra)
    
    # === ГРУДНАЯ КЛЕТКА ===
    chest_z = base_z + pelvis_h + torso_h * 0.6
    chest_width = scale * 0.12
    
    # Грудной блок
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, chest_z))
    chest_block = bpy.context.active_object
    chest_block.scale = (chest_width * 2, scale * 0.05, torso_h * 0.4)
    chest_block.name = "Chest_Block"
    chest_block.data.materials.append(mat_joint)
    objects.append(chest_block)
    
    # === ПЛЕЧЕВОЙ ПОЯС ===
    shoulder_z = base_z + pelvis_h + torso_h
    shoulder_width = scale * 0.18
    
    # Ключицы
    l_clavicle = create_cylinder((-shoulder_width * 0.5, scale * 0.02, shoulder_z),
                                  (0, 0, shoulder_z), ball_small * 0.6, "L_Clavicle", mat_bone)
    r_clavicle = create_cylinder((shoulder_width * 0.5, scale * 0.02, shoulder_z),
                                  (0, 0, shoulder_z), ball_small * 0.6, "R_Clavicle", mat_bone)
    objects.extend([l_clavicle, r_clavicle])
    
    # Шаровые шарниры для плеч
    l_shoulder_ball = create_sphere((-shoulder_width, 0, shoulder_z), ball_medium, "L_Shoulder_Ball", mat_joint)
    r_shoulder_ball = create_sphere((shoulder_width, 0, shoulder_z), ball_medium, "R_Shoulder_Ball", mat_joint)
    objects.extend([l_shoulder_ball, r_shoulder_ball])
    
    # === РУКИ ===
    # Левая рука
    l_upper_arm = create_cylinder(
        (-shoulder_width, 0, shoulder_z),
        (-shoulder_width - scale * 0.1, 0, shoulder_z - arm_len * 0.45),
        ball_small * 0.5, "L_UpperArm", mat_bone
    )
    objects.append(l_upper_arm)
    
    l_elbow_z = shoulder_z - arm_len * 0.45
    l_elbow_ball = create_sphere((-shoulder_width - scale * 0.1, 0, l_elbow_z), ball_small, "L_Elbow_Ball", mat_joint)
    objects.append(l_elbow_ball)
    
    l_forearm = create_cylinder(
        (-shoulder_width - scale * 0.1, 0, l_elbow_z),
        (-shoulder_width - scale * 0.15, 0, shoulder_z - arm_len),
        ball_small * 0.4, "L_Forearm", mat_bone
    )
    objects.append(l_forearm)
    
    l_wrist_ball = create_sphere((-shoulder_width - scale * 0.15, 0, shoulder_z - arm_len), ball_small, "L_Wrist_Ball", mat_joint)
    objects.append(l_wrist_ball)
    
    # Правая рука
    r_upper_arm = create_cylinder(
        (shoulder_width, 0, shoulder_z),
        (shoulder_width + scale * 0.1, 0, shoulder_z - arm_len * 0.45),
        ball_small * 0.5, "R_UpperArm", mat_bone
    )
    objects.append(r_upper_arm)
    
    r_elbow_z = shoulder_z - arm_len * 0.45
    r_elbow_ball = create_sphere((shoulder_width + scale * 0.1, 0, r_elbow_z), ball_small, "R_Elbow_Ball", mat_joint)
    objects.append(r_elbow_ball)
    
    r_forearm = create_cylinder(
        (shoulder_width + scale * 0.1, 0, r_elbow_z),
        (shoulder_width + scale * 0.15, 0, shoulder_z - arm_len),
        ball_small * 0.4, "R_Forearm", mat_bone
    )
    objects.append(r_forearm)
    
    r_wrist_ball = create_sphere((shoulder_width + scale * 0.15, 0, shoulder_z - arm_len), ball_small, "R_Wrist_Ball", mat_joint)
    objects.append(r_wrist_ball)
    
    # === НОГИ ===
    # Левая нога
    l_thigh = create_cylinder(
        (-hip_width * 0.6, 0, pelvis_z),
        (-hip_width * 0.6, 0, leg_len * 0.5),
        ball_medium * 0.5, "L_Thigh", mat_bone
    )
    objects.append(l_thigh)
    
    l_knee_z = leg_len * 0.5
    l_knee_ball = create_sphere((-hip_width * 0.6, 0, l_knee_z), ball_medium, "L_Knee_Ball", mat_joint)
    objects.append(l_knee_ball)
    
    l_shin = create_cylinder(
        (-hip_width * 0.6, 0, l_knee_z),
        (-hip_width * 0.6, 0, 0),
        ball_medium * 0.4, "L_Shin", mat_bone
    )
    objects.append(l_shin)
    
    l_ankle_ball = create_sphere((-hip_width * 0.6, 0, 0.01), ball_small, "L_Ankle_Ball", mat_joint)
    objects.append(l_ankle_ball)
    
    # Правая нога
    r_thigh = create_cylinder(
        (hip_width * 0.6, 0, pelvis_z),
        (hip_width * 0.6, 0, leg_len * 0.5),
        ball_medium * 0.5, "R_Thigh", mat_bone
    )
    objects.append(r_thigh)
    
    r_knee_z = leg_len * 0.5
    r_knee_ball = create_sphere((hip_width * 0.6, 0, r_knee_z), ball_medium, "R_Knee_Ball", mat_joint)
    objects.append(r_knee_ball)
    
    r_shin = create_cylinder(
        (hip_width * 0.6, 0, r_knee_z),
        (hip_width * 0.6, 0, 0),
        ball_medium * 0.4, "R_Shin", mat_bone
    )
    objects.append(r_shin)
    
    r_ankle_ball = create_sphere((hip_width * 0.6, 0, 0.01), ball_small, "R_Ankle_Ball", mat_joint)
    objects.append(r_ankle_ball)
    
    # === ШЕЯ И ГОЛОВА ===
    neck_z = shoulder_z + scale * 0.03
    neck_ball = create_sphere((0, 0, neck_z), ball_medium, "Neck_Ball", mat_joint)
    objects.append(neck_ball)
    
    head_z = neck_z + head_h * 0.3
    
    # Череп (каркас для головы)
    head_r = scale * 0.07
    bpy.ops.mesh.primitive_uv_sphere_add(radius=head_r, location=(0, scale * 0.01, head_z))
    head_sphere = bpy.context.active_object
    head_sphere.name = "Head_Sphere"
    head_sphere.data.materials.append(mat_bone)
    objects.append(head_sphere)
    
    return objects


# ============================================================================
# ТИП 3: МОДУЛЬНЫЙ КАРКАС
# ============================================================================

def create_modular_armature(scale=None):
    """
    Создаёт модульный каркас из отдельных компонентов
    
    Каждый сустав печатается отдельно, затем собирается
    с помощью винтов и гаек.
    
    Возвращает:
        Список всех созданных объектов
    """
    if scale is None:
        scale = ArmatureSettings.DOLL_SCALE
    
    mat_joint = create_material("ModuleJoint", ArmatureSettings.JOINT_COLOR)
    mat_bone = create_material("ModuleBone", ArmatureSettings.BONE_COLOR)
    
    objects = []
    
    # === МОДУЛЬ ТАЗА ===
    pelvis_module = create_pelvis_module(scale, mat_joint)
    objects.extend(pelvis_module)  # ИСПРАВЛЕНО: extend вместо append
    
    # === МОДУЛИ НОГ ===
    l_leg_modules = create_leg_modules(scale, mat_joint, mat_bone, side="L", x_offset=-scale*0.1)
    r_leg_modules = create_leg_modules(scale, mat_joint, mat_bone, side="R", x_offset=scale*0.1)
    objects.extend(l_leg_modules)
    objects.extend(r_leg_modules)
    
    # === МОДУЛЬ ГРУДИ ===
    chest_module = create_chest_module(scale, mat_joint)
    objects.extend(chest_module)  # ИСПРАВЛЕНО: extend вместо append
    
    # === МОДУЛИ РУК ===
    l_arm_modules = create_arm_modules(scale, mat_joint, mat_bone, side="L", x_offset=-scale*0.2)
    r_arm_modules = create_arm_modules(scale, mat_joint, mat_bone, side="R", x_offset=scale*0.2)
    objects.extend(l_arm_modules)
    objects.extend(r_arm_modules)
    
    # === МОДУЛЬ ГОЛОВЫ ===
    head_module = create_head_module(scale, mat_joint, mat_bone)
    objects.extend(head_module)  # ИСПРАВЛЕНО: extend вместо append
    
    return objects


def create_pelvis_module(scale, material):
    """Создаёт модуль тазового пояса"""
    objects = []
    
    # Основание таза
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, scale * 0.5))
    pelvis = bpy.context.active_object
    pelvis.scale = (scale * 0.25, scale * 0.04, scale * 0.06)
    pelvis.name = "Pelvis_Module"
    pelvis.data.materials.append(material)
    objects.append(pelvis)
    
    # Крепления для ног (с отверстиями)
    for side in [-1, 1]:
        # Втулка для крепления ноги
        bpy.ops.mesh.primitive_cylinder_add(
            radius=scale * 0.015,
            depth=scale * 0.02,
            location=(side * scale * 0.1, 0, scale * 0.5)
        )
        hip_mount = bpy.context.active_object
        hip_mount.name = f"{'L' if side < 0 else 'R'}_Hip_Mount"
        hip_mount.data.materials.append(material)
        objects.append(hip_mount)
    
    # Крепление для позвоночника
    spine_mount = create_cylinder(
        (0, 0, scale * 0.53),
        (0, 0, scale * 0.58),
        scale * 0.012,
        "Spine_Mount",
        material
    )
    objects.append(spine_mount)
    
    return objects


def create_leg_modules(scale, mat_joint, mat_bone, side, x_offset):
    """Создаёт модули для одной ноги"""
    objects = []
    side_prefix = side
    
    z_base = scale * 0.45
    
    # Бедро
    thigh = create_cylinder(
        (x_offset, 0, z_base),
        (x_offset, 0, z_base - scale * 0.2),
        scale * 0.012,
        f"{side_prefix}_Thigh",
        mat_bone
    )
    objects.append(thigh)
    
    # Коленный модуль
    knee = create_sphere((x_offset, 0, z_base - scale * 0.2), scale * 0.015, f"{side_prefix}_Knee_Joint", mat_joint)
    objects.append(knee)
    
    # Голень
    shin = create_cylinder(
        (x_offset, 0, z_base - scale * 0.2),
        (x_offset, 0, scale * 0.02),
        scale * 0.01,
        f"{side_prefix}_Shin",
        mat_bone
    )
    objects.append(shin)
    
    # Голеностоп
    ankle = create_sphere((x_offset, 0, scale * 0.02), scale * 0.01, f"{side_prefix}_Ankle_Joint", mat_joint)
    objects.append(ankle)
    
    # Стопа (плоское основание)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x_offset, scale * 0.01, scale * 0.005))
    foot = bpy.context.active_object
    foot.scale = (scale * 0.04, scale * 0.06, scale * 0.008)
    foot.name = f"{side_prefix}_Foot"
    foot.data.materials.append(mat_bone)
    objects.append(foot)
    
    return objects


def create_chest_module(scale, material):
    """Создаёт модуль грудной клетки"""
    objects = []
    
    chest_z = scale * 0.65
    
    # Грудной блок
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, chest_z))
    chest = bpy.context.active_object
    chest.scale = (scale * 0.2, scale * 0.05, scale * 0.12)
    chest.name = "Chest_Module"
    chest.data.materials.append(material)
    objects.append(chest)
    
    # Плечевые крепления
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=scale * 0.012,
            depth=scale * 0.025,
            location=(side * scale * 0.12, 0, chest_z + scale * 0.02)
        )
        shoulder_mount = bpy.context.active_object
        shoulder_mount.name = f"{'L' if side < 0 else 'R'}_Shoulder_Mount"
        shoulder_mount.data.materials.append(material)
        objects.append(shoulder_mount)
    
    # Шейное крепление
    neck_mount = create_cylinder(
        (0, 0, chest_z + scale * 0.07),
        (0, 0, chest_z + scale * 0.1),
        scale * 0.01,
        "Neck_Mount",
        material
    )
    objects.append(neck_mount)
    
    return objects


def create_arm_modules(scale, mat_joint, mat_bone, side, x_offset):
    """Создаёт модули для одной руки"""
    objects = []
    side_prefix = side
    
    shoulder_z = scale * 0.68
    
    # Плечевой сустав
    shoulder = create_sphere((x_offset, 0, shoulder_z), scale * 0.012, f"{side_prefix}_Shoulder_Joint", mat_joint)
    objects.append(shoulder)
    
    # Плечо
    upper_arm = create_cylinder(
        (x_offset, 0, shoulder_z),
        (x_offset + scale * 0.02, 0, shoulder_z - scale * 0.12),
        scale * 0.008,
        f"{side_prefix}_UpperArm",
        mat_bone
    )
    objects.append(upper_arm)
    
    # Локоть
    elbow_z = shoulder_z - scale * 0.12
    elbow = create_sphere((x_offset + scale * 0.02, 0, elbow_z), scale * 0.01, f"{side_prefix}_Elbow_Joint", mat_joint)
    objects.append(elbow)
    
    # Предплечье
    forearm = create_cylinder(
        (x_offset + scale * 0.02, 0, elbow_z),
        (x_offset + scale * 0.04, 0, elbow_z - scale * 0.12),
        scale * 0.006,
        f"{side_prefix}_Forearm",
        mat_bone
    )
    objects.append(forearm)
    
    # Запястье
    wrist_z = elbow_z - scale * 0.12
    wrist = create_sphere((x_offset + scale * 0.04, 0, wrist_z), scale * 0.008, f"{side_prefix}_Wrist_Joint", mat_joint)
    objects.append(wrist)
    
    # Кисть
    hand_x = x_offset + scale * 0.04
    for i in range(4):
        finger = create_cylinder(
            (hand_x - scale * 0.01 + i * scale * 0.006, 0, wrist_z),
            (hand_x - scale * 0.015 + i * scale * 0.007, 0, wrist_z - scale * 0.025),
            scale * 0.002,
            f"{side_prefix}_Finger_{i+1}",
            mat_bone
        )
        objects.append(finger)
    
    return objects


def create_head_module(scale, mat_joint, mat_bone):
    """Создаёт модуль головы"""
    objects = []
    
    head_z = scale * 0.85
    
    # Шейный стержень
    neck_rod = create_cylinder(
        (0, 0, scale * 0.75),
        (0, 0, head_z - scale * 0.04),
        scale * 0.008,
        "Neck_Rod",
        mat_bone
    )
    objects.append(neck_rod)
    
    # Основание черепа
    skull_base = create_sphere((0, scale * 0.01, head_z), scale * 0.015, "Skull_Base", mat_joint)
    objects.append(skull_base)
    
    # Черепной купол
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=scale * 0.055,
        location=(0, scale * 0.01, head_z + scale * 0.02)
    )
    skull = bpy.context.active_object
    skull.name = "Skull_Dome"
    skull.data.materials.append(mat_bone)
    objects.append(skull)
    
    # Крепления для челюсти
    jaw_mount_l = create_sphere((-scale * 0.02, scale * 0.02, head_z - scale * 0.01), scale * 0.006, "Jaw_Mount_L", mat_joint)
    jaw_mount_r = create_sphere((scale * 0.02, scale * 0.02, head_z - scale * 0.01), scale * 0.006, "Jaw_Mount_R", mat_joint)
    objects.extend([jaw_mount_l, jaw_mount_r])
    
    return objects


# ============================================================================
# ТИП 4: КАРКАС ДЛЯ ПАЛЬЦЕВОЙ АНИМАЦИИ
# ============================================================================

def create_hand_armature(scale=None):
    """
    Создаёт детальный каркас кисти для анимации пальцев
    
    Включает все суставы каждого пальца с возможностью
    независимого движения.
    
    Возвращает:
        Список всех созданных объектов
    """
    if scale is None:
        scale = ArmatureSettings.DOLL_SCALE * 0.4  # Размер кисти
    
    mat_joint = create_material("FingerJoint", ArmatureSettings.JOINT_COLOR)
    mat_bone = create_material("FingerBone", ArmatureSettings.BONE_COLOR)
    
    objects = []
    
    # Ладонь
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    palm = bpy.context.active_object
    palm.scale = (scale * 0.5, scale * 0.15, scale * 0.25)
    palm.name = "Palm"
    palm.data.materials.append(mat_bone)
    objects.append(palm)
    
    # Пальцы
    finger_data = [
        ("Thumb", -0.22, 0.03, 0.7, 4),
        ("Index", -0.12, 0.0, 1.0, 3),
        ("Middle", 0.0, 0.0, 1.1, 3),
        ("Ring", 0.12, 0.0, 1.0, 3),
        ("Pinky", 0.22, 0.0, 0.8, 3),
    ]
    
    for finger_name, x_offset, y_offset, length_mult, joints_count in finger_data:
        finger_objects = create_finger(
            scale,
            finger_name,
            x_offset * scale,
            y_offset * scale,
            length_mult,
            joints_count,
            mat_joint,
            mat_bone
        )
        objects.extend(finger_objects)
    
    return objects


def create_finger(scale, name, x_offset, y_offset, length_mult, joints_count, mat_joint, mat_bone):
    """Создаёт один палец с суставами"""
    objects = []
    
    base_z = scale * 0.25
    segment_length = scale * 0.15 * length_mult
    
    for i in range(joints_count):
        # Сустав
        joint_z = base_z + i * segment_length
        joint = create_sphere(
            (x_offset, y_offset, joint_z),
            scale * 0.02,
            f"{name}_Joint_{i+1}",
            mat_joint
        )
        objects.append(joint)
        
        # Сегмент кости
        if i < joints_count - 1:
            bone = create_cylinder(
                (x_offset, y_offset, joint_z),
                (x_offset, y_offset, joint_z + segment_length * 0.9),
                scale * 0.012,
                f"{name}_Bone_{i+1}",
                mat_bone
            )
            objects.append(bone)
    
    # Кончик пальца
    tip_z = base_z + joints_count * segment_length - segment_length * 0.1
    tip = create_sphere(
        (x_offset, y_offset, tip_z),
        scale * 0.015,
        f"{name}_Tip",
        mat_joint
    )
    objects.append(tip)
    
    return objects


# ============================================================================
# ТИП 5: УНИВЕРСАЛЬНЫЕ ШАРНИРЫ (ОТДЕЛЬНЫЕ КОМПОНЕНТЫ)
# ============================================================================

def create_universal_joints():
    """
    Создаёт набор универсальных шарниров для кастомных каркасов
    
    Включает шарики и сокеты разных размеров, которые можно
    использовать для сборки собственного каркаса.
    
    Возвращает:
        Список всех созданных объектов
    """
    objects = []
    mat = create_material("UniversalJoint", ArmatureSettings.JOINT_COLOR)
    
    sizes = [
        ("Small", 0.004),
        ("Medium", 0.006),
        ("Large", 0.008),
    ]
    
    spacing = 0.05
    
    for i, (size_name, radius) in enumerate(sizes):
        x_pos = i * spacing
        
        # Шарик
        ball = create_sphere((x_pos, 0, 0), radius, f"Ball_{size_name}", mat)
        objects.append(ball)
        
        # Сокет (втулка) - полусфера
        socket_inner = radius + ArmatureSettings.JOINT_TOLERANCE
        socket_outer = socket_inner + 0.002
        
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=socket_outer,
            location=(x_pos, spacing, 0)
        )
        socket = bpy.context.active_object
        socket.name = f"Socket_{size_name}"
        socket.data.materials.append(mat)
        objects.append(socket)
        
        # Версия сокета с вырезом (для литья)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=socket_outer,
            depth=socket_outer * 1.5,
            location=(x_pos, spacing * 2, 0)
        )
        socket_open = bpy.context.active_object
        socket_open.name = f"Socket_Open_{size_name}"
        socket_open.data.materials.append(mat)
        objects.append(socket_open)
    
    # Шарнир "петля" (hinge)
    hinge_y = spacing * 3
    for i, (size_name, _) in enumerate(sizes):
        x_pos = i * spacing
        
        # Верхняя часть петли
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, hinge_y, 0.005))
        hinge_top = bpy.context.active_object
        hinge_top.scale = (0.01, 0.003, 0.01)
        hinge_top.name = f"Hinge_Top_{size_name}"
        hinge_top.data.materials.append(mat)
        objects.append(hinge_top)
        
        # Нижняя часть петли
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_pos, hinge_y + 0.01, 0.005))
        hinge_bottom = bpy.context.active_object
        hinge_bottom.scale = (0.01, 0.003, 0.01)
        hinge_bottom.name = f"Hinge_Bottom_{size_name}"
        hinge_bottom.data.materials.append(mat)
        objects.append(hinge_bottom)
        
        # Штифт
        pin = create_cylinder(
            (x_pos, hinge_y + 0.005, 0),
            (x_pos, hinge_y + 0.005, 0.012),
            0.002,
            f"Hinge_Pin_{size_name}",
            mat
        )
        objects.append(pin)
    
    return objects


# ============================================================================
# ФУНКЦИЯ СОЗДАНИЯ ВСЕХ КАРКАСОВ
# ============================================================================

def create_all_armatures():
    """
    Создаёт все типы каркасов в одной сцене,
    размещая их на расстоянии друг от друга
    """
    clear_scene()
    
    spacing = 0.4  # Расстояние между каркасами
    
    # 1. Базовый проволочный каркас
    wire_armature = create_wire_armature()
    wire_armature.location.x = -spacing * 2
    wire_armature.name = "01_Wire_Armature_Basic"
    
    # 2. Ball-and-Socket каркас
    ball_socket_objects = create_ball_socket_armature()
    for obj in ball_socket_objects:
        obj.location.x = 0
    
    # Объединяем в один объект
    if ball_socket_objects:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in ball_socket_objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = ball_socket_objects[0]
        bpy.ops.object.join()
        ball_socket = bpy.context.active_object
        ball_socket.name = "02_BallSocket_Armature_Pro"
    
    # 3. Модульный каркас
    modular_objects = create_modular_armature()
    for obj in modular_objects:
        obj.location.x = spacing
    
    # Объединяем
    if modular_objects:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in modular_objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = modular_objects[0]
        bpy.ops.object.join()
        modular = bpy.context.active_object
        modular.name = "03_Modular_Armature"
    
    # 4. Каркас кисти
    hand_objects = create_hand_armature()
    for obj in hand_objects:
        obj.location.x = spacing * 2
    
    if hand_objects:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in hand_objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = hand_objects[0]
        bpy.ops.object.join()
        hand = bpy.context.active_object
        hand.name = "04_Hand_Armature_Detailed"
    
    # 5. Универсальные шарниры
    joint_objects = create_universal_joints()
    for obj in joint_objects:
        obj.location.x = spacing * 3.5
    
    # Объединяем
    if joint_objects:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in joint_objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = joint_objects[0]
        bpy.ops.object.join()
        joints = bpy.context.active_object
        joints.name = "05_Universal_Joints_Set"
    
    # Добавляем камеру и свет
    setup_scene()
    
    print("\n" + "="*60)
    print("All armatures created successfully!")
    print("="*60)
    print("\nCreated models:")
    print("  1. Wire_Armature_Basic      - Wire armature")
    print("  2. BallSocket_Armature_Pro  - Professional ball-and-socket")
    print("  3. Modular_Armature         - Modular system")
    print("  4. Hand_Armature_Detailed   - Detailed hand")
    print("  5. Universal_Joints_Set     - Universal joints set")
    print("\nTo export STL: File -> Export -> Stl (.stl)")
    print("="*60)


def setup_scene():
    """Настраивает сцену с освещением и камерой"""
    
    # Удаляем существующий свет
    if "Light" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)
    
    # Добавляем три источника света
    # Ключевой свет
    bpy.ops.object.light_add(type='SUN', location=(2, -2, 3))
    key_light = bpy.context.active_object
    key_light.name = "KeyLight"
    key_light.data.energy = 3
    
    # Заполняющий свет
    bpy.ops.object.light_add(type='SUN', location=(-2, -1, 2))
    fill_light = bpy.context.active_object
    fill_light.name = "FillLight"
    fill_light.data.energy = 1.5
    
    # Контровой свет
    bpy.ops.object.light_add(type='SUN', location=(0, 3, 1))
    back_light = bpy.context.active_object
    back_light.name = "BackLight"
    back_light.data.energy = 1
    
    # Добавляем камеру
    bpy.ops.object.camera_add(location=(0.5, -1.2, 0.5))
    camera = bpy.context.active_object
    camera.name = "MainCamera"
    
    # Направляем камеру на центр сцены
    direction = Vector((0, 0, 0.3)) - Vector(camera.location)
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    
    # Делаем камеру активной
    bpy.context.scene.camera = camera
    
    # Устанавливаем render engine для лучшего превью
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 64


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """Главная функция - запускает создание всех каркасов"""
    print("\n" + "="*60)
    print("  PUPPET ARMATURES FOR STOP-MOTION v2.0")
    print("  Compatible with Blender 3.x / 4.x / 5.x")
    print("="*60)
    
    create_all_armatures()


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    main()
