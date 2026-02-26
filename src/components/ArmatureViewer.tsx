'use client';

import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, ContactShadows, Grid } from '@react-three/drei';
import { Suspense, useMemo } from 'react';
import * as THREE from 'three';
import type { ArmatureConfig } from '@/lib/armatureScript';

interface ArmatureViewerProps {
  config: ArmatureConfig;
}

// Ball joint component (red spheres)
function BallJoint({ position, radius }: { 
  position: [number, number, number]; 
  radius: number;
}) {
  return (
    <mesh position={position}>
      <sphereGeometry args={[radius, 24, 24]} />
      <meshStandardMaterial 
        color="#ef4444" 
        metalness={0.6} 
        roughness={0.3} 
      />
    </mesh>
  );
}

// Bone component (blue cylinders)
function Bone({ start, end, diameter }: { 
  start: [number, number, number]; 
  end: [number, number, number]; 
  diameter: number;
}) {
  const boneMesh = useMemo(() => {
    const startVec = new THREE.Vector3(...start);
    const endVec = new THREE.Vector3(...end);
    const direction = new THREE.Vector3().subVectors(endVec, startVec);
    const length = direction.length();
    const center = new THREE.Vector3().addVectors(startVec, endVec).multiplyScalar(0.5);
    
    // Calculate rotation
    const up = new THREE.Vector3(0, 1, 0);
    direction.normalize();
    const quaternion = new THREE.Quaternion().setFromUnitVectors(up, direction);
    
    return { length, center, quaternion };
  }, [start, end]);

  return (
    <mesh 
      position={[boneMesh.center.x, boneMesh.center.y, boneMesh.center.z]} 
      quaternion={boneMesh.quaternion}
    >
      <cylinderGeometry args={[diameter / 2, diameter / 2, boneMesh.length, 16]} />
      <meshStandardMaterial 
        color="#3b82f6" 
        metalness={0.5} 
        roughness={0.4} 
      />
    </mesh>
  );
}

// Body part component (gray)
function BodyPart({ position, size, type = 'sphere' }: { 
  position: [number, number, number]; 
  size: [number, number, number] | number;
  type?: 'sphere' | 'box';
}) {
  return (
    <mesh position={position}>
      {type === 'sphere' ? (
        <sphereGeometry args={[size as number, 24, 24]} />
      ) : (
        <boxGeometry args={size as [number, number, number]} />
      )}
      <meshStandardMaterial 
        color="#6b7280" 
        metalness={0.4} 
        roughness={0.5} 
      />
    </mesh>
  );
}

