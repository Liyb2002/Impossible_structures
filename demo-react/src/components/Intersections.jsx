import * as THREE from "three";
import { useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import { useEffect } from "react";

function Intersections({ intersections, themes }) {
  const meshMatC = useRef();
  const meshMatM = useRef();
  const meshMatY = useRef();
  const [materials, setMaterials] = useState([]);

  useEffect(
    () => setMaterials([meshMatC.current, meshMatM.current, meshMatY.current]),
    []
  );

  useFrame(({ clock }) => {
    const a = clock.getElapsedTime();
    meshMatC.current.opacity = 0.5 * (1 + Math.sin(a * 1.5));
    meshMatM.current.opacity = 0.5 * (1 + Math.sin(a * 1.5));
    meshMatY.current.opacity = 0.5 * (1 + Math.sin(a * 1.5));
  });

  return (
    <group>
      <meshStandardMaterial ref={meshMatC} color={themes[0]} transparent />
      <meshStandardMaterial ref={meshMatM} color={themes[1]} transparent />
      <meshStandardMaterial ref={meshMatY} color={themes[2]} transparent />
      {intersections.map((intersection, index) => {
        return (
          <mesh
            key={"intersection-" + index}
            position={intersection["position"]}
            scale={0.1}
            material={materials[Math.floor(index / 2)]}
          >
            <sphereGeometry args={[1, 16, 16]} />
          </mesh>
        );
      })}
    </group>
  );
}

export default Intersections;
