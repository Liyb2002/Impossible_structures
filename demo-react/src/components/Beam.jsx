import * as THREE from "three";
import { useEffect, useState } from "react";

export default function Beam({ position, scale, colors }) {
  return (
    <mesh position={position} scale={scale}>
      <boxGeometry>
        <bufferAttribute attach="attributes-color" args={[colors, 3]} />
      </boxGeometry>
      <meshStandardMaterial toneMapped={false} vertexColors />
    </mesh>
  );
}
