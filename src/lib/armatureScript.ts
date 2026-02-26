// Armature Script Generator for Blender
// Generates Python scripts for puppet armature creation

export interface ArmatureConfig {
  scaleFactor: number;        // 0.5 - 2.0
  ballJointRadius: number;    // 2.0 - 5.0 mm
  socketGap: number;          // 0.1 - 0.3 mm
  boneDiameter: number;       // 2.0 - 4.0 mm
  armatureType: 'humanoid' | 'simple' | 'animal';
}

export const defaultConfig: ArmatureConfig = {
  scaleFactor: 1.0,
  ballJointRadius: 3.0,
  socketGap: 0.2,
  boneDiameter: 3.0,
  armatureType: 'humanoid',
};

// Generate Blender Python script based on configuration
export function generateBlenderArmatureScript(config: ArmatureConfig): string {
  const { scaleFactor, ballJointRadius, socketGap, boneDiameter, armatureType } = config;
  
  // Calculate derived values
  const socketInnerRadius = ballJointRadius + socketGap;
  const socketOuterRadius = socketInnerRadius + 1.0; // 1mm wall thickness
  const scale = scaleFactor;

  // Armature-specific bone definitions
  const getArmatureBones = () => {
    switch (armatureType) {
      case 'humanoid':
        return `
# Humanoid armature proportions (based on standard puppet anatomy)
BASE_HEIGHT = 200 * ${scale}

# Joint positions
HEAD_POS = (0, 0, BASE_HEIGHT * 0.9)
NECK_POS = (0, 0, BASE_HEIGHT * 0.78)
CHEST_POS = (0, 0, BASE_HEIGHT * 0.65)
PELVIS_POS = (0, 0, BASE_HEIGHT * 0.45)

# Shoulder positions
SHOULDER_WIDTH = 35 * ${scale}
LEFT_SHOULDER = (-SHOULDER_WIDTH/2, 0, BASE_HEIGHT * 0.72)
RIGHT_SHOULDER = (SHOULDER_WIDTH/2, 0, BASE_HEIGHT * 0.72)

# Arm positions
LEFT_ELBOW = (-SHOULDER_WIDTH/2 - 5*${scale}, 0, BASE_HEIGHT * 0.55)
RIGHT_ELBOW = (SHOULDER_WIDTH/2 + 5*${scale}, 0, BASE_HEIGHT * 0.55)
LEFT_WRIST = (-SHOULDER_WIDTH/2 - 8*${scale}, 0, BASE_HEIGHT * 0.38)
RIGHT_WRIST = (SHOULDER_WIDTH/2 + 8*${scale}, 0, BASE_HEIGHT * 0.38)

# Leg positions
HIP_WIDTH = 20 * ${scale}
LEFT_HIP = (-HIP_WIDTH/2, 0, BASE_HEIGHT * 0.42)
RIGHT_HIP = (HIP_WIDTH/2, 0, BASE_HEIGHT * 0.42)
LEFT_KNEE = (-HIP_WIDTH/2, 0, BASE_HEIGHT * 0.25)
RIGHT_KNEE = (HIP_WIDTH/2, 0, BASE_HEIGHT * 0.25)
LEFT_ANKLE = (-HIP_WIDTH/2, 0, BASE_HEIGHT * 0.08)
RIGHT_ANKLE = (HIP_WIDTH/2, 0, BASE_HEIGHT * 0.08)`;
      
      case 'simple':
        return `
# Simple armature - basic stick figure proportions
BASE_HEIGHT = 150 * ${scale}

# Joint positions
HEAD_POS = (0, 0, BASE_HEIGHT * 0.92)
NECK_POS = (0, 0, BASE_HEIGHT * 0.80)
PELVIS_POS = (0, 0, BASE_HEIGHT * 0.45)

# Shoulder positions
SHOULDER_WIDTH = 30 * ${scale}
LEFT_SHOULDER = (-SHOULDER_WIDTH/2, 0, BASE_HEIGHT * 0.75)
RIGHT_SHOULDER = (SHOULDER_WIDTH/2, 0, BASE_HEIGHT * 0.75)

# Arm positions (simpler)
LEFT_ELBOW = (-SHOULDER_WIDTH/2, 0, BASE_HEIGHT * 0.55)
RIGHT_ELBOW = (SHOULDER_WIDTH/2, 0, BASE_HEIGHT * 0.55)
LEFT_WRIST = (-SHOULDER_WIDTH/2, 0, BASE_HEIGHT * 0.35)
RIGHT_WRIST = (SHOULDER_WIDTH/2, 0, BASE_HEIGHT * 0.35)

# Leg positions
HIP_WIDTH = 15 * ${scale}
LEFT_HIP = (-HIP_WIDTH/2, 0, BASE_HEIGHT * 0.42)
RIGHT_HIP = (HIP_WIDTH/2, 0, BASE_HEIGHT * 0.42)
LEFT_ANKLE = (-HIP_WIDTH/2, 0, BASE_HEIGHT * 0.08)
RIGHT_ANKLE = (HIP_WIDTH/2, 0, BASE_HEIGHT * 0.08)`;

      case 'animal':
        return `
# Animal (quadruped) armature proportions
BASE_HEIGHT = 100 * ${scale}
BODY_LENGTH = 200 * ${scale}

# Head and neck
HEAD_POS = (BODY_LENGTH * 0.4, 0, BASE_HEIGHT * 0.7)
NECK_BASE = (BODY_LENGTH * 0.3, 0, BASE_HEIGHT * 0.6)

# Spine/Body
SPINE_FRONT = (BODY_LENGTH * 0.25, 0, BASE_HEIGHT * 0.55)
SPINE_MID = (0, 0, BASE_HEIGHT * 0.5)
SPINE_REAR = (-BODY_LENGTH * 0.25, 0, BASE_HEIGHT * 0.55)
TAIL_BASE = (-BODY_LENGTH * 0.35, 0, BASE_HEIGHT * 0.5)
TAIL_TIP = (-BODY_LENGTH * 0.5, 0, BASE_HEIGHT * 0.45)

# Front legs
FRONT_LEG_SPREAD = 20 * ${scale}
LEFT_FRONT_SHOULDER = (BODY_LENGTH * 0.2, -FRONT_LEG_SPREAD/2, BASE_HEIGHT * 0.5)
RIGHT_FRONT_SHOULDER = (BODY_LENGTH * 0.2, FRONT_LEG_SPREAD/2, BASE_HEIGHT * 0.5)
LEFT_FRONT_ELBOW = (BODY_LENGTH * 0.2, -FRONT_LEG_SPREAD/2, BASE_HEIGHT * 0.3)
RIGHT_FRONT_ELBOW = (BODY_LENGTH * 0.2, FRONT_LEG_SPREAD/2, BASE_HEIGHT * 0.3)
LEFT_FRONT_FOOT = (BODY_LENGTH * 0.22, -FRONT_LEG_SPREAD/2, BASE_HEIGHT * 0.05)
RIGHT_FRONT_FOOT = (BODY_LENGTH * 0.22, FRONT_LEG_SPREAD/2, BASE_HEIGHT * 0.05)

# Rear legs
REAR_LEG_SPREAD = 22 * ${scale}
LEFT_REAR_HIP = (-BODY_LENGTH * 0.2, -REAR_LEG_SPREAD/2, BASE_HEIGHT * 0.5)
RIGHT_REAR_HIP = (-BODY_LENGTH * 0.2, REAR_LEG_SPREAD/2, BASE_HEIGHT * 0.5)
LEFT_REAR_KNEE = (-BODY_LENGTH * 0.22, -REAR_LEG_SPREAD/2, BASE_HEIGHT * 0.35)
RIGHT_REAR_KNEE = (-BODY_LENGTH * 0.22, REAR_LEG_SPREAD/2, BASE_HEIGHT * 0.35)
LEFT_REAR_FOOT = (-BODY_LENGTH * 0.2, -REAR_LEG_SPREAD/2, BASE_HEIGHT * 0.05)
RIGHT_REAR_FOOT = (-BODY_LENGTH * 0.2, REAR_LEG_SPREAD/2, BASE_HEIGHT * 0.05)`;
    }
  };

  // Get bone connections based on armature type
  const getBoneConnections = () => {
    switch (armatureType) {
      case 'humanoid':
        return `
    # Spine
    ("spine_upper", HEAD_POS, NECK_POS),
    ("spine_mid", NECK_POS, CHEST_POS),
    ("spine_lower", CHEST_POS, PELVIS_POS),
    
    # Shoulder bridge
    ("shoulder_bridge", LEFT_SHOULDER, RIGHT_SHOULDER),
    
    # Arms
    ("left_upper_arm", LEFT_SHOULDER, LEFT_ELBOW),
    ("left_lower_arm", LEFT_ELBOW, LEFT_WRIST),
    ("right_upper_arm", RIGHT_SHOULDER, RIGHT_ELBOW),
    ("right_lower_arm", RIGHT_ELBOW, RIGHT_WRIST),
    
    # Hip bridge
    ("hip_bridge", LEFT_HIP, RIGHT_HIP),
    
    # Legs
    ("left_upper_leg", LEFT_HIP, LEFT_KNEE),
    ("left_lower_leg", LEFT_KNEE, LEFT_ANKLE),
    ("right_upper_leg", RIGHT_HIP, RIGHT_KNEE),
    ("right_lower_leg", RIGHT_KNEE, RIGHT_ANKLE),`;

      case 'simple':
        return `
    # Simple spine
    ("spine_upper", HEAD_POS, NECK_POS),
    ("spine_lower", NECK_POS, PELVIS_POS),
    
    # Shoulder bridge
    ("shoulder_bridge", LEFT_SHOULDER, RIGHT_SHOULDER),
    
    # Arms
    ("left_arm", LEFT_SHOULDER, LEFT_WRIST),
    ("right_arm", RIGHT_SHOULDER, RIGHT_WRIST),
    
    # Hip bridge
    ("hip_bridge", LEFT_HIP, RIGHT_HIP),
    
    # Legs
    ("left_leg", LEFT_HIP, LEFT_ANKLE),
    ("right_leg", RIGHT_HIP, RIGHT_ANKLE),`;

      case 'animal':
        return `
    # Neck
    ("neck", HEAD_POS, NECK_BASE),
    
    # Spine
    ("spine_front", NECK_BASE, SPINE_FRONT),
    ("spine_mid", SPINE_FRONT, SPINE_MID),
    ("spine_rear", SPINE_MID, SPINE_REAR),
    ("tail", TAIL_BASE, TAIL_TIP),
    
    # Front legs
    ("left_front_upper", LEFT_FRONT_SHOULDER, LEFT_FRONT_ELBOW),
    ("left_front_lower", LEFT_FRONT_ELBOW, LEFT_FRONT_FOOT),
    ("right_front_upper", RIGHT_FRONT_SHOULDER, RIGHT_FRONT_ELBOW),
    ("right_front_lower", RIGHT_FRONT_ELBOW, RIGHT_FRONT_FOOT),
    
    # Rear legs
    ("left_rear_upper", LEFT_REAR_HIP, LEFT_REAR_KNEE),
    ("left_rear_lower", LEFT_REAR_KNEE, LEFT_REAR_FOOT),
    ("right_rear_upper", RIGHT_REAR_HIP, RIGHT_REAR_KNEE),
    ("right_rear_lower", RIGHT_REAR_KNEE, RIGHT_REAR_FOOT),`;
    }
  };

  // Get joint positions based on armature type
  const getJointPositions = () => {
    switch (armatureType) {
      case 'humanoid':
        return `
    NECK_POS,
    LEFT_SHOULDER, RIGHT_SHOULDER,
    LEFT_ELBOW, RIGHT_ELBOW,
    LEFT_WRIST, RIGHT_WRIST,
    LEFT_HIP, RIGHT_HIP,
    LEFT_KNEE, RIGHT_KNEE,
    LEFT_ANKLE, RIGHT_ANKLE,`;

      case 'simple':
        return `
    NECK_POS,
    LEFT_SHOULDER, RIGHT_SHOULDER,
    LEFT_WRIST, RIGHT_WRIST,
    LEFT_HIP, RIGHT_HIP,
    LEFT_ANKLE, RIGHT_ANKLE,`;

      case 'animal':
        return `
    NECK_BASE,
    LEFT_FRONT_SHOULDER, RIGHT_FRONT_SHOULDER,
    LEFT_FRONT_ELBOW, RIGHT_FRONT_ELBOW,
    LEFT_REAR_HIP, RIGHT_REAR_HIP,
    LEFT_REAR_KNEE, RIGHT_REAR_KNEE,`;
    }
  };

  return `# Blender Python Script for Puppet Armature Generator
# Generated by Web Interface
# Armature Type: ${armatureType}
# Scale Factor: ${scaleFactor}
# Ball Joint Radius: ${ballJointRadius}mm
# Socket Gap: ${socketGap}mm
# Bone Diameter: ${boneDiameter}mm

import bpy
import math
from mathutils import Vector, Matrix

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ============================================================================
# CONFIGURATION
# ============================================================================
BALL_RADIUS = ${ballJointRadius}  # mm
SOCKET_INNER_RADIUS = ${socketInnerRadius.toFixed(3)}  # mm
SOCKET_OUTER_RADIUS = ${socketOuterRadius.toFixed(3)}  # mm
BONE_DIAMETER = ${boneDiameter}  # mm
SOCKET_GAP = ${socketGap}  # mm

# ============================================================================
# ARMATURE PROPORTIONS
# ============================================================================
${getArmatureBones()}

# ============================================================================
# MATERIALS
# ============================================================================
def create_material(name, color):
    """Create a material with given RGB color"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.3
    bsdf.inputs['Roughness'].default_value = 0.4
    return mat

# Color-coded materials
BALL_MATERIAL = create_material("Ball_Joint", (0.9, 0.2, 0.2))    # Red for joints
BONE_MATERIAL = create_material("Bone", (0.4, 0.5, 0.9))          # Blue for bones
SOCKET_MATERIAL = create_material("Socket", (0.5, 0.5, 0.5))      # Gray for sockets

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def create_ball_joint(location, name):
    """Create a ball-and-socket joint at the given location"""
    # Create ball (sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=BALL_RADIUS,
        location=location
    )
    ball = bpy.context.active_object
    ball.name = f"{name}_ball"
    ball.data.materials.append(BALL_MATERIAL)
    
    # Create socket (hollow sphere segment)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=SOCKET_OUTER_RADIUS,
        depth=SOCKET_OUTER_RADIUS * 1.5,
        location=location
    )
    socket = bpy.context.active_object
    socket.name = f"{name}_socket"
    
    # Create inner cutout for socket
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=SOCKET_INNER_RADIUS,
        location=location
    )
    inner_sphere = bpy.context.active_object
    
    # Boolean difference for socket
    modifier = socket.modifiers.new(name="Hollow", type='BOOLEAN')
    modifier.object = inner_sphere
    modifier.operation = 'DIFFERENCE'
    
    # Apply modifier and delete inner sphere
    bpy.context.view_layer.objects.active = socket
    bpy.ops.object.modifier_apply(modifier="Hollow")
    bpy.data.objects.remove(inner_sphere, do_unlink=True)
    
    socket.data.materials.append(SOCKET_MATERIAL)
    
    return ball, socket

def create_bone(start, end, diameter, name):
    """Create a bone/link between two points"""
    direction = Vector(end) - Vector(start)
    length = direction.length
    center = [(start[0] + end[0])/2, (start[1] + end[1])/2, (start[2] + end[2])/2]
    
    # Create cylinder for bone
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diameter/2,
        depth=length,
        location=center
    )
    bone = bpy.context.active_object
    bone.name = name
    
    # Rotate to align with direction
    if length > 0:
        direction.normalize()
        up = Vector((0, 0, 1))
        angle = math.acos(max(-1, min(1, direction.dot(up))))
        axis = up.cross(direction)
        if axis.length > 0:
            axis.normalize()
            bone.rotation_mode = 'AXIS_ANGLE'
            bone.rotation_axis_angle = (angle, axis.x, axis.y, axis.z)
    
    bone.data.materials.append(BONE_MATERIAL)
    return bone

# ============================================================================
# BUILD ARMATURE
# ============================================================================
print("Building ${armatureType} armature...")

# Define bones as (name, start, end) tuples
bones = [
${getBoneConnections()}
]

# Create all bones
for name, start, end in bones:
    create_bone(start, end, BONE_DIAMETER, name)

# Joint positions for ball joints
joint_positions = [
${getJointPositions()}
]

# Create all ball joints
joint_names = [
${armatureType === 'humanoid' ? 
    '"neck", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle"' :
armatureType === 'simple' ?
    '"neck", "left_shoulder", "right_shoulder", "left_wrist", "right_wrist", "left_hip", "right_hip", "left_ankle", "right_ankle"' :
    '"neck_base", "left_front_shoulder", "right_front_shoulder", "left_front_elbow", "right_front_elbow", "left_rear_hip", "right_rear_hip", "left_rear_knee", "right_rear_knee"'
}
]

for pos, name in zip(joint_positions, joint_names):
    create_ball_joint(pos, name)

# Add head for humanoid and simple types
${armatureType !== 'animal' ? `
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=${armatureType === 'humanoid' ? '12 * ' + scale : '10 * ' + scale},
    location=HEAD_POS
)
head = bpy.context.active_object
head.name = "head"
head.data.materials.append(BONE_MATERIAL)
` : `
# Add head for animal
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=8 * ${scale},
    location=HEAD_POS
)
head = bpy.context.active_object
head.name = "head"
head.data.materials.append(BONE_MATERIAL)
`}

# ============================================================================
# COMPLETE
# ============================================================================
print("""
========================================
ARMATURE GENERATION COMPLETE!
========================================
Type: ${armatureType}
Scale: ${scaleFactor}x
Ball Joint Radius: ${ballJointRadius}mm
Socket Gap: ${socketGap}mm
Bone Diameter: ${boneDiameter}mm

Parts Created: {} objects
========================================
""".format(len(bpy.data.objects)))

# Select all objects
bpy.ops.object.select_all(action='SELECT')

print("Script completed successfully!")
`;
}
