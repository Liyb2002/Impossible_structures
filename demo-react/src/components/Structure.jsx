import Beam from './Beam';

function Structure({ beams }) {
  return (
    <>
      <group>
        {beams.map((beam, index) => {
          return (
            <Beam
              key={index}
              position={beam.position}
              scale={beam.scale}
              rotation={beam.rotation}
              type={beam.type}
            />
          );
        })}
      </group>
    </>
  );
}

export default Structure;
