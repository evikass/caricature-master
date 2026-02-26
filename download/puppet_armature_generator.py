"""
================================================================================
PUKKET ARMATURE GENERATOR FOR STOP-MOTION ANIMATION
================================================================================
Blender Python Script for generating 3D-printable puppet armatures
Optimized for SLA/DLP 3D printing

Author: AI Assistant
Version: 1.0
Blender Version: 3.0+

USAGE:
1. Open Blender
2. Go to Scripting tab
3. Open this file
4. Run script (Alt+P)
5. Check collection "Puppet_Armature" for generated parts

FEATURES:
- Ball-and-socket joints with printable tolerances
- Interchangeable bone segments
- Full humanoid armature kit
- Pre-configured for SLA printing
================================================================================
"""

import bpy
import bmesh
import math
from mathutils import Vector, Matrix
from bpy.props import FloatProperty, IntProperty, EnumProperty, BoolProperty

# ============================================================================
# CONFIGURATION - PRINT SETTINGS FOR SLA
# ============================================================================

SLA_TOLERANCE = 0.15  # mm - tolerance for moving parts
BALL_JOINT_TOLERANCE = 0.1  # mm - tighter tolerance for ball joints
MIN_WALL_THICKNESS = 0.8  # mm - minimum wall thickness for SLA
DEFAULT_SCALE = 1.0  # scale factor (1.0 = real size in mm)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def clear_scene():
    """Clear existing armature objects from scene"""
    if "Puppet_Armature" in bpy.data.collections:
        collection = bpy.data.collections["Puppet_Armature"]
        for obj in collection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(collection)


def create_collection(name="Puppet_Armature"):
    """Create or get collection for armature parts"""
    if name not in bpy.data.collections:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    else:
        collection = bpy.data.collections[name]
    return collection


def add_to_collection(obj, collection):
    """Add object to collection"""
    for coll in obj.users_collection:
        coll.objects.unlink(obj)
    collection.objects.link(obj)


def create_material(name, color):
    """Create material with specified color"""
    if name not in bpy.data.materials:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Metallic"].default_value = 0.3
        bsdf.inputs["Roughness"].default_value = 0.4
    return bpy.data.materials[name]


# ============================================================================
# BALL JOINT COMPONENTS
# ============================================================================

def create_ball_joint_head(radius=3.0, neck_radius=1.5, neck_length=4.0, name="Ball_Joint_Head"):
    """
    Create a ball joint head (ball part)
    
    Args:
        radius: Ball radius in mm
        neck_radius: Neck/stem radius in mm
        neck_length: Neck length in mm
        name: Object name
    """
    # Create ball
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
    ball = bpy.context.active_object
    ball.name = name
    
    # Add neck/cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        radius=neck_radius,
        depth=neck_length,
        location=(0, 0, radius + neck_length/2)
    )
    neck = bpy.context.active_object
    
    # Join objects
    bpy.context.view_layer.objects.active = ball
    ball.select_set(True)
    neck.select_set(True)
    bpy.ops.object.join()
    
    # Apply material
    mat = create_material("Joint_Metal", (0.7, 0.7, 0.75, 1.0))
    ball.data.materials.append(mat)
    
    return ball


