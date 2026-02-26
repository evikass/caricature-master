"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     ДЕТАЛЬНЫЙ КАРКАС КИСТИ РУКИ ДЛЯ КУКОЛЬНОЙ АНИМАЦИИ                       ║
║     Detailed Hand Armature for Stop-Motion Animation                        ║
║                                                                              ║
║     Совместимость: Blender 3.x / 4.x / 5.x                                   ║
║     Для печати на SLA 3D-принтере                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Инструкция:
1. Открой Blender → Scripting → New
2. Скопируй этот скрипт
3. Run Script (Alt+P)
4. Экспорт: File → Export → STL

Особенности:
- Каждый палец имеет 3 сустава (кроме большого - 2)
- Все шарики и сокеты - отдельные объекты
- Можно печатать по частям и собирать
"""

import bpy
import math
from mathutils import Vector
import os

# ============================================================================
# НАСТРОЙКИ
# ============================================================================

class HandSettings:
    """Настройки каркаса кисти"""
    
    # Размер кисти (в метрах)
    HAND_SCALE = 0.06  # 6 см - стандартная кисть для 15-20 см куклы
    
    # Размеры суставов
    JOINT_BALL_RADIUS = 0.003      # 3 мм - шарики суставов
    JOINT_SOCKET_THICKNESS = 0.002  # 2 мм - толщина стенки сокета
    JOINT_TOLERANCE = 0.0002        # 0.2 мм - зазор для движения
    
    # Размеры "костей" (цилиндры между суставами)
    BONE_RADIUS = 0.002  # 2 мм - радиус костей
    
    # Цвета материалов
    JOINT_COLOR = (0.85, 0.25, 0.15, 1.0)   # Красно-оранжевый - суставы
    BONE_COLOR = (0.35, 0.35, 0.45, 1.0)    # Серо-синий - кости
    PALM_COLOR = (0.4, 0.4, 0.5, 1.0)       # Серый - ладонь
    SOCKET_COLOR = (0.2, 0.2, 0.25, 1.0)    # Тёмно-серый - сокеты


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
    bsdf.inputs['Metallic'].default_value = 0.6
    bsdf.inputs['Roughness'].default_value = 0.35
    return mat


def create_sphere(location, radius, name, material=None):
    """Создаёт сферу (шарик сустава)"""
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        location=location,
        segments=24,
        ring_count=16
    )
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj


def create_socket(location, ball_radius, name, material=None, opening_angle=0.5):
    """
    Создаёт сокет (втулку) для шарика
    
    opening_angle: какая часть сферы открыта (0.5 = половина)
    """
    inner_radius = ball_radius + HandSettings.JOINT_TOLERANCE
    outer_radius = inner_radius + HandSettings.JOINT_SOCKET_THICKNESS
    
    # Создаём внешний шар
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=outer_radius,
        location=location,
        segments=24,
        ring_count=16
    )
    outer = bpy.context.active_object
    outer.name = f"{name}_outer"
    
    # Создаём внутренний шар для вычитания
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=inner_radius,
        location=location,
        segments=24,
        ring_count=16
    )
    inner = bpy.context.active_object
    inner.name = f"{name}_inner_temp"
    
    # Boolean-вычитание
    modifier = outer.modifiers.new(name="Cut", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = inner
    
    bpy.context.view_layer.objects.active = outer
    bpy.ops.object.modifier_apply(modifier="Cut")
    
    # Удаляем внутренний шар
    bpy.data.objects.remove(inner, do_unlink=True)
    
    outer.name = name
    if material:
        outer.data.materials.append(material)
    
    return outer


def create_cylinder(start, end, radius, name, material=None):
    """Создаёт цилиндр между двумя точками"""
    direction = Vector(end) - Vector(start)
    length = direction.length
    
    if length < 0.0001:
        length = 0.001
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=length,
        location=((Vector(start) + Vector(end)) / 2),
        rotation=(0, 0, 0)
    )
    obj = bpy.context.active_object
    obj.name = name
    
    # Поворачиваем
    direction.normalize()
    up = Vector((0, 0, 1))
    dot = up.dot(direction)
    
    if abs(dot) < 0.9999:
        angle = math.acos(max(-1, min(1, dot)))
        axis = up.cross(direction).normalized()
        if axis.length > 0:
            obj.rotation_mode = 'AXIS_ANGLE'
            obj.rotation_axis_angle = (angle, axis.x, axis.y, axis.z)
    elif dot < 0:
        obj.rotation_euler = (math.pi, 0, 0)
    
    if material:
        obj.data.materials.append(material)
    
    return obj


# ============================================================================
# СОЗДАНИЕ ПАЛЬЦА
# ============================================================================

def create_finger(name, base_pos, angles, lengths, mat_joint, mat_bone, mat_socket):
    """
    Создаёт один палец с полным набором суставов
    
    Параметры:
        name: имя пальца (Thumb, Index, etc.)
        base_pos: базовая позиция (x, y, z)
        angles: углы наклона каждого сегмента [xy_angle, z_angle, ...]
        lengths: длины каждого сегмента
        mat_joint, mat_bone, mat_socket: материалы
    
    Возвращает:
        (balls, sockets, bones) - списки объектов
    """
    balls = []
    sockets = []
    bones = []
    
    ball_r = HandSettings.JOINT_BALL_RADIUS
    bone_r = HandSettings.BONE_RADIUS
    
    current_pos = Vector(base_pos)
    
    for i, length in enumerate(lengths):
        # Угол направления
        xy_angle = angles[i * 2] if i * 2 < len(angles) else 0
        z_angle = angles[i * 2 + 1] if i * 2 + 1 < len(angles) else 0
        
        # === ШАРИК СУСТАВА ===
        ball = create_sphere(
            location=current_pos,
            radius=ball_r,
            name=f"{name}_Joint_{i+1}_Ball",
            material=mat_joint
        )
        balls.append(ball)
        
        # === СОКЕТ (опционально - для сборки) ===
        socket = create_socket(
            location=current_pos,
            ball_radius=ball_r,
            name=f"{name}_Joint_{i+1}_Socket",
            material=mat_socket
        )
        sockets.append(socket)
        
        # === КОСТЬ (от этого сустава к следующему) ===
        if i < len(lengths) - 1:
            # Вычисляем следующую позицию
            direction = Vector((
                math.sin(xy_angle) * math.cos(z_angle),
                math.cos(xy_angle) * math.cos(z_angle),
                math.sin(z_angle)
            ))
            next_pos = current_pos + direction * length
            
            bone = create_cylinder(
                start=current_pos,
                end=next_pos,
                radius=bone_r,
                name=f"{name}_Bone_{i+1}",
                material=mat_bone
            )
            bones.append(bone)
            
            current_pos = next_pos
    
    # === КОНЧИК ПАЛЬЦА ===
    tip = create_sphere(
        location=current_pos,
        radius=ball_r * 0.8,
        name=f"{name}_Tip",
        material=mat_joint
    )
    balls.append(tip)
    
    return balls, sockets, bones


# ============================================================================
# СОЗДАНИЕ ЛАДОНИ
# ============================================================================

def create_palm(scale, mat_palm, mat_socket):
    """
    Создаёт основание ладони с гнёздами для пальцев
    """
    objects = []
    
    # Основание ладони
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    palm = bpy.context.active_object
    palm.scale = (scale * 0.8, scale * 0.4, scale * 0.25)
    palm.name = "Palm_Base"
    palm.data.materials.append(mat_palm)
    objects.append(palm)
    
    # Гнёзда для пальцев (5 штук)
    finger_positions = [
        ("Thumb", -0.35, 0.15, 0.0),   # Большой
        ("Index", -0.2, 0.0, 0.5),      # Указательный
        ("Middle", 0.0, 0.0, 0.55),     # Средний
        ("Ring", 0.2, 0.0, 0.5),        # Безымянный
        ("Pinky", 0.35, 0.0, 0.4),      # Мизинец
    ]
    
    ball_r = HandSettings.JOINT_BALL_RADIUS
    
    for fname, fx, fy, fz in finger_positions:
        pos = (fx * scale, fy * scale, fz * scale)
        
        # Гнездо
        socket = create_socket(
            location=pos,
            ball_radius=ball_r,
            name=f"Palm_{fname}_Socket",
            material=mat_socket
        )
        objects.append(socket)
    
    return objects


# ============================================================================
# СОЗДАНИЕ ПОЛНОЙ КИСТИ
# ============================================================================

def create_full_hand(scale=None, separate_parts=True):
    """
    Создаёт полный каркас кисти
    
    Параметры:
        scale: размер кисти (по умолчанию из настроек)
        separate_parts: True - каждый сустав отдельно, False - объединить
    
    Возвращает:
        Список всех объектов
    """
    if scale is None:
        scale = HandSettings.HAND_SCALE
    
    # Материалы
    mat_joint = create_material("Joint_Material", HandSettings.JOINT_COLOR)
    mat_bone = create_material("Bone_Material", HandSettings.BONE_COLOR)
    mat_palm = create_material("Palm_Material", HandSettings.PALM_COLOR)
    mat_socket = create_material("Socket_Material", HandSettings.SOCKET_COLOR)
    
    all_objects = []
    
    # === ЛАДОНЬ ===
    palm_objects = create_palm(scale, mat_palm, mat_socket)
    all_objects.extend(palm_objects)
    
    # === ПАЛЬЦЫ ===
    # Данные пальцев: (имя, базовая позиция, углы, длины сегментов)
    ball_r = HandSettings.JOINT_BALL_RADIUS
    
    fingers_data = [
        # Большой палец - 2 сустава, особое расположение
        ("Thumb", 
         (-0.35 * scale, 0.15 * scale, 0.0),
         [-0.4, 0.3, -0.3, 0.2],  # Углы
         [scale * 0.18, scale * 0.15]),  # Длины
        
        # Указательный - 3 сустава
        ("Index",
         (-0.2 * scale, 0.0 * scale, 0.5 * scale),
         [-0.05, 0.4, 0.0, 0.35, 0.05, 0.25],
         [scale * 0.2, scale * 0.15, scale * 0.12]),
        
        # Средний - 3 сустава (самый длинный)
        ("Middle",
         (0.0 * scale, 0.0 * scale, 0.55 * scale),
         [0.0, 0.45, 0.0, 0.4, 0.0, 0.3],
         [scale * 0.22, scale * 0.16, scale * 0.13]),
        
        # Безымянный - 3 сустава
        ("Ring",
         (0.2 * scale, 0.0 * scale, 0.5 * scale),
         [0.05, 0.4, 0.05, 0.35, 0.1, 0.25],
         [scale * 0.2, scale * 0.14, scale * 0.11]),
        
        # Мизинец - 3 сустава (самый короткий)
        ("Pinky",
         (0.35 * scale, 0.0 * scale, 0.4 * scale),
         [0.15, 0.35, 0.1, 0.3, 0.15, 0.2],
         [scale * 0.16, scale * 0.12, scale * 0.1]),
    ]
    
    for finger_name, base_pos, angles, lengths in fingers_data:
        balls, sockets, bones = create_finger(
            finger_name, base_pos, angles, lengths,
            mat_joint, mat_bone, mat_socket
        )
        all_objects.extend(balls)
        all_objects.extend(sockets)
        all_objects.extend(bones)
    
    # === ЗАПЯСТЬЕ ===
    wrist_pos = (0, -scale * 0.25, scale * 0.15)
    
    # Шарик запястья
    wrist_ball = create_sphere(
        location=wrist_pos,
        radius=ball_r * 1.3,
        name="Wrist_Joint_Ball",
        material=mat_joint
    )
    all_objects.append(wrist_ball)
    
    # Сокет запястья
    wrist_socket = create_socket(
        location=wrist_pos,
        ball_radius=ball_r * 1.3,
        name="Wrist_Joint_Socket",
        material=mat_socket
    )
    all_objects.append(wrist_socket)
    
    # Соединение ладонь-запястье
    wrist_bone = create_cylinder(
        start=(0, -scale * 0.1, scale * 0.15),
        end=wrist_pos,
        radius=HandSettings.BONE_RADIUS * 1.2,
        name="Wrist_Bone",
        material=mat_bone
    )
    all_objects.append(wrist_bone)
    
    return all_objects


# ============================================================================
# СОЗДАНИЕ НАБОРА ДЛЯ ПЕЧАТИ
# ============================================================================

def create_printable_kit():
    """
    Создаёт набор деталей, разложенных для печати
    Каждый тип деталей в своём ряду
    """
    clear_scene()
    
    scale = HandSettings.HAND_SCALE
    
    # Материалы
    mat_joint = create_material("Joint_Material", HandSettings.JOINT_COLOR)
    mat_bone = create_material("Bone_Material", HandSettings.BONE_COLOR)
    mat_socket = create_material("Socket_Material", HandSettings.SOCKET_COLOR)
    
    all_objects = []
    
    ball_r = HandSettings.JOINT_BALL_RADIUS
    
    # === РЯД 1: ШАРИКИ СУСТАВОВ ===
    row_y = 0.05
    ball_positions = []
    
    # Шарики для каждого сустава каждого пальца
    finger_joints = [
        ("Thumb", 2),   # 2 сустава + кончик
        ("Index", 3),
        ("Middle", 3),
        ("Ring", 3),
        ("Pinky", 3),
    ]
    
    x_pos = 0
    for fname, joint_count in finger_joints:
        for i in range(joint_count + 1):  # +1 для кончика
            ball = create_sphere(
                location=(x_pos * 0.012, row_y, 0),
                radius=ball_r * (0.8 if i == joint_count else 1.0),
                name=f"Ball_{fname}_{i+1}",
                material=mat_joint
            )
            all_objects.append(ball)
            x_pos += 1
        
        x_pos += 1  # Промежуток между пальцами
    
    # Шарик запястья
    wrist_ball = create_sphere(
        location=(x_pos * 0.012, row_y, 0),
        radius=ball_r * 1.3,
        name="Ball_Wrist",
        material=mat_joint
    )
    all_objects.append(wrist_ball)
    
    # === РЯД 2: СОКЕТЫ ===
    row_y = 0.05
    x_pos = 0
    
    for fname, joint_count in finger_joints:
        for i in range(joint_count):
            socket = create_socket(
                location=(x_pos * 0.015, row_y, 0.025),
                ball_radius=ball_r,
                name=f"Socket_{fname}_{i+1}",
                material=mat_socket
            )
            all_objects.append(socket)
            x_pos += 1
        x_pos += 1
    
    # Сокет запястья
    wrist_socket = create_socket(
        location=(x_pos * 0.015, row_y, 0.025),
        ball_radius=ball_r * 1.3,
        name="Socket_Wrist",
        material=mat_socket
    )
    all_objects.append(wrist_socket)
    
    # === РЯД 3: КОСТИ ===
    row_y = 0.1
    x_pos = 0
    
    finger_bones = [
        ("Thumb", 2),   # 2 кости
        ("Index", 3),
        ("Middle", 3),
        ("Ring", 3),
        ("Pinky", 3),
    ]
    
    bone_lengths = [
        [0.012, 0.01],           # Thumb
        [0.014, 0.01, 0.008],    # Index
        [0.015, 0.011, 0.009],   # Middle
        [0.014, 0.01, 0.008],    # Ring
        [0.011, 0.008, 0.006],   # Pinky
    ]
    
    for fidx, (fname, bone_count) in enumerate(finger_bones):
        lengths = bone_lengths[fidx]
        for i in range(bone_count):
            bone = create_cylinder(
                start=(x_pos * 0.02, row_y, 0),
                end=(x_pos * 0.02, row_y, lengths[i]),
                radius=HandSettings.BONE_RADIUS,
                name=f"Bone_{fname}_{i+1}",
                material=mat_bone
            )
            all_objects.append(bone)
            x_pos += 1
        x_pos += 1
    
    # === ЛАДОНЬ (отдельно, масштабировано) ===
    palm_pos = (0, 0.15, 0)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=palm_pos)
    palm = bpy.context.active_object
    palm.scale = (scale * 0.8, scale * 0.4, scale * 0.25)
    palm.name = "Palm_Base_Print"
    palm.data.materials.append(mat_joint)
    all_objects.append(palm)
    
    # Добавляем освещение
    setup_scene()
    
    return all_objects


def setup_scene():
    """Настраивает сцену"""
    # Освещение
    bpy.ops.object.light_add(type='SUN', location=(1, -1, 2))
    light1 = bpy.context.active_object
    light1.data.energy = 2.5
    
    bpy.ops.object.light_add(type='SUN', location=(-1, 1, 1.5))
    light2 = bpy.context.active_object
    light2.data.energy = 1.5
    
    # Камера
    bpy.ops.object.camera_add(location=(0.08, -0.25, 0.15))
    cam = bpy.context.active_object
    
    direction = Vector((0.04, 0.05, 0)) - Vector(cam.location)
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()
    
    bpy.context.scene.camera = cam
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 32


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """Главная функция"""
    print("\n" + "="*60)
    print("  ДЕТАЛЬНЫЙ КАРКАС КИСТИ РУКИ")
    print("  Detailed Hand Armature for SLA Printing")
    print("="*60)
    
    # Выбор режима:
    # 1. Полная кисть в сборе (для превью)
    # 2. Набор деталей для печати
    
    print("\nСоздаю набор для 3D-печати...")
    create_printable_kit()
    
    print("\n✓ Создано:")
    print("  - Шарики суставов (Row 1)")
    print("  - Сокеты/втулки (Row 2)")  
    print("  - Кости пальцев (Row 3)")
    print("  - Основа ладони")
    print("\nДля экспорта: File → Export → STL")


def create_assembled_hand():
    """Создаёт собранную кисть для превью"""
    clear_scene()
    objects = create_full_hand()
    setup_scene()
    return objects


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    main()