// Humanoid armature
function HumanoidArmature({ config }: { config: ArmatureConfig }) {
  const scale = config.scaleFactor;
  const baseHeight = 200 * scale;
  const jointRadius = config.ballJointRadius * scale / 3;
  const boneDiameter = config.boneDiameter * scale;
  
  const joints = useMemo(() => ({
    head: [0, baseHeight * 0.9, 0] as [number, number, number],
    neck: [0, baseHeight * 0.78, 0] as [number, number, number],
    chest: [0, baseHeight * 0.65, 0] as [number, number, number],
    pelvis: [0, baseHeight * 0.45, 0] as [number, number, number],
    leftShoulder: [-17.5 * scale, baseHeight * 0.72, 0] as [number, number, number],
    rightShoulder: [17.5 * scale, baseHeight * 0.72, 0] as [number, number, number],
    leftElbow: [-20 * scale, baseHeight * 0.55, 0] as [number, number, number],
    rightElbow: [20 * scale, baseHeight * 0.55, 0] as [number, number, number],
    leftWrist: [-22 * scale, baseHeight * 0.38, 0] as [number, number, number],
    rightWrist: [22 * scale, baseHeight * 0.38, 0] as [number, number, number],
    leftHip: [-10 * scale, baseHeight * 0.42, 0] as [number, number, number],
    rightHip: [10 * scale, baseHeight * 0.42, 0] as [number, number, number],
    leftKnee: [-10 * scale, baseHeight * 0.25, 0] as [number, number, number],
    rightKnee: [10 * scale, baseHeight * 0.25, 0] as [number, number, number],
    leftAnkle: [-10 * scale, baseHeight * 0.08, 0] as [number, number, number],
    rightAnkle: [10 * scale, baseHeight * 0.08, 0] as [number, number, number],
  }), [scale, baseHeight]);

  return (
    <group>
      {/* Head - gray body part */}
      <BodyPart position={joints.head} size={12 * scale} />
      
      {/* Spine bones */}
      <Bone start={joints.head} end={joints.neck} diameter={boneDiameter} />
      <Bone start={joints.neck} end={joints.chest} diameter={boneDiameter} />
      <Bone start={joints.chest} end={joints.pelvis} diameter={boneDiameter * 1.2} />
      
      {/* Shoulder bridge */}
      <Bone start={joints.leftShoulder} end={joints.rightShoulder} diameter={boneDiameter} />
      
      {/* Arms */}
      <Bone start={joints.leftShoulder} end={joints.leftElbow} diameter={boneDiameter * 0.8} />
      <Bone start={joints.leftElbow} end={joints.leftWrist} diameter={boneDiameter * 0.7} />
      <Bone start={joints.rightShoulder} end={joints.rightElbow} diameter={boneDiameter * 0.8} />
      <Bone start={joints.rightElbow} end={joints.rightWrist} diameter={boneDiameter * 0.7} />
      
      {/* Hip bridge */}
      <Bone start={joints.leftHip} end={joints.rightHip} diameter={boneDiameter * 1.2} />
      
      {/* Legs */}
      <Bone start={joints.leftHip} end={joints.leftKnee} diameter={boneDiameter} />
      <Bone start={joints.leftKnee} end={joints.leftAnkle} diameter={boneDiameter * 0.9} />
      <Bone start={joints.rightHip} end={joints.rightKnee} diameter={boneDiameter} />
      <Bone start={joints.rightKnee} end={joints.rightAnkle} diameter={boneDiameter * 0.9} />
      
      {/* Ball joints - red spheres */}
      <BallJoint position={joints.neck} radius={jointRadius} />
      <BallJoint position={joints.leftShoulder} radius={jointRadius} />
      <BallJoint position={joints.rightShoulder} radius={jointRadius} />
      <BallJoint position={joints.leftElbow} radius={jointRadius} />
      <BallJoint position={joints.rightElbow} radius={jointRadius} />
      <BallJoint position={joints.leftWrist} radius={jointRadius} />
      <BallJoint position={joints.rightWrist} radius={jointRadius} />
      <BallJoint position={joints.leftHip} radius={jointRadius} />
      <BallJoint position={joints.rightHip} radius={jointRadius} />
      <BallJoint position={joints.leftKnee} radius={jointRadius} />
      <BallJoint position={joints.rightKnee} radius={jointRadius} />
      <BallJoint position={joints.leftAnkle} radius={jointRadius} />
      <BallJoint position={joints.rightAnkle} radius={jointRadius} />
      
      {/* Feet - gray body parts */}
      <BodyPart 
        position={[joints.leftAnkle[0], 5 * scale, 3 * scale]} 
        size={[10 * scale, 20 * scale, 6 * scale]} 
        type="box" 
      />
      <BodyPart 
        position={[joints.rightAnkle[0], 5 * scale, 3 * scale]} 
        size={[10 * scale, 20 * scale, 6 * scale]} 
        type="box" 
      />
    </group>
  );
}