def create_ball_joint_socket(
    ball_radius=3.0,
    socket_thickness=1.5,
    coverage=0.7,
    slot_width=0.8,
    name="Ball_Joint_Socket"
):
    """
    Create a ball joint socket (cup part)
    
    Args:
        ball_radius: Radius of ball it must accept
        socket_thickness: Wall thickness of socket
        coverage: How much of ball is covered (0.5-0.85)
        slot_width: Width of adjustment slot
        name: Object name
    """
    inner_radius = ball_radius + BALL_JOINT_TOLERANCE
    outer_radius = inner_radius + socket_thickness
    
    # Create outer sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=outer_radius, location=(0, 0, 0))
    socket = bpy.context.active_object
    socket.name = name
    
    # Switch to edit mode to create the socket cavity
    bpy.context.view_layer.objects.active = socket
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Create inner sphere for boolean difference
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=inner_radius,
        location=(0, 0, 0)
    )
    inner_sphere = bpy.context.active_object
    inner_sphere.name = "inner_sphere_temp"
    
    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Boolean difference
    modifier = socket.modifiers.new(name="InnerCavity", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = inner_sphere
    bpy.context.view_layer.objects.active = socket
    bpy.ops.object.modifier_apply(modifier="InnerCavity")
    
    # Delete the inner sphere
    bpy.data.objects.remove(inner_sphere, do_unlink=True)
    
    # Cut away bottom portion (create cup shape)
    bpy.ops.mesh.primitive_cube_add(
        size=outer_radius * 3,
        location=(0, 0, -outer_radius * (1 - coverage + 0.5))
    )
    cutter = bpy.context.active_object
    
    modifier = socket.modifiers.new(name="BottomCut", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = cutter
    bpy.ops.object.modifier_apply(modifier="BottomCut")
    bpy.data.objects.remove(cutter, do_unlink=True)
    
    # Add slot for tension adjustment
    bpy.ops.mesh.primitive_cube_add(
        size=slot_width,
        location=(0, 0, 0)
    )
    slot_cutter = bpy.context.active_object
    slot_cutter.scale = (1, outer_radius * 3, outer_radius * 3)
    
    modifier = socket.modifiers.new(name="SlotCut", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = slot_cutter
    bpy.ops.object.modifier_apply(modifier="SlotCut")
    bpy.data.objects.remove(slot_cutter, do_unlink=True)
    
    # Add neck mounting point
    bpy.ops.mesh.primitive_cylinder_add(
        radius=inner_radius * 0.5,
        depth=socket_thickness * 3,
        location=(0, 0, outer_radius * coverage)
    )
    neck = bpy.context.active_object
    
    bpy.context.view_layer.objects.active = socket
    socket.select_set(True)
    neck.select_set(True)
    bpy.ops.object.join()
    
    # Apply material
    mat = create_material("Joint_Metal", (0.7, 0.7, 0.75, 1.0))
    socket.data.materials.append(mat)
    
    return socket


def create_ball_joint_assembly(
    ball_radius=3.0,
    neck_length=5.0,
    name="Ball_Joint_Assembly"
):
    """Create complete ball joint assembly (head + socket)"""
    collection = create_collection("Puppet_Armature")
    
    # Create ball head
    ball = create_ball_joint_head(
        radius=ball_radius,
        neck_radius=ball_radius * 0.5,
        neck_length=neck_length,
        name=f"{name}_Head"
    )
    add_to_collection(ball, collection)
    ball.location = (-ball_radius * 3, 0, 0)
    
    # Create socket
    socket = create_ball_joint_socket(
        ball_radius=ball_radius,
        socket_thickness=ball_radius * 0.4,
        coverage=0.7,
        slot_width=0.8,
        name=f"{name}_Socket"
    )
    add_to_collection(socket, collection)
    socket.location = (ball_radius * 3, 0, 0)
    
    return ball, socket


# ============================================================================
# HINGE JOINT COMPONENTS
# ============================================================================

def create_hinge_joint(
    width=8.0,
    height=6.0,
    depth=4.0,
    hole_diameter=2.0,
    name="Hinge_Joint"
):
    """
    Create a hinge joint for elbows/knees
    
    Args:
        width: Width of hinge plates
        height: Height of hinge
        depth: Depth of hinge
        hole_diameter: Diameter of hinge pin hole
        name: Object name
    """
    collection = create_collection("Puppet_Armature")
    
    # Create fork part
    fork = create_hinge_fork(width, height, depth, hole_diameter, f"{name}_Fork")
    add_to_collection(fork, collection)
    fork.location = (-width * 1.5, 0, 0)
    
    # Create tongue part
    tongue = create_hinge_tongue(width, height, depth, hole_diameter, f"{name}_Tongue")
    add_to_collection(tongue, collection)
    tongue.location = (width * 1.5, 0, 0)
    
    # Create pin
    pin = create_hinge_pin(hole_diameter, depth * 1.2, f"{name}_Pin")
    add_to_collection(pin, collection)
    pin.location = (0, depth * 2, 0)
    
    return fork, tongue, pin


def create_hinge_fork(width, height, depth, hole_diameter, name):
    """Create fork part of hinge joint"""
    # Main body
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    fork = bpy.context.active_object
    fork.name = name
    fork.scale = (width, depth, height)
    
    # Create fork slots
    slot_width = depth * 0.4
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, depth * 0.5, 0))
    slot1 = bpy.context.active_object
    slot1.scale = (width * 1.1, slot_width, height * 0.7)
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -depth * 0.5, 0))
    slot2 = bpy.context.active_object
    slot2.scale = (width * 1.1, slot_width, height * 0.7)
    
    # Boolean subtract slots
    for slot in [slot1, slot2]:
        modifier = fork.modifiers.new(name="Slot", type='BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = slot
        bpy.context.view_layer.objects.active = fork
        bpy.ops.object.modifier_apply(modifier="Slot")
        bpy.data.objects.remove(slot, do_unlink=True)
    
    # Add hinge holes
    hole_radius = (hole_diameter + SLA_TOLERANCE) / 2
    
    for y_offset in [depth * 0.35, -depth * 0.35]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=hole_radius,
            depth=width * 2,
            location=(0, y_offset, height * 0.25)
        )
        hole = bpy.context.active_object
        hole.rotation_euler = (0, math.pi/2, 0)
        
        modifier = fork.modifiers.new(name="Hole", type='BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = hole
        bpy.context.view_layer.objects.active = fork
        bpy.ops.object.modifier_apply(modifier="Hole")
        bpy.data.objects.remove(hole, do_unlink=True)
    
    mat = create_material("Joint_Metal", (0.7, 0.7, 0.75, 1.0))
    fork.data.materials.append(mat)
    
    return fork


def create_hinge_tongue(width, height, depth, hole_diameter, name):
    """Create tongue part of hinge joint"""
    tongue_depth = depth * 0.35
    
    # Main body
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    tongue = bpy.context.active_object
    tongue.name = name
    tongue.scale = (width * 0.9, tongue_depth, height * 0.6)
    
    # Add hinge hole
    hole_radius = (hole_diameter + SLA_TOLERANCE) / 2
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=hole_radius,
        depth=width * 2,
        location=(0, 0, height * 0.15)
    )
    hole = bpy.context.active_object
    hole.rotation_euler = (0, math.pi/2, 0)
    
    modifier = tongue.modifiers.new(name="Hole", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = hole
    bpy.context.view_layer.objects.active = tongue
    bpy.ops.object.modifier_apply(modifier="Hole")
    bpy.data.objects.remove(hole, do_unlink=True)
    
    mat = create_material("Joint_Metal", (0.7, 0.7, 0.75, 1.0))
    tongue.data.materials.append(mat)
    
    return tongue


def create_hinge_pin(hole_diameter, length, name):
    """Create hinge pin"""
    pin_radius = hole_diameter / 2 - SLA_TOLERANCE * 0.5
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=pin_radius,
        depth=length,
        location=(0, 0, 0)
    )
    pin = bpy.context.active_object
    pin.name = name
    pin.rotation_euler = (0, math.pi/2, 0)
    
    # Add head
    bpy.ops.mesh.primitive_cylinder_add(
        radius=pin_radius * 1.8,
        depth=pin_radius * 2,
        location=(length/2, 0, 0)
    )
    head = bpy.context.active_object
    
    bpy.context.view_layer.objects.active = pin
    pin.select_set(True)
    head.select_set(True)
    bpy.ops.object.join()
    
    mat = create_material("Joint_Metal", (0.7, 0.7, 0.75, 1.0))
    pin.data.materials.append(mat)
    
    return pin


