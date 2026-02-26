"""
Blender Python Script: Puppet Armature Generator for SLA 3D Printing
=====================================================================
Генератор каркасов для кукольной анимации с шарнирными соединениями.
Совместим с SLA 3D печатью.

Инструкция по использованию:
1. Откройте Blender
2. Перейдите в Scripting tab
3. Откройте этот файл (blender_puppet_armature.py)
4. Нажмите "Run Script" (Alt+P)
5. Настройте параметры в панели "Puppet Armature"

Автор: Super Z AI Assistant
Версия: 1.0
"""

import bpy
import bmesh
import math
from mathutils import Vector, Matrix, Euler
import os

# ============================================================================
# КОНФИГУРАЦИЯ И ПАРАМЕТРЫ
# ============================================================================

class PuppetArmatureSettings:
    """Настройки каркаса куклы"""
    
    # Общие параметры (в миллиметрах)
    scale_factor: float = 1.0  # Масштаб
    
    # Параметры шарнирных соединений
    ball_radius: float = 3.0  # Радиус шара
    socket_radius: float = 3.2  # Радиус гнезда (с зазором)
    socket_thickness: float = 1.5  # Толщина стенки гнезда
    socket_gap: float = 0.15  # Зазор для SLA печати (мм)
    
    # Параметры костей/стержней
    bone_diameter: float = 2.5  # Диаметр стержня
    bone_hole_diameter: float = 1.0  # Диаметр отверстия под проволоку
    
    # Параметры персонажа (пропорции)
    head_height: float = 25.0
    neck_height: float = 10.0
    torso_height: float = 40.0
    pelvis_height: float = 15.0
    shoulder_width: float = 35.0
    hip_width: float = 25.0
    
    # Конечности
    upper_arm_length: float = 30.0
    lower_arm_length: float = 25.0
    hand_length: float = 12.0
    
    upper_leg_length: float = 35.0
    lower_leg_length: float = 30.0
    foot_length: float = 15.0
    
    # Материалы
    use_materials: bool = True


# ============================================================================
# УТИЛИТЫ ДЛЯ СОЗДАНИЯ ГЕОМЕТРИИ
# ============================================================================

