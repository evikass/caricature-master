'use client';

import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, ContactShadows, PerspectiveCamera } from '@react-three/drei';
import { Suspense, useMemo } from 'react';
import * as THREE from 'three';
import type { ArmatureSettings } from '@/lib/armature-generator';

interface ArmaturePreviewProps {
  settings: ArmatureSettings;
}

// Ball joint component
function BallJoint({ position, radius, isSocket = false }: { 
  position: [number, number, number]; 
  radius: number; 
  isSocket?: boolean;
}) {
  return (
    <mesh position={position}>
      <sphereGeometry args={[radius, 16, 16]} />
      <meshStandardMaterial 
        color={isSocket ? '#3b82f6' : '#ef4444'} 
        metalness={0.6} 
        roughness={0.3} 
      />
    </mesh>
  );
}

// Bone component (cylinder between two points)
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
      <cylinderGeometry args={[diameter / 2, diameter / 2, boneMesh.length, 12]} />
      <meshStandardMaterial color="#6b7280" metalness={0.5} roughness={0.4} />
    </mesh>
  );
}

// Hand component
function Hand({ wristPosition, side, fingerCount, scale }: {
  wristPosition: [number, number, number];
  side: 'left' | 'right';
  fingerCount: number;
  scale: number;
}) {
  const handCenter: [number, number, number] = [
    wristPosition[0] + (side === 'left' ? -8 : 8) * scale,
    wristPosition[1],
    wristPosition[2] - 10 * scale,
  ];

  const fingers = useMemo(() => {
    const fingerSpacing = 3 * scale;
    const startX = handCenter[0] - ((fingerCount - 1) * fingerSpacing) / 2;
    
    return Array.from({ length: fingerCount }, (_, i) => ({
      base: [startX + i * fingerSpacing, handCenter[1], handCenter[2] - 3 * scale] as [number, number, number],
      tip: [startX + i * fingerSpacing, handCenter[1], handCenter[2] - 12 * scale] as [number, number, number],
    }));
  }, [fingerCount, scale, handCenter]);

  return (
    <group>
      {/* Palm */}
      <mesh position={handCenter}>
        <boxGeometry args={[8 * scale, 3 * scale, 6 * scale]} />
        <meshStandardMaterial color="#eab308" metalness={0.4} roughness={0.5} />
      </mesh>
      
      {/* Fingers */}
      {fingers.map((finger, i) => (
        <group key={i}>
          <Bone start={finger.base} end={finger.tip} diameter={2 * scale} />
          <BallJoint position={finger.tip} radius={1.2 * scale} />
        </group>
      ))}
      
      {/* Thumb */}
      <Bone 
        start={[
          handCenter[0] + (side === 'left' ? 3 : -3) * scale,
          handCenter[1] + 3 * scale,
          handCenter[2]
        ]}
        end={[
          handCenter[0] + (side === 'left' ? 3 : -3) * scale,
          handCenter[1] + 6 * scale,
          handCenter[2] - 5 * scale
        ]}
        diameter={2 * scale}
      />
    </group>
  );
}

// Foot component
function Foot({ anklePosition, side, scale }: {
  anklePosition: [number, number, number];
  side: 'left' | 'right';
  scale: number;
}) {
  const footCenter: [number, number, number] = [
    anklePosition[0],
    anklePosition[1] + 8 * scale,
    3 * scale,
  ];

  return (
    <group>
      <mesh position={footCenter}>
        <boxGeometry args={[10 * scale, 20 * scale, 6 * scale]} />
        <meshStandardMaterial color="#22c55e" metalness={0.4} roughness={0.5} />
      </mesh>
      {/* Tie-down hole indicator */}
      <mesh position={[footCenter[0], footCenter[1] - 5 * scale, footCenter[2] + 2 * scale]}>
        <cylinderGeometry args={[2 * scale, 2 * scale, 2 * scale, 12]} />
        <meshStandardMaterial color="#1f2937" metalness={0.7} roughness={0.3} />
      </mesh>
    </group>
  );
}