# ============================================================================
# BONE SEGMENTS / STRUTS
# ============================================================================

def create_bone_strut(
    length=30.0,
    end_diameter=4.0,
    mid_diameter=3.0,
    wire_hole=1.5,
    name="Bone_Strut"
):
    """
    Create a bone segment with wire channel
    
    Args:
        length: Total length in mm
        end_diameter: Diameter at ends
        mid_diameter: Diameter at middle (tapered)
        wire_hole: Diameter of wire channel
        name: Object name
    """
    collection = create_collection("Puppet_Armature")
    
    # Create main bone shape using subdivision
    bpy.ops.mesh.primitive_cylinder_add(
        radius=end_diameter/2,
        depth=length,
        location=(0, 0, 0)
    )
    bone = bpy.context.active_object
    bone.name = name
    
    # Add wire hole through center
    hole_radius = wire_hole / 2 + SLA_TOLERANCE
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=hole_radius,
        depth=length * 1.2,
        location=(0, 0, 0)
    )
    hole = bpy.context.active_object
    
    modifier = bone.modifiers.new(name="WireHole", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = hole
    bpy.context.view_layer.objects.active = bone
    bpy.ops.object.modifier_apply(modifier="WireHole")
    bpy.data.objects.remove(hole, do_unlink=True)
    
    # Add flutes for weight reduction (optional aesthetic)
    bone = add_bone_flutes(bone, num_flutes=6, depth=0.3)
    
    mat = create_material("Bone_Material", (0.6, 0.55, 0.5, 1.0))
    bone.data.materials.append(mat)
    
    add_to_collection(bone, collection)
    
    return bone


def add_bone_flutes(obj, num_flutes=6, depth=0.3):
    """Add decorative flutes to bone segment"""
    radius = obj.dimensions.x / 2
    
    for i in range(num_flutes):
        angle = (2 * math.pi * i) / num_flutes
        x = math.cos(angle) * (radius - depth/2)
        y = math.sin(angle) * (radius - depth/2)
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=depth,
            depth=obj.dimensions.z * 1.1,
            location=(x, y, 0)
        )
        flute = bpy.context.active_object
        
        modifier = obj.modifiers.new(name=f"Flute_{i}", type='BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = flute
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=f"Flute_{i}")
        bpy.data.objects.remove(flute, do_unlink=True)
    
    return obj


def create_tapered_strut(
    length=25.0,
    start_diameter=5.0,
    end_diameter=3.0,
    wire_hole=1.2,
    name="Tapered_Strut"
):
    """Create a tapered strut for fingers/toes"""
    collection = create_collection("Puppet_Armature")
    
    # Create cone-like shape
    segments = 8
    verts = []
    faces = []
    
    for i in range(segments + 1):
        t = i / segments
        z = t * length
        radius = start_diameter/2 + (end_diameter/2 - start_diameter/2) * t
        radius -= wire_hole/2  # Account for wire channel
        
        # Create ring of vertices
        for j in range(12):
            angle = (2 * math.pi * j) / 12
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            verts.append((x, y, z - length/2))
    
    # Create faces (simplified)
    mesh = bpy.data.meshes.new(f"{name}_mesh")
    mesh.from_pydata(verts, [], [])
    
    obj = bpy.object.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    mat = create_material("Bone_Material", (0.6, 0.55, 0.5, 1.0))
    obj.data.materials.append(mat)
    
    add_to_collection(obj, collection)
    
    return obj


# ============================================================================
# FOOT AND HAND PLATES
# ============================================================================

