import * as THREE from "three";
import { useState, useEffect } from "react";
import Beam from "./Beam";

function Structure({ beams, colors, themes, showLayers }) {
  const temp_color = new THREE.Color();
  const [vertexColors, setVertexColors] = useState([]);

  const getVertexColors = (cs) => {
    let vertex_colors = [];
    cs.forEach((color) => {
      temp_color.set(color);
      for (let i = 0; i < 8; i++) {
        vertex_colors.push(temp_color.r, temp_color.g, temp_color.b);
      }
    });
    return Float32Array.from(vertex_colors);
  };

  const layerVertexColors = themes.map((theme) => getVertexColors(theme));

  useEffect(() => {
    setVertexColors(getVertexColors(colors));
  }, [colors]);

  return (
    <>
      {vertexColors.length > 0 ? (
        <group>
          {beams.map((beam, index) => {
            return showLayers && beam.layer === undefined ? (
              <mesh key={index}></mesh>
            ) : (
              <Beam
                key={index}
                position={beam.position}
                scale={beam.scale}
                colors={
                  showLayers && beam.layer !== undefined
                    ? layerVertexColors[beam.layer]
                    : vertexColors
                }
                layer={beam.layer}
              />
            );
          })}
        </group>
      ) : (
        <></>
      )}
    </>
  );
}

export default Structure;