// Head component
function Head({ position, scale }: { position: [number, number, number]; scale: number }) {
  return (
    <mesh position={position}>
      <sphereGeometry args={[12 * scale, 24, 24]} />
      <meshStandardMaterial color="#9ca3af" metalness={0.4} roughness={0.5} />
    </mesh>
  );
}

// Main Armature component
function Armature({ settings }: ArmaturePreviewProps) {
  const scale = settings.height / 200;
  const jointRadius = settings.jointDiameter / 2 * scale;
  
  // Joint positions
  const joints = useMemo(() => ({
    head: [0, settings.height * 0.9, 0] as [number, number, number],
    neck: [0, settings.height * 0.78, 0] as [number, number, number],
    leftShoulder: [-17.5 * scale, settings.height * 0.73, 0] as [number, number, number],
    rightShoulder: [17.5 * scale, settings.height * 0.73, 0] as [number, number, number],
    leftElbow: [-20 * scale, settings.height * 0.58, 0] as [number, number, number],
    rightElbow: [20 * scale, settings.height * 0.58, 0] as [number, number, number],
    leftWrist: [-22 * scale, settings.height * 0.43, 0] as [number, number, number],
    rightWrist: [22 * scale, settings.height * 0.43, 0] as [number, number, number],
    leftHip: [-10 * scale, settings.height * 0.42, 0] as [number, number, number],
    rightHip: [10 * scale, settings.height * 0.42, 0] as [number, number, number],
    leftKnee: [-10 * scale, settings.height * 0.25, 0] as [number, number, number],
    rightKnee: [10 * scale, settings.height * 0.25, 0] as [number, number, number],
    leftAnkle: [-10 * scale, settings.height * 0.08, 0] as [number, number, number],
    rightAnkle: [10 * scale, settings.height * 0.08, 0] as [number, number, number],
  }), [settings.height, scale]);

  const boneDiameter = 4 * scale;

  return (
    <group>
      {/* Head */}
      <Head position={joints.head} scale={scale} />
      
      {/* Spine */}
      <Bone start={joints.head} end={joints.neck} diameter={boneDiameter} />
      <Bone start={joints.neck} end={[0, settings.height * 0.72, 0]} diameter={boneDiameter} />
      <Bone start={[0, settings.height * 0.72, 0]} end={[0, settings.height * 0.45, 0]} diameter={boneDiameter * 1.2} />
      
      {/* Neck joint */}
      <BallJoint position={joints.neck} radius={jointRadius} />
      
      {/* Shoulder bridge */}
      <Bone start={joints.leftShoulder} end={joints.rightShoulder} diameter={boneDiameter} />
      
      {/* Arms */}
      <BallJoint position={joints.leftShoulder} radius={jointRadius} />
      <BallJoint position={joints.rightShoulder} radius={jointRadius} />
      
      <Bone start={joints.leftShoulder} end={joints.leftElbow} diameter={boneDiameter * 0.8} />
      <Bone start={joints.rightShoulder} end={joints.rightElbow} diameter={boneDiameter * 0.8} />
      
      <BallJoint position={joints.leftElbow} radius={jointRadius} />
      <BallJoint position={joints.rightElbow} radius={jointRadius} />
      
      <Bone start={joints.leftElbow} end={joints.leftWrist} diameter={boneDiameter * 0.7} />
      <Bone start={joints.rightElbow} end={joints.rightWrist} diameter={boneDiameter * 0.7} />
      
      <BallJoint position={joints.leftWrist} radius={jointRadius} />
      <BallJoint position={joints.rightWrist} radius={jointRadius} />
      
      {/* Hands */}
      <Hand 
        wristPosition={joints.leftWrist} 
        side="left" 
        fingerCount={settings.fingerCount}
        scale={scale}
      />
      <Hand 
        wristPosition={joints.rightWrist} 
        side="right" 
        fingerCount={settings.fingerCount}
        scale={scale}
      />
      
      {/* Hip bridge */}
      <Bone start={joints.leftHip} end={joints.rightHip} diameter={boneDiameter * 1.2} />
      
      {/* Legs */}
      <BallJoint position={joints.leftHip} radius={jointRadius} />
      <BallJoint position={joints.rightHip} radius={jointRadius} />
      
      <Bone start={joints.leftHip} end={joints.leftKnee} diameter={boneDiameter} />
      <Bone start={joints.rightHip} end={joints.rightKnee} diameter={boneDiameter} />
      
      <BallJoint position={joints.leftKnee} radius={jointRadius} />
      <BallJoint position={joints.rightKnee} radius={jointRadius} />
      
      <Bone start={joints.leftKnee} end={joints.leftAnkle} diameter={boneDiameter * 0.9} />
      <Bone start={joints.rightKnee} end={joints.rightAnkle} diameter={boneDiameter * 0.9} />
      
      <BallJoint position={joints.leftAnkle} radius={jointRadius} />
      <BallJoint position={joints.rightAnkle} radius={jointRadius} />
      
      {/* Feet */}
      <Foot anklePosition={joints.leftAnkle} side="left" scale={scale} />
      <Foot anklePosition={joints.rightAnkle} side="right" scale={scale} />
      
      {/* Optional ears */}
      {settings.includeEars && (
        <>
          <mesh 
            position={[-10 * scale, settings.height * 0.92, 0]}
            rotation={[0, 0, Math.PI / 9]}
          >
            <coneGeometry args={[3 * scale, 8 * scale, 12]} />
            <meshStandardMaterial color="#6b7280" metalness={0.5} roughness={0.4} />
          </mesh>
          <mesh 
            position={[10 * scale, settings.height * 0.92, 0]}
            rotation={[0, 0, -Math.PI / 9]}
          >
            <coneGeometry args={[3 * scale, 8 * scale, 12]} />
            <meshStandardMaterial color="#6b7280" metalness={0.5} roughness={0.4} />
          </mesh>
        </>
      )}
      
      {/* Optional tail */}
      {settings.includeTail && (
        <group>
          <Bone 
            start={[0, -8 * scale, settings.height * 0.38]}
            end={[0, -15 * scale, settings.height * 0.35]}
            diameter={boneDiameter}
          />
          <Bone 
            start={[0, -15 * scale, settings.height * 0.35]}
            end={[0, -22 * scale, settings.height * 0.30]}
            diameter={boneDiameter * 0.85}
          />
          <Bone 
            start={[0, -22 * scale, settings.height * 0.30]}
            end={[0, -28 * scale, settings.height * 0.22]}
            diameter={boneDiameter * 0.7}
          />
        </group>
      )}
    </group>
  );
}