def create_foot_plate(
    length=25.0,
    width=12.0,
    thickness=2.0,
    tie_holes=3,
    hole_diameter=2.0,
    name="Foot_Plate"
):
    """
    Create foot plate with tie-down holes
    
    Args:
        length: Length in mm
        width: Width in mm
        thickness: Plate thickness
        tie_holes: Number of tie-down holes
        hole_diameter: Hole diameter
        name: Object name
    """
    collection = create_collection("Puppet_Armature")
    
    # Create main plate
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    plate = bpy.context.active_object
    plate.name = name
    plate.scale = (length, width, thickness)
    
    # Add rounded ends
    bpy.ops.mesh.primitive_cylinder_add(
        radius=width/2,
        depth=thickness,
        location=(length/2, 0, 0)
    )
    end1 = bpy.context.active_object
    end1.rotation_euler = (math.pi/2, 0, 0)
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=width/2,
        depth=thickness,
        location=(-length/2, 0, 0)
    )
    end2 = bpy.context.active_object
    end2.rotation_euler = (math.pi/2, 0, 0)
    
    # Join all parts
    bpy.context.view_layer.objects.active = plate
    plate.select_set(True)
    end1.select_set(True)
    end2.select_set(True)
    bpy.ops.object.join()
    
    # Add tie-down holes
    hole_spacing = length / (tie_holes + 1)
    
    for i in range(tie_holes):
        x_pos = -length/2 + hole_spacing * (i + 1)
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=hole_diameter/2 + SLA_TOLERANCE,
            depth=thickness * 2,
            location=(x_pos, 0, 0)
        )
        hole = bpy.context.active_object
        hole.rotation_euler = (math.pi/2, 0, 0)
        
        modifier = plate.modifiers.new(name=f"Hole_{i}", type='BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = hole
        bpy.context.view_layer.objects.active = plate
        bpy.ops.object.modifier_apply(modifier=f"Hole_{i}")
        bpy.data.objects.remove(hole, do_unlink=True)
    
    mat = create_material("Plate_Material", (0.5, 0.5, 0.55, 1.0))
    plate.data.materials.append(mat)
    
    add_to_collection(plate, collection)
    
    return plate


def create_hand_plate(
    width=15.0,
    height=10.0,
    thickness=1.5,
    finger_slots=4,
    name="Hand_Plate"
):
    """Create hand plate with finger mounting points"""
    collection = create_collection("Puppet_Armature")
    
    # Create palm base
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    hand = bpy.context.active_object
    hand.name = name
    hand.scale = (width, height, thickness)
    
    # Add finger mounting points
    finger_spacing = width / (finger_slots + 1)
    
    for i in range(finger_slots):
        x_pos = -width/2 + finger_spacing * (i + 1)
        
        # Ball joint mount for finger
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=thickness * 1.2,
            location=(x_pos, height/2 + thickness, 0)
        )
        mount = bpy.context.active_object
        
        bpy.context.view_layer.objects.active = hand
        hand.select_set(True)
        mount.select_set(True)
        bpy.ops.object.join()
    
    mat = create_material("Plate_Material", (0.5, 0.5, 0.55, 1.0))
    hand.data.materials.append(mat)
    
    add_to_collection(hand, collection)
    
    return hand


# ============================================================================
# COMPLETE HUMANOID ARMATURE
# ============================================================================

