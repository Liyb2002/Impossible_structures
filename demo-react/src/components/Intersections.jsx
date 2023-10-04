import { useRef, useState, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';

function Intersections({ intersections, themes }) {
  const meshMatC = useRef();
  const [material, setMaterial] = useState();

  useEffect(() => {
    setMaterial(meshMatC.current);
  }, []);

  useFrame(({ clock }) => {
    const a = clock.getElapsedTime();
    meshMatC.current.opacity = 0.3 * (1 + Math.sin(a * 1.5)) + 0.5;
  });

  return (
    <group>
      <meshStandardMaterial ref={meshMatC} color={themes[0]} transparent />
      {intersections != undefined && intersections.length == 2 ? (
        <group>
          <mesh
            key={'first'}
            position={intersections[0]}
            scale={0.15}
            material={material}
          >
            <sphereGeometry args={[1, 16, 16]} />
          </mesh>
          <mesh
            key={'second'}
            position={intersections[1]}
            scale={0.15}
            material={material}
          >
            <sphereGeometry args={[1, 16, 16]} />
          </mesh>
        </group>
      ) : (
        <></>
      )}
    </group>
  );
}

export default Intersections;