// Simple armature
function SimpleArmature({ config }: { config: ArmatureConfig }) {
  const scale = config.scaleFactor;
  const baseHeight = 150 * scale;
  const jointRadius = config.ballJointRadius * scale / 3;
  const boneDiameter = config.boneDiameter * scale;
  
  const joints = useMemo(() => ({
    head: [0, baseHeight * 0.92, 0] as [number, number, number],
    neck: [0, baseHeight * 0.80, 0] as [number, number, number],
    pelvis: [0, baseHeight * 0.45, 0] as [number, number, number],
    leftShoulder: [-15 * scale, baseHeight * 0.75, 0] as [number, number, number],
    rightShoulder: [15 * scale, baseHeight * 0.75, 0] as [number, number, number],
    leftWrist: [-15 * scale, baseHeight * 0.35, 0] as [number, number, number],
    rightWrist: [15 * scale, baseHeight * 0.35, 0] as [number, number, number],
    leftHip: [-7.5 * scale, baseHeight * 0.42, 0] as [number, number, number],
    rightHip: [7.5 * scale, baseHeight * 0.42, 0] as [number, number, number],
    leftAnkle: [-7.5 * scale, baseHeight * 0.08, 0] as [number, number, number],
    rightAnkle: [7.5 * scale, baseHeight * 0.08, 0] as [number, number, number],
  }), [scale, baseHeight]);

  return (
    <group>
      {/* Head */}
      <BodyPart position={joints.head} size={10 * scale} />
      
      {/* Spine */}
      <Bone start={joints.head} end={joints.neck} diameter={boneDiameter} />
      <Bone start={joints.neck} end={joints.pelvis} diameter={boneDiameter * 1.2} />
      
      {/* Shoulder bridge */}
      <Bone start={joints.leftShoulder} end={joints.rightShoulder} diameter={boneDiameter} />
      
      {/* Arms (no elbows) */}
      <Bone start={joints.leftShoulder} end={joints.leftWrist} diameter={boneDiameter * 0.7} />
      <Bone start={joints.rightShoulder} end={joints.rightWrist} diameter={boneDiameter * 0.7} />
      
      {/* Hip bridge */}
      <Bone start={joints.leftHip} end={joints.rightHip} diameter={boneDiameter * 1.2} />
      
      {/* Legs (no knees) */}
      <Bone start={joints.leftHip} end={joints.leftAnkle} diameter={boneDiameter * 0.9} />
      <Bone start={joints.rightHip} end={joints.rightAnkle} diameter={boneDiameter * 0.9} />
      
      {/* Ball joints */}
      <BallJoint position={joints.neck} radius={jointRadius} />
      <BallJoint position={joints.leftShoulder} radius={jointRadius} />
      <BallJoint position={joints.rightShoulder} radius={jointRadius} />
      <BallJoint position={joints.leftWrist} radius={jointRadius} />
      <BallJoint position={joints.rightWrist} radius={jointRadius} />
      <BallJoint position={joints.leftHip} radius={jointRadius} />
      <BallJoint position={joints.rightHip} radius={jointRadius} />
      <BallJoint position={joints.leftAnkle} radius={jointRadius} />
      <BallJoint position={joints.rightAnkle} radius={jointRadius} />
      
      {/* Feet */}
      <BodyPart 
        position={[joints.leftAnkle[0], 4 * scale, 2 * scale]} 
        size={[8 * scale, 15 * scale, 5 * scale]} 
        type="box" 
      />
      <BodyPart 
        position={[joints.rightAnkle[0], 4 * scale, 2 * scale]} 
        size={[8 * scale, 15 * scale, 5 * scale]} 
        type="box" 
      />
    </group>
  );
}