def create_humanoid_armature(scale=1.0, name="Humanoid_Armature"):
    """
    Create complete humanoid puppet armature kit
    
    Args:
        scale: Scale factor (1.0 = ~200mm height)
        name: Base name for parts
    """
    collection = create_collection("Puppet_Armature")
    
    # Create sub-collection for this armature
    armature_name = f"{name}_Kit"
    if armature_name not in bpy.data.collections:
        sub_coll = bpy.data.collections.new(armature_name)
        collection.children.link(sub_coll)
    else:
        sub_coll = bpy.data.collections[armature_name]
    
    parts_created = []
    
    # Scale factors
    s = scale
    
    # ----- HEAD JOINT (large ball joint) -----
    head_ball, head_socket = create_ball_joint_assembly(
        ball_radius=4.0 * s,
        neck_length=8.0 * s,
        name=f"{name}_Head"
    )
    add_to_collection(head_ball, sub_coll)
    add_to_collection(head_socket, sub_coll)
    head_ball.location = (-20 * s, 40 * s, 0)
    head_socket.location = (20 * s, 40 * s, 0)
    parts_created.append("Head Joint")
    
    # ----- NECK/SPINE BONE -----
    spine = create_bone_strut(
        length=25.0 * s,
        end_diameter=5.0 * s,
        mid_diameter=4.0 * s,
        wire_hole=1.5 * s,
        name=f"{name}_Spine"
    )
    add_to_collection(spine, sub_coll)
    spine.location = (0, 20 * s, 0)
    parts_created.append("Spine Segment")
    
    # ----- SHOULDER JOINTS -----
    for side in ["L", "R"]:
        shoulder_ball, shoulder_socket = create_ball_joint_assembly(
            ball_radius=3.5 * s,
            neck_length=6.0 * s,
            name=f"{name}_Shoulder_{side}"
        )
        add_to_collection(shoulder_ball, sub_coll)
        add_to_collection(shoulder_socket, sub_coll)
        
        x_offset = 35 * s if side == "L" else 35 * s
        shoulder_ball.location = (-x_offset, 20 * s, 0)
        shoulder_socket.location = (x_offset + 15 * s, 20 * s, 0)
    parts_created.append("Shoulder Joints (x2)")
    
    # ----- UPPER ARM BONES -----
    for side in ["L", "R"]:
        arm = create_bone_strut(
            length=30.0 * s,
            end_diameter=4.0 * s,
            mid_diameter=3.0 * s,
            wire_hole=1.2 * s,
            name=f"{name}_UpperArm_{side}"
        )
        add_to_collection(arm, sub_coll)
        x_offset = 50 * s if side == "L" else -50 * s
        arm.location = (x_offset, 0, 0)
        arm.rotation_euler = (0, 0, math.pi/2 if side == "L" else -math.pi/2)
    parts_created.append("Upper Arm Bones (x2)")
    
    # ----- ELBOW HINGES -----
    for side in ["L", "R"]:
        fork, tongue, pin = create_hinge_joint(
            width=6.0 * s,
            height=5.0 * s,
            depth=4.0 * s,
            hole_diameter=1.5 * s,
            name=f"{name}_Elbow_{side}"
        )
        add_to_collection(fork, sub_coll)
        add_to_collection(tongue, sub_coll)
        add_to_collection(pin, sub_coll)
        
        x_base = 65 * s if side == "L" else -65 * s
        fork.location = (x_base, -20 * s, 0)
        tongue.location = (x_base + 15 * s, -20 * s, 0)
        pin.location = (x_base + 7.5 * s, -25 * s, 0)
    parts_created.append("Elbow Hinges (x2)")
    
    # ----- FOREARM BONES -----
    for side in ["L", "R"]:
        forearm = create_bone_strut(
            length=25.0 * s,
            end_diameter=3.5 * s,
            mid_diameter=2.5 * s,
            wire_hole=1.0 * s,
            name=f"{name}_Forearm_{side}"
        )
        add_to_collection(forearm, sub_coll)
        x_offset = 80 * s if side == "L" else -80 * s
        forearm.location = (x_offset, -20 * s, 0)
        forearm.rotation_euler = (0, 0, math.pi/2 if side == "L" else -math.pi/2)
    parts_created.append("Forearm Bones (x2)")
    
    # ----- WRIST JOINTS -----
    for side in ["L", "R"]:
        wrist_ball, wrist_socket = create_ball_joint_assembly(
            ball_radius=2.5 * s,
            neck_length=4.0 * s,
            name=f"{name}_Wrist_{side}"
        )
        add_to_collection(wrist_ball, sub_coll)
        add_to_collection(wrist_socket, sub_coll)
        
        x_offset = 95 * s if side == "L" else -95 * s
        wrist_ball.location = (x_offset, -40 * s, 0)
        wrist_socket.location = (x_offset + 10 * s, -40 * s, 0)
    parts_created.append("Wrist Joints (x2)")
    
    # ----- HIP JOINTS -----
    for side in ["L", "R"]:
        hip_ball, hip_socket = create_ball_joint_assembly(
            ball_radius=4.0 * s,
            neck_length=8.0 * s,
            name=f"{name}_Hip_{side}"
        )
        add_to_collection(hip_ball, sub_coll)
        add_to_collection(hip_socket, sub_coll)
        
        x_offset = 15 * s if side == "L" else -15 * s
        hip_ball.location = (-x_offset, -40 * s, 0)
        hip_socket.location = (x_offset + 10 * s, -40 * s, 0)
    parts_created.append("Hip Joints (x2)")
    
    # ----- THIGH BONES -----
    for side in ["L", "R"]:
        thigh = create_bone_strut(
            length=35.0 * s,
            end_diameter=5.0 * s,
            mid_diameter=4.0 * s,
            wire_hole=1.5 * s,
            name=f"{name}_Thigh_{side}"
        )
        add_to_collection(thigh, sub_coll)
        x_offset = 30 * s if side == "L" else -30 * s
        thigh.location = (x_offset, -60 * s, 0)
    parts_created.append("Thigh Bones (x2)")
    
    # ----- KNEE HINGES -----
    for side in ["L", "R"]:
        fork, tongue, pin = create_hinge_joint(
            width=7.0 * s,
            height=6.0 * s,
            depth=5.0 * s,
            hole_diameter=2.0 * s,
            name=f"{name}_Knee_{side}"
        )
        add_to_collection(fork, sub_coll)
        add_to_collection(tongue, sub_coll)
        add_to_collection(pin, sub_coll)
        
        x_base = 30 * s if side == "L" else -30 * s
        fork.location = (x_base, -85 * s, 0)
        tongue.location = (x_base + 18 * s, -85 * s, 0)
        pin.location = (x_base + 9 * s, -90 * s, 0)
    parts_created.append("Knee Hinges (x2)")
    
    # ----- SHIN BONES -----
    for side in ["L", "R"]:
        shin = create_bone_strut(
            length=30.0 * s,
            end_diameter=4.0 * s,
            mid_diameter=3.0 * s,
            wire_hole=1.2 * s,
            name=f"{name}_Shin_{side}"
        )
        add_to_collection(shin, sub_coll)
        x_offset = 30 * s if side == "L" else -30 * s
        shin.location = (x_offset, -110 * s, 0)
    parts_created.append("Shin Bones (x2)")
    
    # ----- ANKLE JOINTS -----
    for side in ["L", "R"]:
        ankle_ball, ankle_socket = create_ball_joint_assembly(
            ball_radius=3.0 * s,
            neck_length=5.0 * s,
            name=f"{name}_Ankle_{side}"
        )
        add_to_collection(ankle_ball, sub_coll)
        add_to_collection(ankle_socket, sub_coll)
        
        x_offset = 30 * s if side == "L" else -30 * s
        ankle_ball.location = (x_offset, -135 * s, 0)
        ankle_socket.location = (x_offset + 10 * s, -135 * s, 0)
    parts_created.append("Ankle Joints (x2)")
    
    # ----- FOOT PLATES -----
    for side in ["L", "R"]:
        foot = create_foot_plate(
            length=20.0 * s,
            width=10.0 * s,
            thickness=2.0 * s,
            tie_holes=2,
            hole_diameter=2.0 * s,
            name=f"{name}_Foot_{side}"
        )
        add_to_collection(foot, sub_coll)
        
        x_offset = 30 * s if side == "L" else -30 * s
        foot.location = (x_offset, -155 * s, 0)
    parts_created.append("Foot Plates (x2)")
    
    # ----- HAND PLATES -----
    for side in ["L", "R"]:
        hand = create_hand_plate(
            width=12.0 * s,
            height=8.0 * s,
            thickness=1.5 * s,
            finger_slots=4,
            name=f"{name}_Hand_{side}"
        )
        add_to_collection(hand, sub_coll)
        
        x_offset = 110 * s if side == "L" else -110 * s
        hand.location = (x_offset, -60 * s, 0)
    parts_created.append("Hand Plates (x2)")
    
    # ----- FINGER STRUTS (small) -----
    for i in range(8):  # 4 per hand
        finger = create_bone_strut(
            length=12.0 * s,
            end_diameter=2.0 * s,
            mid_diameter=1.5 * s,
            wire_hole=0.8 * s,
            name=f"{name}_Finger_{i}"
        )
        add_to_collection(finger, sub_coll)
        
        row = i // 4
        col = i % 4
        finger.location = (120 * s + col * 8 * s, -80 * s - row * 10 * s, 0)
    parts_created.append("Finger Struts (x8)")
    
    return parts_created