def create_material(name: str, color: tuple) -> bpy.types.Material:
    """Создание материала с указанным цветом"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.2
        bsdf.inputs["Roughness"].default_value = 0.3
    return mat


def create_uv_sphere(name: str, radius: float, location: tuple, segments: int = 32) -> bpy.types.Object:
    """Создание UV сферы"""
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        location=location,
        segments=segments,
        ring_count=segments // 2
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj


def create_cylinder(name: str, radius: float, height: float, location: tuple, rotation: tuple = (0, 0, 0)) -> bpy.types.Object:
    """Создание цилиндра"""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=height,
        location=location,
        rotation=rotation
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj


def create_cube(name: str, size: tuple, location: tuple) -> bpy.types.Object:
    """Создание куба"""
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def boolean_operation(obj_a: bpy.types.Object, obj_b: bpy.types.Object, operation: str = 'DIFFERENCE') -> bpy.types.Object:
    """Булева операция между объектами"""
    modifier = obj_a.modifiers.new(name="Boolean", type='BOOLEAN')
    modifier.object = obj_b
    modifier.operation = operation
    modifier.solver = 'FAST'
    
    # Применяем модификатор
    bpy.context.view_layer.objects.active = obj_a
    bpy.ops.object.modifier_apply(modifier="Boolean")
    
    # Удаляем вспомогательный объект
    bpy.data.objects.remove(obj_b, do_unlink=True)
    
    return obj_a


# ============================================================================
# ШАРНИРНЫЕ СОЕДИНЕНИЯ (BALL-AND-SOCKET JOINTS)
# ============================================================================

def create_ball_joint(name: str, radius: float, location: tuple, with_hole: bool = True, hole_diameter: float = 1.0) -> bpy.types.Object:
    """
    Создание шарового шарнира (ball joint)
    Используется для: плечи, бёдра, шея, запястья
    """
    # Создаём основной шар
    ball = create_uv_sphere(f"{name}_ball", radius, location)
    
    if with_hole:
        # Создаём отверстие для проволоки/стержня
        hole = create_cylinder(f"{name}_hole_temp", hole_diameter / 2, radius * 3, location)
        boolean_operation(ball, hole, 'DIFFERENCE')
    
    return ball


def create_socket_joint(name: str, ball_radius: float, socket_radius: float, 
                        location: tuple, socket_depth: float = None, 
                        with_stem: bool = True, stem_length: float = 10.0,
                        stem_diameter: float = 2.5) -> bpy.types.Object:
    """
    Создание гнезда для шарового шарнира (socket joint)
    """
    if socket_depth is None:
        socket_depth = ball_radius * 1.2
    
    # Создаём внешний корпус гнезда
    outer_radius = socket_radius + 1.5
    socket_outer = create_uv_sphere(f"{name}_socket_outer", outer_radius, location)
    
    # Создаём внутреннюю полость (вычитание)
    inner_location = (location[0], location[1], location[2])
    socket_inner = create_uv_sphere(f"{name}_socket_inner_temp", socket_radius, inner_location)
    
    # Создаём отверстие для входа шара (срезаем верхушку)
    cap_z = location[2] + socket_radius * 0.3
    cap_size = (outer_radius * 2, outer_radius * 2, outer_radius)
    cap_location = (location[0], location[1], location[2] + outer_radius + cap_z - outer_radius)
    cap = create_cube(f"{name}_cap_temp", cap_size, cap_location)
    
    # Вычитаем внутреннюю сферу
    boolean_operation(socket_outer, socket_inner, 'DIFFERENCE')
    
    # Вычитаем колпак для создания входного отверстия
    boolean_operation(socket_outer, cap, 'DIFFERENCE')
    
    if with_stem:
        # Добавляем стержень
        stem_z = location[2] - outer_radius - stem_length / 2
        stem = create_cylinder(f"{name}_stem", stem_diameter / 2, stem_length, 
                               (location[0], location[1], stem_z))
        
        # Объединяем гнездо и стержень
        bpy.ops.object.select_all(action='DESELECT')
        socket_outer.select_set(True)
        stem.select_set(True)
        bpy.context.view_layer.objects.active = socket_outer
        bpy.ops.object.join()
        socket_outer.name = f"{name}_socket"
    
    return socket_outer


def create_ball_socket_pair(name: str, ball_radius: float, gap: float, 
                            location: tuple, stem_length: float = 10.0,
                            stem_diameter: float = 2.5) -> tuple:
    """
    Создание пары шар-гнездо (ball and socket pair)
    Возвращает tuple: (ball_object, socket_object)
    """
    socket_radius = ball_radius + gap
    
    # Создаём шар
    ball = create_ball_joint(f"{name}", ball_radius, location)
    
    # Создаём гнездо смещённое по оси Z
    socket_location = (location[0], location[1], location[2] + ball_radius * 2 + stem_length)
    socket = create_socket_joint(f"{name}", ball_radius, socket_radius, 
                                 socket_location, stem_length=stem_length,
                                 stem_diameter=stem_diameter)
    
    return (ball, socket)


# ============================================================================
# ШАРНИРНЫЕ СОЕДИНЕНИЯ ТИПА "ПЕТЛЯ" (HINGE JOINTS)
# ============================================================================

def create_hinge_joint(name: str, radius: float, thickness: float, 
                       location: tuple, axis: str = 'X') -> bpy.types.Object:
    """
    Создание шарнирного соединения типа петли (hinge joint)
    Используется для: колени, локти, пальцы
    """
    # Создаём основную часть
    hinge_outer = create_cylinder(f"{name}_outer", radius, thickness, location)
    
    # Вращаем согласно оси
    if axis == 'X':
        hinge_outer.rotation_euler = (math.pi / 2, 0, 0)
    elif axis == 'Y':
        hinge_outer.rotation_euler = (0, math.pi / 2, 0)
    
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    # Создаём внутренний паз (для зацепа с парной деталью)
    inner_radius = radius * 0.6
    hinge_inner = create_cylinder(f"{name}_inner_temp", inner_radius, thickness * 1.1, location)
    
    if axis == 'X':
        hinge_inner.rotation_euler = (math.pi / 2, 0, 0)
    elif axis == 'Y':
        hinge_inner.rotation_euler = (0, math.pi / 2, 0)
    
    boolean_operation(hinge_outer, hinge_inner, 'DIFFERENCE')
    
    hinge_outer.name = f"{name}_hinge"
    return hinge_outer


def create_hinge_pair(name: str, radius: float, thickness: float, 
                      location: tuple, axis: str = 'X', gap: float = 0.15) -> tuple:
    """
    Создание пары шарнирных соединений (hinge pair)
    """
    # Первая часть (с пазом)
    part1 = create_hinge_joint(f"{name}_A", radius, thickness, location, axis)
    
    # Вторая часть (с выступом)
    offset = thickness + gap if axis != 'Y' else 0
    offset_y = thickness + gap if axis == 'Y' else 0
    
    part2_location = (location[0] + offset, location[1] + offset_y, location[2])
    part2 = create_hinge_joint(f"{name}_B", radius * 0.55, thickness, part2_location, axis)
    
    return (part1, part2)


# ============================================================================
# КОСТНЫЕ ЭЛЕМЕНТЫ (BONES/STRUTS)
# ============================================================================

def create_bone_segment(name: str, length: float, diameter: float, 
                        location: tuple, rotation: tuple = (0, 0, 0),
                        with_wire_hole: bool = True, hole_diameter: float = 1.0) -> bpy.types.Object:
    """
    Создание сегмента кости/стержня
    """
    # Создаём основной цилиндр
    bone = create_cylinder(name, diameter / 2, length, location, rotation)
    
    if with_wire_hole:
        # Добавляем продольное отверстие для проволоки
        hole_radius = hole_diameter / 2
        hole = create_cylinder(f"{name}_hole_temp", hole_radius, length * 1.1, location, rotation)
        boolean_operation(bone, hole, 'DIFFERENCE')
    
    # Добавляем фаски на концах
    # (можно добавить позже через bevel modifier)
    
    return bone


def create_bone_with_end_caps(name: str, length: float, diameter: float,
                               location: tuple, rotation: tuple = (0, 0, 0)) -> bpy.types.Object:
    """
    Создание кости с закруглёнными концами
    """
    bone = create_cylinder(name, diameter / 2, length, location, rotation)
    
    # Добавляем сферы на концах
    euler = Euler(rotation)
    direction = Vector((0, 0, 1)).rotate(euler) or Vector((0, 0, 1))
    
    end1_loc = (location[0], location[1], location[2] + length / 2)
    end2_loc = (location[0], location[1], location[2] - length / 2)
    
    end1 = create_uv_sphere(f"{name}_end1_temp", diameter / 2, end1_loc, segments=16)
    end2 = create_uv_sphere(f"{name}_end2_temp", diameter / 2, end2_loc, segments=16)
    
    # Объединяем
    bpy.ops.object.select_all(action='DESELECT')
    bone.select_set(True)
    end1.select_set(True)
    end2.select_set(True)
    bpy.context.view_layer.objects.active = bone
    bpy.ops.object.join()
    bone.name = name
    
    return bone


# ============================================================================
# СЛОЖНЫЕ УЗЛЫ
# ============================================================================

def create_shoulder_joint(name: str, ball_radius: float, gap: float,
                          location: tuple, arm_direction: tuple = (1, 0, 0)) -> bpy.types.Object:
    """
    Создание плечевого сустава (с мячом и гнездом в одном узле)
    """
    # Создаём гнездо
    socket = create_socket_joint(name, ball_radius, ball_radius + gap, location,
                                  with_stem=True, stem_length=8.0)
    
    # Создаём плечевую кость
    arm_length = 15.0
    arm_loc = (location[0] + arm_direction[0] * arm_length,
               location[1] + arm_direction[1] * arm_length,
               location[2] + arm_direction[2] * arm_length)
    
    arm_bone = create_bone_segment(f"{name}_humerus", arm_length, 2.5, arm_loc)
    
    # Объединяем
    bpy.ops.object.select_all(action='DESELECT')
    socket.select_set(True)
    arm_bone.select_set(True)
    bpy.context.view_layer.objects.active = socket
    bpy.ops.object.join()
    
    return socket


def create_hip_joint(name: str, ball_radius: float, gap: float,
                     location: tuple, leg_direction: tuple = (0, 0, -1)) -> bpy.types.Object:
    """
    Создание тазобедренного сустава
    """
    # Создаём шар
    ball = create_ball_joint(f"{name}_ball", ball_radius, location)
    
    # Создаём бедренную кость
    leg_length = 20.0
    leg_loc = (location[0] + leg_direction[0] * leg_length,
               location[1] + leg_direction[1] * leg_length,
               location[2] + leg_direction[2] * leg_length)
    
    leg_bone = create_bone_segment(f"{name}_femur", leg_length, 3.0, leg_loc)
    
    # Объединяем
    bpy.ops.object.select_all(action='DESELECT')
    ball.select_set(True)
    leg_bone.select_set(True)
    bpy.context.view_layer.objects.active = ball
    bpy.ops.object.join()
    ball.name = name
    
    return ball


def create_torso_section(name: str, width: float, height: float, depth: float,
                         location: tuple) -> bpy.types.Object:
    """
    Создание секции торса (грудной клетки или таза)
    """
    # Создаём основную рамку
    # Используем куб с вырезанным центром для лёгкости
    
    outer = create_cube(f"{name}_outer", (width, depth, height), location)
    
    inner_width = width - 4.0
    inner_depth = depth - 4.0
    inner_height = height - 2.0
    inner = create_cube(f"{name}_inner_temp", (inner_width, inner_depth, inner_height), location)
    
    boolean_operation(outer, inner, 'DIFFERENCE')
    outer.name = name
    
    return outer


def create_hand_armature(name: str, scale: float, location: tuple) -> bpy.types.Object:
    """
    Создание каркаса кисти руки
    """
    hand_objects = []
    
    # Ладонь
    palm = create_cube(f"{name}_palm", (scale * 8, scale * 3, scale * 1), location)
    hand_objects.append(palm)
    
    # Пальцы (5 пальцев)
    finger_positions = [
        ("thumb", (scale * 5, scale * 2, 0), scale * 4, 30),  # Большой
        ("index", (scale * 4, 0, scale * 3), scale * 5, 0),
        ("middle", (scale * 0, 0, scale * 5.5), scale * 6, 0),
        ("ring", (scale * -4, 0, scale * 5), scale * 5.5, 0),
        ("pinky", (scale * -7, 0, scale * 4), scale * 4, 0),
    ]
    
    for finger_name, offset, length, angle in finger_positions:
        finger_loc = (location[0] + offset[0], location[1] + offset[1], location[2] + offset[2])
        
        # Создаём сегменты пальца (3 фаланги)
        for seg in range(3):
            seg_length = length * (1 - seg * 0.25)
            seg_z = finger_loc[2] + seg * seg_length * 0.8
            
            segment = create_cylinder(
                f"{name}_{finger_name}_seg{seg}",
                scale * 0.8,
                seg_length * 0.7,
                (finger_loc[0], finger_loc[1], seg_z)
            )
            hand_objects.append(segment)
            
            # Добавляем сустав между сегментами
            if seg < 2:
                joint_ball = create_uv_sphere(
                    f"{name}_{finger_name}_joint{seg}",
                    scale * 0.9,
                    (finger_loc[0], finger_loc[1], seg_z + seg_length * 0.35)
                )
                hand_objects.append(joint_ball)
    
    # Объединяем все объекты
    bpy.ops.object.select_all(action='DESELECT')
    for obj in hand_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = hand_objects[0]
    bpy.ops.object.join()
    
    result = bpy.context.active_object
    result.name = name
    
    return result


def create_foot_armature(name: str, scale: float, location: tuple) -> bpy.types.Object:
    """
    Создание каркаса стопы
    """
    foot_objects = []
    
    # Основная часть стопы
    foot_base = create_cube(f"{name}_base", (scale * 6, scale * 12, scale * 2), location)
    foot_objects.append(foot_base)
    
    # Пятка
    heel = create_uv_sphere(f"{name}_heel", scale * 2.5, 
                            (location[0], location[1] - scale * 4, location[2]))
    foot_objects.append(heel)
    
    # Пальцы стопы (упрощённо)
    for i in range(5):
        toe_x = location[0] + (i - 2) * scale * 1.5
        toe = create_uv_sphere(f"{name}_toe_{i}", scale * 0.8,
                               (toe_x, location[1] + scale * 7, location[2]))
        foot_objects.append(toe)
    
    # Объединяем
    bpy.ops.object.select_all(action='DESELECT')
    for obj in foot_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = foot_objects[0]
    bpy.ops.object.join()
    
    result = bpy.context.active_object
    result.name = name
    
    return result


# ============================================================================
# ПОЛНЫЕ КАРКАСЫ
# ============================================================================

def create_humanoid_armature(settings: PuppetArmatureSettings = None) -> dict:
    """
    Создание полного гуманоидного каркаса
    Возвращает словарь с объектами по частям тела
    """
    if settings is None:
        settings = PuppetArmatureSettings()
    
    s = settings.scale_factor
    parts = {}
    
    # === ГОЛОВА ===
    head_loc = (0, 0, 150 * s)
    parts['head'] = create_uv_sphere("head", settings.head_height / 2, head_loc, segments=24)
    
    # === ШЕЯ ===
    neck_loc = (0, 0, 130 * s)
    parts['neck_ball'] = create_ball_joint("neck_ball", settings.ball_radius, neck_loc)
    
    # === ГРУДНАЯ КЛЕТКА ===
    torso_loc = (0, 0, 100 * s)
    parts['torso'] = create_torso_section("torso", settings.shoulder_width * s, 
                                          settings.torso_height * s, 15 * s, torso_loc)
    
    # === ТАЗ ===
    pelvis_loc = (0, 0, 55 * s)
    parts['pelvis'] = create_torso_section("pelvis", settings.hip_width * s,
                                           settings.pelvis_height * s, 12 * s, pelvis_loc)
    
    # === ПЛЕЧЕВЫЕ СУСТАВЫ ===
    shoulder_y = 115 * s
    shoulder_x = settings.shoulder_width / 2 * s
    
    # Левое плечо
    parts['shoulder_L_socket'] = create_socket_joint(
        "shoulder_L", settings.ball_radius, settings.ball_radius + settings.socket_gap,
        (-shoulder_x, 0, shoulder_y), stem_length=10 * s
    )
    
    # Правое плечо
    parts['shoulder_R_socket'] = create_socket_joint(
        "shoulder_R", settings.ball_radius, settings.ball_radius + settings.socket_gap,
        (shoulder_x, 0, shoulder_y), stem_length=10 * s
    )
    
    # === РУКИ ===
    # Левая рука
    upper_arm_L_loc = (-shoulder_x - settings.upper_arm_length / 2 * s, 0, shoulder_y - 10 * s)
    parts['upper_arm_L'] = create_bone_with_end_caps(
        "upper_arm_L", settings.upper_arm_length * s, settings.bone_diameter * s, upper_arm_L_loc,
        rotation=(0, math.pi / 2, 0)
    )
    
    # Локоть левый (шарнир)
    elbow_L_loc = (-shoulder_x - settings.upper_arm_length * s, 0, shoulder_y - 10 * s)
    parts['elbow_L_ball'], parts['elbow_L_socket'] = create_ball_socket_pair(
        "elbow_L", settings.ball_radius * 0.8, settings.socket_gap,
        elbow_L_loc, stem_length=8 * s
    )
    
    # Предплечье левое
    lower_arm_L_loc = (-shoulder_x - settings.upper_arm_length * s - settings.lower_arm_length / 2 * s, 
                        0, shoulder_y - 10 * s)
    parts['lower_arm_L'] = create_bone_with_end_caps(
        "lower_arm_L", settings.lower_arm_length * s, settings.bone_diameter * s, lower_arm_L_loc,
        rotation=(0, math.pi / 2, 0)
    )
    
    # Кисть левая
    hand_L_loc = (-shoulder_x - settings.upper_arm_length * s - settings.lower_arm_length * s - 5 * s,
                  0, shoulder_y - 10 * s)
    parts['hand_L'] = create_hand_armature("hand_L", s * 1.2, hand_L_loc)
    
    # Правая рука (аналогично)
    upper_arm_R_loc = (shoulder_x + settings.upper_arm_length / 2 * s, 0, shoulder_y - 10 * s)
    parts['upper_arm_R'] = create_bone_with_end_caps(
        "upper_arm_R", settings.upper_arm_length * s, settings.bone_diameter * s, upper_arm_R_loc,
        rotation=(0, -math.pi / 2, 0)
    )
    
    elbow_R_loc = (shoulder_x + settings.upper_arm_length * s, 0, shoulder_y - 10 * s)
    parts['elbow_R_ball'], parts['elbow_R_socket'] = create_ball_socket_pair(
        "elbow_R", settings.ball_radius * 0.8, settings.socket_gap,
        elbow_R_loc, stem_length=8 * s
    )
    
    lower_arm_R_loc = (shoulder_x + settings.upper_arm_length * s + settings.lower_arm_length / 2 * s,
                       0, shoulder_y - 10 * s)
    parts['lower_arm_R'] = create_bone_with_end_caps(
        "lower_arm_R", settings.lower_arm_length * s, settings.bone_diameter * s, lower_arm_R_loc,
        rotation=(0, -math.pi / 2, 0)
    )
    
    hand_R_loc = (shoulder_x + settings.upper_arm_length * s + settings.lower_arm_length * s + 5 * s,
                  0, shoulder_y - 10 * s)
    parts['hand_R'] = create_hand_armature("hand_R", s * 1.2, hand_R_loc)
    
    # === ТАЗОБЕДРЕННЫЕ СУСТАВЫ ===
    hip_y = 50 * s
    hip_x = settings.hip_width / 3 * s
    
    # Левое бедро
    parts['hip_L_ball'] = create_ball_joint(
        "hip_L_ball", settings.ball_radius * 1.2, (-hip_x, 0, hip_y)
    )
    
    # Правое бедро
    parts['hip_R_ball'] = create_ball_joint(
        "hip_R_ball", settings.ball_radius * 1.2, (hip_x, 0, hip_y)
    )
    
    # === НОГИ ===
    # Левая нога
    upper_leg_L_loc = (-hip_x, 0, hip_y - settings.upper_leg_length / 2 * s)
    parts['upper_leg_L'] = create_bone_with_end_caps(
        "upper_leg_L", settings.upper_leg_length * s, settings.bone_diameter * s * 1.2, upper_leg_L_loc
    )
    
    # Колено левое
    knee_L_loc = (-hip_x, 0, hip_y - settings.upper_leg_length * s)
    parts['knee_L_ball'], parts['knee_L_socket'] = create_ball_socket_pair(
        "knee_L", settings.ball_radius, settings.socket_gap,
        knee_L_loc, stem_length=8 * s
    )
    
    # Голень левая
    lower_leg_L_loc = (-hip_x, 0, hip_y - settings.upper_leg_length * s - settings.lower_leg_length / 2 * s)
    parts['lower_leg_L'] = create_bone_with_end_caps(
        "lower_leg_L", settings.lower_leg_length * s, settings.bone_diameter * s, lower_leg_L_loc
    )
    
    # Стопа левая
    foot_L_loc = (-hip_x, -3 * s, hip_y - settings.upper_leg_length * s - settings.lower_leg_length * s - 3 * s)
    parts['foot_L'] = create_foot_armature("foot_L", s * 1.5, foot_L_loc)
    
    # Правая нога (аналогично)
    upper_leg_R_loc = (hip_x, 0, hip_y - settings.upper_leg_length / 2 * s)
    parts['upper_leg_R'] = create_bone_with_end_caps(
        "upper_leg_R", settings.upper_leg_length * s, settings.bone_diameter * s * 1.2, upper_leg_R_loc
    )
    
    knee_R_loc = (hip_x, 0, hip_y - settings.upper_leg_length * s)
    parts['knee_R_ball'], parts['knee_R_socket'] = create_ball_socket_pair(
        "knee_R", settings.ball_radius, settings.socket_gap,
        knee_R_loc, stem_length=8 * s
    )
    
    lower_leg_R_loc = (hip_x, 0, hip_y - settings.upper_leg_length * s - settings.lower_leg_length / 2 * s)
    parts['lower_leg_R'] = create_bone_with_end_caps(
        "lower_leg_R", settings.lower_leg_length * s, settings.bone_diameter * s, lower_leg_R_loc
    )
    
    foot_R_loc = (hip_x, -3 * s, hip_y - settings.upper_leg_length * s - settings.lower_leg_length * s - 3 * s)
    parts['foot_R'] = create_foot_armature("foot_R", s * 1.5, foot_R_loc)
    
    return parts


def create_simple_puppet_armature(settings: PuppetArmatureSettings = None) -> dict:
    """
    Создание упрощённого каркаса куклы (для начинающих)
    Минимум деталей, проще печатать
    """
    if settings is None:
        settings = PuppetArmatureSettings()
    
    s = settings.scale_factor
    parts = {}
    
    # Упрощённый каркас - только основные суставы
    
    # Голова (полая сфера)
    head_loc = (0, 0, 80 * s)
    parts['head'] = create_uv_sphere("head_simple", 15 * s, head_loc, segments=20)
    
    # Торс (простой каркас)
    torso_loc = (0, 0, 50 * s)
    parts['torso'] = create_torso_section("torso_simple", 25 * s, 35 * s, 12 * s, torso_loc)
    
    # Таз
    pelvis_loc = (0, 0, 25 * s)
    parts['pelvis'] = create_torso_section("pelvis_simple", 20 * s, 15 * s, 10 * s, pelvis_loc)
    
    # Суставы - упрощённые шарики
    joint_positions = {
        'neck': (0, 0, 65 * s),
        'shoulder_L': (-15 * s, 0, 60 * s),
        'shoulder_R': (15 * s, 0, 60 * s),
        'elbow_L': (-30 * s, 0, 55 * s),
        'elbow_R': (30 * s, 0, 55 * s),
        'wrist_L': (-45 * s, 0, 50 * s),
        'wrist_R': (45 * s, 0, 50 * s),
        'hip_L': (-8 * s, 0, 20 * s),
        'hip_R': (8 * s, 0, 20 * s),
        'knee_L': (-8 * s, 0, 0 * s),
        'knee_R': (8 * s, 0, 0 * s),
        'ankle_L': (-8 * s, 0, -20 * s),
        'ankle_R': (8 * s, 0, -20 * s),
    }
    
    for name, pos in joint_positions.items():
        parts[f'{name}_ball'] = create_ball_joint(f"{name}_ball", settings.ball_radius * 0.8, pos)
    
    # Конечности - простые стержни
    bone_configs = [
        ("upper_arm_L", (-22 * s, 0, 57 * s), 18 * s),
        ("upper_arm_R", (22 * s, 0, 57 * s), 18 * s),
        ("lower_arm_L", (-37 * s, 0, 52 * s), 18 * s),
        ("lower_arm_R", (37 * s, 0, 52 * s), 18 * s),
        ("upper_leg_L", (-8 * s, 0, 10 * s), 20 * s),
        ("upper_leg_R", (8 * s, 0, 10 * s), 20 * s),
        ("lower_leg_L", (-8 * s, 0, -10 * s), 20 * s),
        ("lower_leg_R", (8 * s, 0, -10 * s), 20 * s),
    ]
    
    for name, pos, length in bone_configs:
        parts[name] = create_bone_segment(name, length, settings.bone_diameter * s, pos)
    
    return parts


def create_animal_quadruped_armature(settings: PuppetArmatureSettings = None) -> dict:
    """
    Создание каркаса четвероногого животного (собака, кошка)
    """
    if settings is None:
        settings = PuppetArmatureSettings()
    
    s = settings.scale_factor * 0.8
    parts = {}
    
    # Голова
    head_loc = (0, 25 * s, 40 * s)
    parts['head'] = create_uv_sphere("head_animal", 12 * s, head_loc, segments=20)
    
    # Морда (удлинённая)
    muzzle_loc = (0, 35 * s, 38 * s)
    parts['muzzle'] = create_uv_sphere("muzzle", 6 * s, muzzle_loc, segments=16)
    
    # Шея
    neck_loc = (0, 15 * s, 35 * s)
    parts['neck'] = create_bone_segment("neck", 15 * s, 4 * s, neck_loc)
    
    # Торс
    torso_loc = (0, 0, 25 * s)
    parts['torso'] = create_torso_section("torso_animal", 15 * s, 50 * s, 12 * s, torso_loc)
    
    # Хвост
    tail_locs = [(0, -30 * s, 25 * s), (0, -40 * s, 28 * s), (0, -50 * s, 32 * s)]
    for i, loc in enumerate(tail_locs):
        parts[f'tail_seg_{i}'] = create_bone_segment(f"tail_seg_{i}", 12 * s, 2 * s, loc)
    
    # Ноги (4 лапы)
    leg_positions = {
        'front_L': (-10 * s, 15 * s, 0),
        'front_R': (10 * s, 15 * s, 0),
        'back_L': (-10 * s, -15 * s, 0),
        'back_R': (10 * s, -15 * s, 0),
    }
    
    for leg_name, base_pos in leg_positions.items():
        # Верхняя часть ноги
        upper_loc = (base_pos[0], base_pos[1], base_pos[2] + 20 * s)
        parts[f'{leg_name}_upper'] = create_bone_segment(f"{leg_name}_upper", 20 * s, 3 * s, upper_loc)
        
        # Колено/локоть
        knee_loc = (base_pos[0], base_pos[1], base_pos[2] + 10 * s)
        parts[f'{leg_name}_joint'] = create_ball_joint(f"{leg_name}_joint", settings.ball_radius * 0.7, knee_loc)
        
        # Нижняя часть ноги
        lower_loc = (base_pos[0], base_pos[1], base_pos[2] + 5 * s)
        parts[f'{leg_name}_lower'] = create_bone_segment(f"{leg_name}_lower", 10 * s, 2.5 * s, lower_loc)
        
        # Лапа
        paw_loc = (base_pos[0], base_pos[1] + 3 * s, base_pos[2])
        parts[f'{leg_name}_paw'] = create_uv_sphere(f"{leg_name}_paw", 3 * s, paw_loc, segments=12)
    
    return parts


# ============================================================================
# ФУНКЦИИ ЭКСПОРТА И ОРГАНИЗАЦИИ
# ============================================================================

def organize_into_collections(parts: dict, collection_name: str = "PuppetArmature"):
    """
    Организация частей в коллекции по категориям
    """
    # Создаём главную коллекцию
    main_collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(main_collection)
    
    # Определяем категории
    categories = {
        'head': ['head', 'muzzle', 'neck'],
        'torso': ['torso', 'pelvis', 'spine'],
        'arm_L': ['shoulder_L', 'elbow_L', 'wrist_L', 'arm_L', 'hand_L', 'upper_arm_L', 'lower_arm_L'],
        'arm_R': ['shoulder_R', 'elbow_R', 'wrist_R', 'arm_R', 'hand_R', 'upper_arm_R', 'lower_arm_R'],
        'leg_L': ['hip_L', 'knee_L', 'ankle_L', 'leg_L', 'foot_L', 'upper_leg_L', 'lower_leg_L'],
        'leg_R': ['hip_R', 'knee_R', 'ankle_R', 'leg_R', 'foot_R', 'upper_leg_R', 'lower_leg_R'],
        'tail': ['tail'],
        'joints': ['ball', 'socket', 'joint'],
    }
    
    # Создаём подколлекции
    sub_collections = {}
    for cat_name in categories.keys():
        sub = bpy.data.collections.new(f"{collection_name}_{cat_name}")
        main_collection.children.link(sub)
        sub_collections[cat_name] = sub
    
    # Распределяем объекты
    for part_name, obj in parts.items():
        assigned = False
        for cat_name, keywords in categories.items():
            if any(kw.lower() in part_name.lower() for kw in keywords):
                sub_collections[cat_name].objects.link(obj)
                assigned = True
                break
        
        if not assigned:
            main_collection.objects.link(obj)
        
        # Убираем из основной коллекции сцены
        for coll in bpy.data.collections:
            if obj.name in coll.objects:
                try:
                    coll.objects.unlink(obj)
                except:
                    pass


def apply_print_materials(parts: dict):
    """
    Применение материалов для визуализации частей для печати
    """
    # Создаём материалы
    mat_joint = create_material("Joint_Material", (0.8, 0.2, 0.2))  # Красный - суставы
    mat_bone = create_material("Bone_Material", (0.3, 0.5, 0.8))   # Синий - кости
    mat_body = create_material("Body_Material", (0.5, 0.5, 0.5))   # Серый - тело
    
    for part_name, obj in parts.items():
        if 'ball' in part_name.lower() or 'socket' in part_name.lower() or 'joint' in part_name.lower():
            obj.data.materials.append(mat_joint)
        elif 'arm' in part_name.lower() or 'leg' in part_name.lower() or 'bone' in part_name.lower():
            obj.data.materials.append(mat_bone)
        else:
            obj.data.materials.append(mat_body)


def export_to_stl(output_dir: str, parts: dict, prefix: str = "puppet"):
    """
    Экспорт частей в STL файлы для 3D печати
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    exported_files = []
    
    for part_name, obj in parts.items():
        # Выбираем объект
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        # Экспортируем
        filepath = os.path.join(output_dir, f"{prefix}_{part_name}.stl")
        bpy.ops.export_mesh.stl(
            filepath=filepath,
            use_selection=True,
            global_scale=0.001,  # Конвертация мм -> м для STL
            use_mesh_modifiers=True
        )
        exported_files.append(filepath)
        print(f"Exported: {filepath}")
    
    return exported_files