// Scene lighting and controls
function Scene({ settings }: ArmaturePreviewProps) {
  return (
    <>
      <PerspectiveCamera makeDefault position={[0, 150, 300]} fov={50} />
      <OrbitControls 
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={100}
        maxDistance={800}
        target={[0, settings.height / 2, 0]}
      />
      
      {/* Lighting */}
      <ambientLight intensity={0.4} />
      <directionalLight position={[100, 200, 100]} intensity={0.8} castShadow />
      <directionalLight position={[-100, 150, -50]} intensity={0.4} />
      <pointLight position={[0, 300, 0]} intensity={0.3} />
      
      {/* Environment */}
      <Environment preset="studio" />
      
      {/* Ground shadow */}
      <ContactShadows 
        position={[0, 0, 0]}
        opacity={0.4}
        scale={400}
        blur={2}
        far={100}
      />
      
      {/* Grid helper */}
      <gridHelper args={[400, 40, '#374151', '#1f2937']} position={[0, 0, 0]} />
      
      {/* Center the armature */}
      <group position={[0, 0, 0]}>
        <Armature settings={settings} />
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

// Main export
export default function ArmaturePreview({ settings }: ArmaturePreviewProps) {
  return (
    <div className="w-full h-full bg-gradient-to-b from-slate-900 to-slate-800 rounded-lg overflow-hidden">
      <Canvas shadows>
        <Suspense fallback={<LoadingFallback />}>
          <Scene settings={settings} />
        </Suspense>
      </Canvas>
    </div>
  );
}