# ============================================================================
# SIMPLE QUADRUPED ARMATURE (for animal puppets)
# ============================================================================

def create_quadruped_armature(scale=1.0, name="Quadruped_Armature"):
    """Create quadruped (four-legged) armature kit"""
    collection = create_collection("Puppet_Armature")
    
    armature_name = f"{name}_Kit"
    if armature_name not in bpy.data.collections:
        sub_coll = bpy.data.collections.new(armature_name)
        collection.children.link(sub_coll)
    else:
        sub_coll = bpy.data.collections[armature_name]
    
    parts_created = []
    s = scale
    
    # Spine segments
    for i in range(3):
        spine = create_bone_strut(
            length=20.0 * s,
            end_diameter=4.0 * s,
            mid_diameter=3.5 * s,
            wire_hole=1.2 * s,
            name=f"{name}_Spine_{i}"
        )
        add_to_collection(spine, sub_coll)
        spine.location = (i * 30 * s - 30 * s, 30 * s, 0)
    parts_created.append("Spine Segments (x3)")
    
    # Legs (4 total)
    leg_positions = [
        ("FL", -40 * s, 0),  # Front Left
        ("FR", -40 * s, -20 * s),  # Front Right
        ("BL", 40 * s, 0),  # Back Left
        ("BR", 40 * s, -20 * s),  # Back Right
    ]
    
    for leg_name, x, y in leg_positions:
        # Hip/Shoulder joint
        ball, socket = create_ball_joint_assembly(
            ball_radius=3.0 * s,
            neck_length=5.0 * s,
            name=f"{name}_LegJoint_{leg_name}"
        )
        add_to_collection(ball, sub_coll)
        add_to_collection(socket, sub_coll)
        ball.location = (x - 10 * s, y, 0)
        socket.location = (x + 10 * s, y, 0)
        
        # Upper leg
        upper = create_bone_strut(
            length=20.0 * s,
            end_diameter=3.5 * s,
            mid_diameter=2.8 * s,
            wire_hole=1.0 * s,
            name=f"{name}_UpperLeg_{leg_name}"
        )
        add_to_collection(upper, sub_coll)
        upper.location = (x, y - 25 * s, 0)
        
        # Lower leg
        lower = create_bone_strut(
            length=18.0 * s,
            end_diameter=3.0 * s,
            mid_diameter=2.5 * s,
            wire_hole=1.0 * s,
            name=f"{name}_LowerLeg_{leg_name}"
        )
        add_to_collection(lower, sub_coll)
        lower.location = (x, y - 50 * s, 0)
        
        # Paw
        paw = create_foot_plate(
            length=12.0 * s,
            width=8.0 * s,
            thickness=1.5 * s,
            tie_holes=1,
            hole_diameter=1.5 * s,
            name=f"{name}_Paw_{leg_name}"
        )
        add_to_collection(paw, sub_coll)
        paw.location = (x, y - 65 * s, 0)
    
    parts_created.append("Leg Sets (x4)")
    
    # Head joint
    head_ball, head_socket = create_ball_joint_assembly(
        ball_radius=3.5 * s,
        neck_length=6.0 * s,
        name=f"{name}_Head"
    )
    add_to_collection(head_ball, sub_coll)
    add_to_collection(head_socket, sub_coll)
    head_ball.location = (-70 * s, 30 * s, 0)
    head_socket.location = (-50 * s, 30 * s, 0)
    parts_created.append("Head Joint")
    
    # Tail bones
    for i in range(3):
        tail = create_bone_strut(
            length=15.0 * s - i * 3 * s,
            end_diameter=2.5 * s - i * 0.3 * s,
            mid_diameter=2.0 * s - i * 0.3 * s,
            wire_hole=0.8 * s,
            name=f"{name}_Tail_{i}"
        )
        add_to_collection(tail, sub_coll)
        tail.location = (60 * s + i * 18 * s, 30 * s, 0)
    parts_created.append("Tail Segments (x3)")
    
    return parts_created