# ============================================================================
# ОСНОВНАЯ ФУНКЦИЯ
# ============================================================================

def clear_scene():
    """Очистка сцены перед генерацией"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Удаляем все коллекции кроме основной
    for coll in bpy.data.collections:
        if coll.name not in ['Collection', 'Master Collection']:
            bpy.data.collections.remove(coll)


def generate_puppet_armature(armature_type: str = 'humanoid', scale: float = 1.0,
                              export_stl: bool = False, output_dir: str = "/tmp/puppet_parts"):
    """
    Главная функция генерации каркаса
    
    Параметры:
    - armature_type: 'humanoid', 'simple', 'animal'
    - scale: масштаб модели
    - export_stl: экспортировать в STL
    - output_dir: директория для экспорта
    """
    # Очищаем сцену
    clear_scene()
    
    # Создаём настройки
    settings = PuppetArmatureSettings()
    settings.scale_factor = scale
    
    # Генерируем каркас
    print(f"Generating {armature_type} armature...")
    
    if armature_type == 'humanoid':
        parts = create_humanoid_armature(settings)
    elif armature_type == 'simple':
        parts = create_simple_puppet_armature(settings)
    elif armature_type == 'animal':
        parts = create_animal_quadruped_armature(settings)
    else:
        raise ValueError(f"Unknown armature type: {armature_type}")
    
    print(f"Generated {len(parts)} parts")
    
    # Организуем в коллекции
    organize_into_collections(parts, f"PuppetArmature_{armature_type}")
    
    # Применяем материалы
    apply_print_materials(parts)
    
    # Экспортируем
    if export_stl:
        exported = export_to_stl(output_dir, parts, armature_type)
        print(f"Exported {len(exported)} STL files to {output_dir}")
    
    return parts


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    # Генерация гуманоидного каркаса
    # Измените тип на 'simple' или 'animal' для других вариантов
    
    parts = generate_puppet_armature(
        armature_type='humanoid',  # 'humanoid', 'simple', 'animal'
        scale=1.0,
        export_stl=False,  # Установите True для экспорта STL
        output_dir="/home/z/my-project/download/stl_parts"
    )
    
    print("\n" + "="*60)
    print("КАРКАС КУКЛЫ УСПЕШНО СОЗДАН!")
    print("="*60)
    print("\nСозданные части:")
    for name in sorted(parts.keys()):
        print(f"  - {name}")
    print("\nИнструкция:")
    print("1. Изучите модель в 3D viewport")
    print("2. Для печати экспортируйте в STL: File > Export > Stl")
    print("3. Рекомендуемый материал: фотополимерная смола для SLA")
    print("4. Размер шаров суставов: 3-4 мм (для мини-кукол)")
    print("="*60)
