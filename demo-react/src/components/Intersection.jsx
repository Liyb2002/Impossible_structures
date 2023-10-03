import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

function Intersection({ material, planeMaterial, firstPos, secondPos }) {
  const firstCircle = useRef();
  const secondCircle = useRef();

  useFrame(({ clock }) => {
    const a = clock.getElapsedTime();
    const scale = Array(3).fill(0.1 * (1 + Math.sin(a * 1.5)));
    firstCircle.current.scale.set(...scale);
    secondCircle.current.scale.set(...scale);
  });

  return (
    <group>
      <mesh key={'first'} position={firstPos} scale={0.1} material={material}>
        <sphereGeometry args={[1, 16, 16]} />
      </mesh>
      <mesh ref={firstCircle} position={firstPos} material={planeMaterial}>
        <circleGeometry args={[1, 32]} />
      </mesh>
      <mesh key={'second'} position={secondPos} scale={0.1} material={material}>
        <sphereGeometry args={[1, 16, 16]} />
      </mesh>
      <mesh ref={secondCircle} position={secondPos} material={planeMaterial}>
        <circleGeometry args={[1, 32]} />
      </mesh>
    </group>
  );
}

export default Intersection;
