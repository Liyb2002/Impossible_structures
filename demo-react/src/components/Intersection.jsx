import { useState, useEffect, useRef } from "react";
import { useDrag } from "@use-gesture/react";
import { useThree, useFrame } from "@react-three/fiber";
import { useSpring, animated, config } from "@react-spring/three";

const UV_MAX = 1;
const UV_MIN = 0;

function Intersection({
  layers,
  intersections,
  setIntersections,
  index,
  material,
  planeMaterial,
  setEnableOrbit,
  showIntersections,
  hoverOn,
  setHoverOn,
}) {
  const [isActive, setIsActive] = useState(false);
  const [firstCenter, setFirstCenter] = useState([0, 0, 0]);
  const [secondCenter, setSecondCenter] = useState([0, 0, 0]);
  const [firstPos, setFirstPos] = useState([0, 0, 0]);
  const [secondPos, setSecondPos] = useState([0, 0, 0]);
  const [currentUV, setCurrentUV] = useState({ u: 0.5, v: 0.5 });
  const [prevXY, setPrevXY] = useState({ x: 0, y: 0 });
  const firstCircle = useRef();
  const secondCircle = useRef();

  // Perspective Camera (fov = 60, aspect ratio = 1.0)
  const CAM_LOWER_LEFT_CORNER = [
    4.250209457436538, 3.951534142681988, 5.0662055923125955,
  ];
  const CAM_HORIZONTAL = [0.8159961348760577, 0.0, -0.8159961348760577];
  const CAM_VERTICAL = [
    -0.4711155881283861, 0.9422311762567722, -0.4711155881283861,
  ];
  const CAM_ORIGIN = [5, 5, 5];

  const add = (v1, v2) => [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]];
  const subtract = (v1, v2) => [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]];
  const scalar = (v, c) => [v[0] * c, v[1] * c, v[2] * c];
  const length = (v) => Math.sqrt(v[0] ** 2, v[1] ** 2, v[2] ** 2);
  const clamp = (v) => Math.max(Math.min(v, UV_MAX), UV_MIN);

  // Center
  const DISTANCE_COEF = 0.181791411511676;

  const getPos = (u, v, center) => {
    let ray = subtract(
      add(
        add(CAM_LOWER_LEFT_CORNER, scalar(CAM_HORIZONTAL, u)),
        scalar(CAM_VERTICAL, v)
      ),
      CAM_ORIGIN
    );

    let t = (center[2] - 5) / ray[2];
    return [5 + ray[0] * t, 5 + ray[1] * t, center[2]];
  };

  useEffect(() => {
    const { layer1, layer2, u, v } = intersections[index];

    if (layer1 >= 0 && layer2 >= 0) {
      const new_firstCenter = Array(3).fill(
        5 - layers[layer1].z * DISTANCE_COEF
      );
      const new_secondCenter = Array(3).fill(
        5 - layers[layer2].z * DISTANCE_COEF
      );

      setFirstCenter(new_firstCenter);
      setSecondCenter(new_secondCenter);

      setFirstPos(getPos(u, v, new_firstCenter));
      setSecondPos(getPos(u, v, new_secondCenter));
      setIsActive(true);
    } else {
      setIsActive(false);
    }
  }, [intersections]);

  // Draggable
  const { size } = useThree();
  const updateUV = (new_u, new_v) => {
    setIntersections(
      intersections.map((intersection, i) => {
        if (i === index) {
          return { ...intersection, u: new_u, v: new_v };
        } else {
          return intersection;
        }
      })
    );
  };

  const bind = useDrag(
    ({ offset: [ox, oy], first, last }) => {
      let { u, v } = currentUV;
      let { x, y } = prevXY;

      if (first) {
        // console.log("Start Drag");
        u = intersections[index].u;
        v = intersections[index].v;
        setCurrentUV({ u, v });
        setEnableOrbit(false);
      }

      // console.log("Dragging");
      const new_u = clamp(u + (ox - x) / size.width);
      const new_v = clamp(v - (oy - y) / size.height);
      updateUV(new_u, new_v);

      if (last) {
        // console.log("End Drag");
        setPrevXY({ x: ox, y: oy });
        setCurrentUV({ u: new_u, v: new_v });
        setEnableOrbit(true);
      }
    },
    { pointerEvents: true }
  );

  const onIntersectionHover = (e) => {
    // console.log("Enter");
    setHoverOn(index);
  };

  const onIntersectionUnhover = (e) => {
    // console.log("Leave");
    setHoverOn(-1);
  };

  useEffect(() => {
    if (hoverOn === index) console.log("OnHover");
  }, [hoverOn]);

  useFrame(({ clock }) => {
    if (isActive) {
      const a = clock.getElapsedTime();
      const scale = Array(3).fill(0.1 * (1 + Math.sin(a * 1.5)));
      firstCircle.current.scale.set(...scale);
      secondCircle.current.scale.set(...scale);
    }
  });

  return (
    <group>
      {isActive ? (
        <>
          <mesh
            key={"intersection-" + index + "-first"}
            position={firstPos}
            {...bind()}
            scale={0.1}
            material={material}
            onPointerOver={onIntersectionHover}
            onPointerOut={onIntersectionUnhover}
          >
            <sphereGeometry args={[1, 16, 16]} />
          </mesh>
          <mesh ref={firstCircle} position={firstPos} material={planeMaterial}>
            <circleGeometry args={[1, 32]} />
          </mesh>
          <mesh
            key={"intersection-" + index + "-second"}
            position={secondPos}
            {...bind()}
            scale={0.1}
            material={material}
            onPointerOver={onIntersectionHover}
            onPointerOut={onIntersectionUnhover}
          >
            <sphereGeometry args={[1, 16, 16]} />
          </mesh>
          <mesh
            ref={secondCircle}
            position={secondPos}
            material={planeMaterial}
          >
            <circleGeometry args={[1, 32]} />
          </mesh>
        </>
      ) : (
        <></>
      )}
    </group>
  );
}

export default Intersection;