// Animal (quadruped) armature
function AnimalArmature({ config }: { config: ArmatureConfig }) {
  const scale = config.scaleFactor;
  const baseHeight = 100 * scale;
  const bodyLength = 200 * scale;
  const jointRadius = config.ballJointRadius * scale / 3;
  const boneDiameter = config.boneDiameter * scale;
  
  const joints = useMemo(() => ({
    head: [bodyLength * 0.4, baseHeight * 0.7, 0] as [number, number, number],
    neckBase: [bodyLength * 0.3, baseHeight * 0.6, 0] as [number, number, number],
    spineFront: [bodyLength * 0.25, baseHeight * 0.55, 0] as [number, number, number],
    spineMid: [0, baseHeight * 0.5, 0] as [number, number, number],
    spineRear: [-bodyLength * 0.25, baseHeight * 0.55, 0] as [number, number, number],
    tailBase: [-bodyLength * 0.35, baseHeight * 0.5, 0] as [number, number, number],
    tailMid: [-bodyLength * 0.45, baseHeight * 0.45, 0] as [number, number, number],
    tailTip: [-bodyLength * 0.55, baseHeight * 0.35, 0] as [number, number, number],
    leftFrontShoulder: [bodyLength * 0.2, baseHeight * 0.5, -10 * scale] as [number, number, number],
    rightFrontShoulder: [bodyLength * 0.2, baseHeight * 0.5, 10 * scale] as [number, number, number],
    leftFrontElbow: [bodyLength * 0.2, baseHeight * 0.3, -10 * scale] as [number, number, number],
    rightFrontElbow: [bodyLength * 0.2, baseHeight * 0.3, 10 * scale] as [number, number, number],
    leftFrontFoot: [bodyLength * 0.22, baseHeight * 0.05, -10 * scale] as [number, number, number],
    rightFrontFoot: [bodyLength * 0.22, baseHeight * 0.05, 10 * scale] as [number, number, number],
    leftRearHip: [-bodyLength * 0.2, baseHeight * 0.5, -11 * scale] as [number, number, number],
    rightRearHip: [-bodyLength * 0.2, baseHeight * 0.5, 11 * scale] as [number, number, number],
    leftRearKnee: [-bodyLength * 0.22, baseHeight * 0.35, -11 * scale] as [number, number, number],
    rightRearKnee: [-bodyLength * 0.22, baseHeight * 0.35, 11 * scale] as [number, number, number],
    leftRearFoot: [-bodyLength * 0.2, baseHeight * 0.05, -11 * scale] as [number, number, number],
    rightRearFoot: [-bodyLength * 0.2, baseHeight * 0.05, 11 * scale] as [number, number, number],
  }), [scale, baseHeight, bodyLength]);

  return (
    <group>
      {/* Head */}
      <BodyPart position={joints.head} size={8 * scale} />
      
      {/* Neck */}
      <Bone start={joints.head} end={joints.neckBase} diameter={boneDiameter * 0.8} />
      
      {/* Spine */}
      <Bone start={joints.neckBase} end={joints.spineFront} diameter={boneDiameter} />
      <Bone start={joints.spineFront} end={joints.spineMid} diameter={boneDiameter * 1.2} />
      <Bone start={joints.spineMid} end={joints.spineRear} diameter={boneDiameter * 1.2} />
      
      {/* Tail */}
      <Bone start={joints.spineRear} end={joints.tailBase} diameter={boneDiameter * 0.8} />
      <Bone start={joints.tailBase} end={joints.tailMid} diameter={boneDiameter * 0.6} />
      <Bone start={joints.tailMid} end={joints.tailTip} diameter={boneDiameter * 0.4} />
      
      {/* Front legs */}
      <Bone start={joints.leftFrontShoulder} end={joints.leftFrontElbow} diameter={boneDiameter * 0.8} />
      <Bone start={joints.leftFrontElbow} end={joints.leftFrontFoot} diameter={boneDiameter * 0.7} />
      <Bone start={joints.rightFrontShoulder} end={joints.rightFrontElbow} diameter={boneDiameter * 0.8} />
      <Bone start={joints.rightFrontElbow} end={joints.rightFrontFoot} diameter={boneDiameter * 0.7} />
      
      {/* Rear legs */}
      <Bone start={joints.leftRearHip} end={joints.leftRearKnee} diameter={boneDiameter * 0.9} />
      <Bone start={joints.leftRearKnee} end={joints.leftRearFoot} diameter={boneDiameter * 0.8} />
      <Bone start={joints.rightRearHip} end={joints.rightRearKnee} diameter={boneDiameter * 0.9} />
      <Bone start={joints.rightRearKnee} end={joints.rightRearFoot} diameter={boneDiameter * 0.8} />
      
      {/* Ball joints */}
      <BallJoint position={joints.neckBase} radius={jointRadius} />
      <BallJoint position={joints.leftFrontShoulder} radius={jointRadius} />
      <BallJoint position={joints.rightFrontShoulder} radius={jointRadius} />
      <BallJoint position={joints.leftFrontElbow} radius={jointRadius} />
      <BallJoint position={joints.rightFrontElbow} radius={jointRadius} />
      <BallJoint position={joints.leftRearHip} radius={jointRadius} />
      <BallJoint position={joints.rightRearHip} radius={jointRadius} />
      <BallJoint position={joints.leftRearKnee} radius={jointRadius} />
      <BallJoint position={joints.rightRearKnee} radius={jointRadius} />
      
      {/* Paws - small gray boxes */}
      <BodyPart position={joints.leftFrontFoot} size={[6 * scale, 8 * scale, 4 * scale]} type="box" />
      <BodyPart position={joints.rightFrontFoot} size={[6 * scale, 8 * scale, 4 * scale]} type="box" />
      <BodyPart position={joints.leftRearFoot} size={[6 * scale, 8 * scale, 4 * scale]} type="box" />
      <BodyPart position={joints.rightRearFoot} size={[6 * scale, 8 * scale, 4 * scale]} type="box" />
    </group>
  );
}

