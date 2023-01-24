import * as THREE from "three";
import { useRef, useState, useEffect } from "react";
import { useFrame } from "@react-three/fiber";

import Intersection from "./Intersection";

function Intersections({
  layers,
  intersections,
  setIntersections,
  themes,
  setEnableOrbit,
  showIntersections,
}) {
  const meshMatC = useRef();
  const meshMatM = useRef();
  const meshMatY = useRef();
  const planeMatC = useRef();
  const planeMatM = useRef();
  const planeMatY = useRef();
  const [materials, setMaterials] = useState([]);
  const [planeMaterials, setPlaneMaterials] = useState([]);
  const [hoverOn, setHoverOn] = useState(-1);

  useEffect(() => {
    setMaterials([meshMatC.current, meshMatM.current, meshMatY.current]);
    setPlaneMaterials([
      planeMatC.current,
      planeMatM.current,
      planeMatY.current,
    ]);
  }, []);

  useFrame(({ clock }) => {
    const a = clock.getElapsedTime();
    // if (hoverOn === 0) {
    meshMatC.current.opacity = 0.3 * (1 + Math.sin(a * 1.5)) + 0.2;
    planeMatC.current.opacity = 0.1 * (1 + Math.sin(a * 1.5));
    // } else if (hoverOn === 1) {
    meshMatM.current.opacity = 0.3 * (1 + Math.sin(a * 1.5)) + 0.2;
    planeMatM.current.opacity = 0.1 * (1 + Math.sin(a * 1.5));
    // } else if (hoverOn === 2) {
    meshMatY.current.opacity = 0.3 * (1 + Math.sin(a * 1.5)) + 0.2;
    planeMatY.current.opacity = 0.1 * (1 + Math.sin(a * 1.5));
    // }
  });

  return (
    <group>
      <meshStandardMaterial ref={meshMatC} color={themes[0]} transparent />
      <meshStandardMaterial ref={meshMatM} color={themes[1]} transparent />
      <meshStandardMaterial ref={meshMatY} color={themes[2]} transparent />
      <meshStandardMaterial ref={planeMatC} color={themes[0]} transparent />
      <meshStandardMaterial ref={planeMatM} color={themes[1]} transparent />
      <meshStandardMaterial ref={planeMatY} color={themes[2]} transparent />
      {intersections.map((_, index) => (
        <Intersection
          key={"intersection-" + index}
          layers={layers}
          intersections={intersections}
          setIntersections={setIntersections}
          index={index}
          material={materials[index]}
          planeMaterial={planeMaterials[index]}
          setEnableOrbit={setEnableOrbit}
          hoverOn={hoverOn}
          setHoverOn={setHoverOn}
        />
      ))}
    </group>
  );
}

export default Intersections;