# ============================================================================
# WIRE ARMATURE SYSTEM (simple wire-based)
# ============================================================================

def create_wire_armature_kit(scale=1.0, name="Wire_Armature"):
    """
    Create wire-based armature components
    These are holders/guides for twisted wire armatures
    """
    collection = create_collection("Puppet_Armature")
    
    armature_name = f"{name}_Kit"
    if armature_name not in bpy.data.collections:
        sub_coll = bpy.data.collections.new(armature_name)
        collection.children.link(sub_coll)
    else:
        sub_coll = bpy.data.collections[armature_name]
    
    parts_created = []
    s = scale
    
    # Wire holders with epoxy cavities
    # Create a generic wire holder
    def create_wire_holder(length, width, wire_count, name):
        # Main body
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        holder = bpy.context.active_object
        holder.name = name
        holder.scale = (length, width, width * 0.8)
        
        # Create wire channels
        wire_spacing = width / (wire_count + 1)
        for i in range(wire_count):
            y_pos = -width/2 + wire_spacing * (i + 1)
            
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.6 * s,
                depth=length * 1.2,
                location=(0, y_pos, 0)
            )
            hole = bpy.context.active_object
            hole.rotation_euler = (0, math.pi/2, 0)
            
            modifier = holder.modifiers.new(name=f"Wire_{i}", type='BOOLEAN')
            modifier.operation = 'DIFFERENCE'
            modifier.object = hole
            bpy.context.view_layer.objects.active = holder
            bpy.ops.object.modifier_apply(modifier=f"Wire_{i}")
            bpy.data.objects.remove(hole, do_unlink=True)
        
        # Create epoxy cavity (larger central hole)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=width * 0.25,
            depth=length * 0.8,
            location=(0, 0, 0)
        )
        cavity = bpy.context.active_object
        cavity.rotation_euler = (0, math.pi/2, 0)
        
        modifier = holder.modifiers.new(name="Epoxy_Cavity", type='BOOLEAN')
        modifier.operation = 'DIFFERENCE'
        modifier.object = cavity
        bpy.context.view_layer.objects.active = holder
        bpy.ops.object.modifier_apply(modifier="Epoxy_Cavity")
        bpy.data.objects.remove(cavity, do_unlink=True)
        
        return holder
    
    # Spine holder
    spine_holder = create_wire_holder(20 * s, 8 * s, 4, f"{name}_Spine_Holder")
    add_to_collection(spine_holder, sub_coll)
    spine_holder.location = (0, 0, 0)
    parts_created.append("Spine Wire Holder")
    
    # Leg holders
    for side in ["L", "R"]:
        leg_holder = create_wire_holder(15 * s, 6 * s, 3, f"{name}_Leg_Holder_{side}")
        add_to_collection(leg_holder, sub_coll)
        x_offset = 30 * s if side == "L" else -30 * s
        leg_holder.location = (x_offset, -20 * s, 0)
    parts_created.append("Leg Wire Holders (x2)")
    
    # Arm holders
    for side in ["L", "R"]:
        arm_holder = create_wire_holder(12 * s, 5 * s, 2, f"{name}_Arm_Holder_{side}")
        add_to_collection(arm_holder, sub_coll)
        x_offset = 50 * s if side == "L" else -50 * s
        arm_holder.location = (x_offset, 20 * s, 0)
    parts_created.append("Arm Wire Holders (x2)")
    
    # Neck holder
    neck_holder = create_wire_holder(10 * s, 4 * s, 2, f"{name}_Neck_Holder")
    add_to_collection(neck_holder, sub_coll)
    neck_holder.location = (0, 40 * s, 0)
    parts_created.append("Neck Wire Holder")
    
    # Apply materials
    mat = create_material("Wire_Holder_Material", (0.4, 0.35, 0.3, 1.0))
    for obj in sub_coll.objects:
        if len(obj.data.materials) == 0:
            obj.data.materials.append(mat)
    
    return parts_created


# ============================================================================
# MAIN EXECUTION
# ============================================================================

class ArmatureGeneratorPanel(bpy.types.Panel):
    """Panel for Puppet Armature Generator"""
    bl_label = "Puppet Armature Generator"
    bl_idname = "VIEW3D_PT_puppet_armature"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Puppet Tools'
    
    def draw(self, context):
        layout = self.layout
        
        # Humanoid armature
        box = layout.box()
        box.label(text="Humanoid Armature", icon='ARMATURE_DATA')
        row = box.row()
        row.operator("object.generate_humanoid", text="Generate Kit")
        
        # Quadruped armature
        box = layout.box()
        box.label(text="Quadruped Armature", icon='ARMATURE_DATA')
        row = box.row()
        row.operator("object.generate_quadruped", text="Generate Kit")
        
        # Wire armature
        box = layout.box()
        box.label(text="Wire Armature System", icon='MESH_CYLINDER')
        row = box.row()
        row.operator("object.generate_wire", text="Generate Kit")
        
        # Individual components
        box = layout.box()
        box.label(text="Individual Components", icon='MESH_CUBE')
        row = box.row()
        row.operator("object.generate_ball_joint", text="Ball Joint")
        row = box.row()
        row.operator("object.generate_hinge", text="Hinge Joint")
        row = box.row()
        row.operator("object.generate_bone", text="Bone Strut")
        row = box.row()
        row.operator("object.generate_foot", text="Foot Plate")
        
        # Clear button
        layout.separator()
        layout.operator("object.clear_armatures", text="Clear All Armatures", icon='X')