// Scene setup
function Scene({ config }: ArmatureViewerProps) {
  const cameraPosition = useMemo(() => {
    const baseDistance = config.armatureType === 'animal' ? 350 : 300;
    return [0, 150, baseDistance * config.scaleFactor] as [number, number, number];
  }, [config.scaleFactor, config.armatureType]);

  const targetHeight = useMemo(() => {
    return config.armatureType === 'animal' ? 50 * config.scaleFactor : 100 * config.scaleFactor;
  }, [config.scaleFactor, config.armatureType]);

  return (
    <>
      <PerspectiveCamera makeDefault position={cameraPosition} fov={50} />
      <OrbitControls 
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={50}
        maxDistance={600}
        target={[0, targetHeight, 0]}
      />
      
      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[100, 200, 100]} intensity={0.8} castShadow />
      <directionalLight position={[-100, 150, -50]} intensity={0.4} />
      <pointLight position={[0, 300, 0]} intensity={0.3} />
      
      {/* Grid */}
      <Grid 
        args={[400, 400]} 
        position={[0, 0, 0]}
        cellSize={20}
        cellThickness={0.5}
        cellColor="#374151"
        sectionSize={100}
        sectionThickness={1}
        sectionColor="#1f2937"
        fadeDistance={500}
        fadeStrength={1}
      />
      
      {/* Ground shadow */}
      <ContactShadows 
        position={[0, 0, 0]}
        opacity={0.4}
        scale={400}
        blur={2}
        far={100}
      />
      
      {/* Armature */}
      <group position={[0, 0, 0]}>
        {config.armatureType === 'humanoid' && <HumanoidArmature config={config} />}
        {config.armatureType === 'simple' && <SimpleArmature config={config} />}
        {config.armatureType === 'animal' && <AnimalArmature config={config} />}
      </group>
    </>
  );
}

// Loading fallback
function LoadingFallback() {
  return (
    <mesh>
      <boxGeometry args={[50, 50, 50]} />
      <meshStandardMaterial color="#374151" wireframe />
    </mesh>
  );
}

export default function ArmatureViewer({ config }: ArmatureViewerProps) {
  return (
    <div className="w-full h-full bg-gradient-to-b from-slate-900 to-slate-800 rounded-lg overflow-hidden">
      <Canvas shadows>
        <Suspense fallback={<LoadingFallback />}>
          <Scene config={config} />
        </Suspense>
      </Canvas>
    </div>
  );
}
