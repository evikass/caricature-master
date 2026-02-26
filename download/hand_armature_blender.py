"""
╔══════════════════════════════════════════════════════════════════════════════╗
║     КАРКАС КИСТИ ДЛЯ КУКОЛЬНОЙ АНИМАЦИИ                                      ║
║     Hand Armature for Stop-Motion Animation                                  ║
║                                                                              ║
║     Совместимость: Blender 3.x / 4.x / 5.x                                   ║
║     Для печати на SLA 3D-принтере                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Инструкция:
1. Blender → Scripting → New
2. Вставь скрипт
3. Run Script (Alt+P)

Версия: 2.0
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
    # 0.06 = 6 см (для куклы ~15-20 см)
    HAND_SCALE = 0.06
    
    # Диаметр суставов
    JOINT_RADIUS = 0.003  # 3 мм
    
    # Диаметр костей (сегментов пальцев)
    BONE_RADIUS = 0.002   # 2 мм
    
    # Диаметр ладони
    PALM_JOINT_RADIUS = 0.004  # 4 мм
    
    # Зазор для SLA печати
    JOINT_TOLERANCE = 0.0003  # 0.3 мм
    
    # Цвета материалов
    JOINT_COLOR = (0.85, 0.25, 0.15, 1.0)   # Красно-оранжевый - суставы
    BONE_COLOR = (0.35, 0.35, 0.45, 1.0)    # Серый - кости
    PALM_COLOR = (0.4, 0.4, 0.5, 1.0)       # Тёмно-серый - ладонь


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
    """Создаёт сферу (шарнир)"""
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
    """Создаёт цилиндр (кость)"""
    direction = Vector(end) - Vector(start)
    length = direction.length
    
    if length < 0.0001:
        length = 0.001
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=length,
        location=((Vector(start) + Vector(end)) / 2)
    )
    obj = bpy.context.active_object
    obj.name = name
    
    # Поворот
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


def create_palm(scale, material):
    """Создаёт ладонь с креплениями для пальцев"""
    objects = []
    
    # Основание ладони (блок)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    palm = bpy.context.active_object
    palm.scale = (scale * 0.8, scale * 0.25, scale * 0.35)
    palm.name = "Palm_Base"
    palm.data.materials.append(material)
    objects.append(palm)
    
    # Суставы основания пальцев (MCP joints)
    mcp_positions = [
        ("Thumb_MCP", -0.32, 0.08, 0.65),
        ("Index_MCP", -0.16, 0.02, 0.75),
        ("Middle_MCP", 0.0, 0.0, 0.78),
        ("Ring_MCP", 0.16, 0.01, 0.75),
        ("Pinky_MCP", 0.30, 0.03, 0.68),
    ]
    
    for name, x, y, z in mcp_positions:
        joint = create_sphere(
            (x * scale, y * scale, z * scale),
            HandSettings.JOINT_RADIUS * 1.1,
            name,
            material
        )
        objects.append(joint)
    
    # Запястный сустав (wrist)
    wrist = create_sphere(
        (0, -scale * 0.08, -scale * 0.1),
        HandSettings.PALM_JOINT_RADIUS,
        "Wrist_Joint",
        material
    )
    objects.append(wrist)
    
    # Крепление к предплечью
    forearm_mount = create_cylinder(
        (0, -scale * 0.08, -scale * 0.1),
        (0, -scale * 0.15, -scale * 0.25),
        HandSettings.JOINT_RADIUS * 0.8,
        "Forearm_Mount",
        material
    )
    objects.append(forearm_mount)
    
    return objects


def create_finger(scale, name, base_pos, length_mult, segments, mat_joint, mat_bone, angles=(0, 0)):
    """
    Создаёт палец с суставами
    
    Параметры:
        scale: масштаб
        name: имя пальца
        base_pos: позиция основания (x, y, z)
        length_mult: множитель длины
        segments: количество сегментов (обычно 3)
        mat_joint: материал суставов
        mat_bone: материал костей
        angles: углы наклона (боковой, переднезадний)
    """
    objects = []
    
    base_x, base_y, base_z = base_pos
    seg_length = scale * 0.28 * length_mult
    
    # Углы в радианы
    angle_side = math.radians(angles[0])    # Боковой наклон
    angle_front = math.radians(angles[1])   # Переднезадний наклон
    
    current_x = base_x
    current_y = base_y
    current_z = base_z
    
    for i in range(segments):
        # Сустав
        joint_name = f"{name}_Joint_{i+1}"
        joint = create_sphere(
            (current_x, current_y, current_z),
            HandSettings.JOINT_RADIUS,
            joint_name,
            mat_joint
        )
        objects.append(joint)
        
        # Кость к следующему суставу
        if i < segments:
            # Вычисляем позицию следующего сустава с учётом углов
            next_x = current_x + seg_length * math.sin(angle_side)
            next_y = current_y + seg_length * 0.05  # Небольшой наклон вперёд
            next_z = current_z + seg_length * math.cos(angle_front)
            
            bone_name = f"{name}_Bone_{i+1}"
            bone = create_cylinder(
                (current_x, current_y, current_z),
                (next_x, next_y, next_z),
                HandSettings.BONE_RADIUS,
                bone_name,
                mat_bone
            )
            objects.append(bone)
            
            # Обновляем позицию
            current_x = next_x
            current_y = next_y
            current_z = next_z
    
    # Кончик пальца
    tip = create_sphere(
        (current_x, current_y, current_z),
        HandSettings.JOINT_RADIUS * 0.8,
        f"{name}_Tip",
        mat_joint
    )
    objects.append(tip)
    
    return objects


def create_thumb(scale, mat_joint, mat_bone):
    """Создаёт большой палец с особой геометрией"""
    objects = []
    
    # Основание (CMC joint) - ближе к ладони
    cmc_pos = (-scale * 0.35, scale * 0.02, scale * 0.35)
    cmc = create_sphere(cmc_pos, HandSettings.JOINT_RADIUS * 1.2, "Thumb_CMC", mat_joint)
    objects.append(cmc)
    
    # Первый сегмент (matacarpal)
    mcp_pos = (
        cmc_pos[0] - scale * 0.18,
        cmc_pos[1] + scale * 0.08,
        cmc_pos[2] + scale * 0.12
    )
    
    bone1 = create_cylinder(
        cmc_pos, mcp_pos,
        HandSettings.BONE_RADIUS * 1.1,
        "Thumb_Metacarpal",
        mat_bone
    )
    objects.append(bone1)
    
    # MCP сустав
    mcp = create_sphere(mcp_pos, HandSettings.JOINT_RADIUS, "Thumb_MCP", mat_joint)
    objects.append(mcp)
    
    # Второй сегмент (proximal phalanx)
    pip_pos = (
        mcp_pos[0] - scale * 0.15,
        mcp_pos[1] + scale * 0.12,
        mcp_pos[2] + scale * 0.2
    )
    
    bone2 = create_cylinder(
        mcp_pos, pip_pos,
        HandSettings.BONE_RADIUS,
        "Thumb_Proximal",
        mat_bone
    )
    objects.append(bone2)
    
    # IP сустав
    ip = create_sphere(pip_pos, HandSettings.JOINT_RADIUS, "Thumb_IP", mat_joint)
    objects.append(ip)
    
    # Третий сегмент (distal phalanx)
    tip_pos = (
        pip_pos[0] - scale * 0.1,
        pip_pos[1] + scale * 0.08,
        pip_pos[2] + scale * 0.15
    )
    
    bone3 = create_cylinder(
        pip_pos, tip_pos,
        HandSettings.BONE_RADIUS * 0.9,
        "Thumb_Distal",
        mat_bone
    )
    objects.append(bone3)
    
    # Кончик
    tip = create_sphere(tip_pos, HandSettings.JOINT_RADIUS * 0.8, "Thumb_Tip", mat_joint)
    objects.append(tip)
    
    return objects


def create_hand_armature(scale=None):
    """Создаёт полный каркас кисти"""
    if scale is None:
        scale = HandSettings.HAND_SCALE
    
    mat_joint = create_material("Joint_Material", HandSettings.JOINT_COLOR)
    mat_bone = create_material("Bone_Material", HandSettings.BONE_COLOR)
    mat_palm = create_material("Palm_Material", HandSettings.PALM_COLOR)
    
    objects = []
    
    # === ЛАДОНЬ ===
    palm_objects = create_palm(scale, mat_palm)
    objects.extend(palm_objects)
    
    # === БОЛЬШОЙ ПАЛЕЦ ===
    thumb_objects = create_thumb(scale, mat_joint, mat_bone)
    objects.extend(thumb_objects)
    
    # === ОСТАЛЬНЫЕ ПАЛЬЦЫ ===
    fingers_config = [
        # (имя, x, y, z, длина, сегменты, (боковой угол, передний угол))
        ("Index", -0.16, 0.02, 0.75, 1.0, 3, (-3, 0)),
        ("Middle", 0.0, 0.0, 0.78, 1.15, 3, (0, 0)),
        ("Ring", 0.16, 0.01, 0.75, 1.05, 3, (3, 0)),
        ("Pinky", 0.30, 0.03, 0.68, 0.85, 3, (8, 0)),
    ]
    
    for name, x, y, z, length, segs, angles in fingers_config:
        base_pos = (x * scale, y * scale, z * scale)
        finger_objects = create_finger(
            scale, name, base_pos, length, segs,
            mat_joint, mat_bone, angles
        )
        objects.extend(finger_objects)
    
    return objects


def create_right_hand(scale=None):
    """Создаёт ПРАВУЮ кисть (зеркально отражённую)"""
    if scale is None:
        scale = HandSettings.HAND_SCALE
    
    objects = create_hand_armature(scale)
    
    # Отражаем по оси X
    for obj in objects:
        obj.scale.x = -obj.scale.x
    
    # Переименовываем
    for obj in objects:
        obj.name = obj.name.replace("Thumb", "R_Thumb")
        obj.name = obj.name.replace("Index", "R_Index")
        obj.name = obj.name.replace("Middle", "R_Middle")
        obj.name = obj.name.replace("Ring", "R_Ring")
        obj.name = obj.name.replace("Pinky", "R_Pinky")
        obj.name = obj.name.replace("Palm", "R_Palm")
        obj.name = obj.name.replace("Wrist", "R_Wrist")
        obj.name = obj.name.replace("Forearm", "R_Forearm")
        if obj.name.startswith("J") or obj.name.startswith("Bone"):
            obj.name = "R_" + obj.name
    
    return objects


def create_left_hand(scale=None):
    """Создаёт ЛЕВУЮ кисть"""
    if scale is None:
        scale = HandSettings.HAND_SCALE
    
    objects = create_hand_armature(scale)
    
    # Переименовываем
    for obj in objects:
        obj.name = "L_" + obj.name
    
    return objects


def create_both_hands(scale=None):
    """Создаёт обе кисти"""
    if scale is None:
        scale = HandSettings.HAND_SCALE
    
    # Левая рука (слева)
    left_objects = create_left_hand(scale)
    for obj in left_objects:
        obj.location.x = -scale * 1.2
    
    # Правая рука (справа, отражённая)
    right_objects = create_right_hand(scale)
    for obj in right_objects:
        obj.location.x = scale * 1.2
    
    return left_objects + right_objects


def setup_scene():
    """Настраивает сцену"""
    # Свет
    bpy.ops.object.light_add(type='SUN', location=(2, -2, 3))
    bpy.context.active_object.data.energy = 3
    
    bpy.ops.object.light_add(type='SUN', location=(-2, -1, 2))
    bpy.context.active_object.data.energy = 1.5
    
    # Камера
    bpy.ops.object.camera_add(location=(0.15, -0.25, 0.15))
    cam = bpy.context.active_object
    direction = Vector((0, 0, 0.05)) - Vector(cam.location)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    
    # Render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 64


def create_hand_with_sockets(scale=None):
    """
    Создаёт кисть с шарнирными сокетами для соединения частей
    
    Каждый сустав имеет отдельные части: шарик и втулку
    """
    if scale is None:
        scale = HandSettings.HAND_SCALE
    
    mat_joint = create_material("Socket_Joint", HandSettings.JOINT_COLOR)
    mat_bone = create_material("Socket_Bone", HandSettings.BONE_COLOR)
    mat_palm = create_material("Socket_Palm", HandSettings.PALM_COLOR)
    
    objects = []
    
    # === ЛАДОНЬ С ГНЕЗДАМИ ===
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    palm = bpy.context.active_object
    palm.scale = (scale * 0.8, scale * 0.25, scale * 0.35)
    palm.name = "Palm_Body"
    palm.data.materials.append(mat_palm)
    objects.append(palm)
    
    # Гнёзда для пальцев (socket receivers)
    socket_positions = [
        ("Index", -0.16, 0.02, 0.75),
        ("Middle", 0.0, 0.0, 0.78),
        ("Ring", 0.16, 0.01, 0.75),
        ("Pinky", 0.30, 0.03, 0.68),
    ]
    
    for name, x, y, z in socket_positions:
        # Втулка-гнездо
        socket_inner = HandSettings.JOINT_RADIUS + HandSettings.JOINT_TOLERANCE
        socket_outer = socket_inner + 0.0015
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=socket_outer,
            depth=socket_outer * 2,
            location=(x * scale, y * scale, z * scale)
        )
        socket = bpy.context.active_object
        socket.name = f"{name}_Socket_Housing"
        socket.data.materials.append(mat_joint)
        objects.append(socket)
    
    # === ПАЛЬЦЫ С ШАРИКАМИ ===
    fingers_config = [
        ("Index", -0.16, 0.02, 0.75, 1.0, 3, (-3, 0)),
        ("Middle", 0.0, 0.0, 0.78, 1.15, 3, (0, 0)),
        ("Ring", 0.16, 0.01, 0.75, 1.05, 3, (3, 0)),
        ("Pinky", 0.30, 0.03, 0.68, 0.85, 3, (8, 0)),
    ]
    
    for name, x, y, z, length, segs, angles in fingers_config:
        base_pos = (x * scale, y * scale, z * scale + scale * 0.15)
        finger_objects = create_finger(
            scale, name, base_pos, length, segs,
            mat_joint, mat_bone, angles
        )
        objects.extend(finger_objects)
    
    # Большой палец
    thumb_objects = create_thumb(scale, mat_joint, mat_bone)
    # Сдвигаем вверх для раздельной печати
    for obj in thumb_objects:
        obj.location.z += scale * 0.5
    objects.extend(thumb_objects)
    
    return objects


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """Создаёт каркас кисти"""
    clear_scene()
    
    print("\n" + "="*50)
    print("  HAND ARMATURE FOR STOP-MOTION")
    print("="*50)
    
    # Выберите один из вариантов:
    
    # Вариант 1: Левая кисть
    # objects = create_left_hand()
    
    # Вариант 2: Правая кисть
    # objects = create_right_hand()
    
    # Вариант 3: Обе кисти
    objects = create_both_hands()
    
    # Вариант 4: Кисть с раздельными сокетами (для сборки)
    # objects = create_hand_with_sockets()
    
    # Объединяем в один объект
    if objects:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = objects[0]
        bpy.ops.object.join()
        
        result = bpy.context.active_object
        result.name = "Hand_Armature_Complete"
    
    setup_scene()
    
    print("\nCreated: Hand Armature")
    print("Scale: {:.0f} mm".format(HandSettings.HAND_SCALE * 1000))
    print("\nTo export: File → Export → STL")
    print("="*50)


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    main()