class GenerateHumanoidOperator(bpy.types.Operator):
    """Generate complete humanoid armature kit"""
    bl_idname = "object.generate_humanoid"
    bl_label = "Generate Humanoid Armature"
    
    def execute(self, context):
        parts = create_humanoid_armature(scale=1.0, name="Humanoid")
        self.report({'INFO'}, f"Created {len(parts)} component types")
        return {'FINISHED'}


class GenerateQuadrupedOperator(bpy.types.Operator):
    """Generate complete quadruped armature kit"""
    bl_idname = "object.generate_quadruped"
    bl_label = "Generate Quadruped Armature"
    
    def execute(self, context):
        parts = create_quadruped_armature(scale=1.0, name="Quadruped")
        self.report({'INFO'}, f"Created {len(parts)} component types")
        return {'FINISHED'}


class GenerateWireOperator(bpy.types.Operator):
    """Generate wire armature kit"""
    bl_idname = "object.generate_wire"
    bl_label = "Generate Wire Armature"
    
    def execute(self, context):
        parts = create_wire_armature_kit(scale=1.0, name="Wire")
        self.report({'INFO'}, f"Created {len(parts)} component types")
        return {'FINISHED'}


class GenerateBallJointOperator(bpy.types.Operator):
    """Generate single ball joint assembly"""
    bl_idname = "object.generate_ball_joint"
    bl_label = "Generate Ball Joint"
    
    def execute(self, context):
        ball, socket = create_ball_joint_assembly(ball_radius=3.0, neck_length=5.0, name="Ball_Joint")
        self.report({'INFO'}, "Created ball joint assembly")
        return {'FINISHED'}


class GenerateHingeOperator(bpy.types.Operator):
    """Generate single hinge joint"""
    bl_idname = "object.generate_hinge"
    bl_label = "Generate Hinge Joint"
    
    def execute(self, context):
        fork, tongue, pin = create_hinge_joint(name="Hinge_Joint")
        self.report({'INFO'}, "Created hinge joint")
        return {'FINISHED'}


class GenerateBoneOperator(bpy.types.Operator):
    """Generate bone strut"""
    bl_idname = "object.generate_bone"
    bl_label = "Generate Bone Strut"
    
    def execute(self, context):
        bone = create_bone_strut(length=25.0, name="Bone_Strut")
        self.report({'INFO'}, "Created bone strut")
        return {'FINISHED'}


class GenerateFootOperator(bpy.types.Operator):
    """Generate foot plate"""
    bl_idname = "object.generate_foot"
    bl_label = "Generate Foot Plate"
    
    def execute(self, context):
        foot = create_foot_plate(name="Foot_Plate")
        self.report({'INFO'}, "Created foot plate")
        return {'FINISHED'}


class ClearArmaturesOperator(bpy.types.Operator):
    """Clear all generated armature parts"""
    bl_idname = "object.clear_armatures"
    bl_label = "Clear All Armatures"
    
    def execute(self, context):
        clear_scene()
        self.report({'INFO'}, "Cleared all armature parts")
        return {'FINISHED'}


# Register classes
classes = [
    ArmatureGeneratorPanel,
    GenerateHumanoidOperator,
    GenerateQuadrupedOperator,
    GenerateWireOperator,
    GenerateBallJointOperator,
    GenerateHingeOperator,
    GenerateBoneOperator,
    GenerateFootOperator,
    ClearArmaturesOperator,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    # When run as script, generate default humanoid armature
    register()
    
    print("\n" + "="*70)
    print("PUPPET ARMATURE GENERATOR - Starting generation...")
    print("="*70)
    
    # Generate humanoid armature by default
    parts = create_humanoid_armature(scale=1.0, name="Humanoid")
    
    print("\nGenerated components:")
    for part in parts:
        print(f"  ✓ {part}")
    
    print("\n" + "="*70)
    print("Generation complete! Check 'Puppet_Armature' collection.")
    print("="*70)
    print("""
    TIPS FOR SLA PRINTING:
    ----------------------
    1. Orient parts to minimize supports on joint surfaces
    2. Use 0.025-0.05mm layer height for best detail
    3. Hollow parts with 1.5mm min wall thickness to save resin
    4. Add drainage holes to hollow parts
    5. Clean parts thoroughly before curing
    6. Test fit joints - sand if needed for smooth motion
    
    ASSEMBLY:
    ---------
    1. Clean and cure all printed parts
    2. Test fit ball joints - adjust with sandpaper if needed
    3. Use Loctite or thread locker on hinge pins
    4. Thread armature wire through bone channels
    5. Secure joints with epoxy or set screws
    
    PANEL ACCESS:
    -------------
    View 3D > Sidebar (N) > Puppet Tools
    """)
