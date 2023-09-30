import { useGLTF } from '@react-three/drei';
import { useState, useEffect, useMemo } from 'react';

export default function Beam({ position, scale, rotation, type }) {
  const model1 = useGLTF('./glb/1.glb');
  const model4_0 = useGLTF('./glb/4_0.glb');
  const model4_1 = useGLTF('./glb/4_1.glb');
  const model5_0 = useGLTF('./glb/5_0.glb');
  const model5_1 = useGLTF('./glb/5_1.glb');
  const model5_2 = useGLTF('./glb/5_2.glb');
  const model5_3 = useGLTF('./glb/5_3.glb');
  const model6_0 = useGLTF('./glb/6_0.glb');
  const model6_1 = useGLTF('./glb/6_1.glb');
  const model6_2 = useGLTF('./glb/6_2.glb');
  const model6_3 = useGLTF('./glb/6_3.glb');
  const model6_4 = useGLTF('./glb/6_4.glb');
  const model7 = useGLTF('./glb/7.glb');
  const model8 = useGLTF('./glb/8.glb');
  const model9 = useGLTF('./glb/9.glb');
  const model10 = useGLTF('./glb/10.glb');

  const get_model_name = (type) => {
    var rand = Math.random();
    switch (type) {
      case ('1', '7', '8', '9'):
        return type;
      case '4':
        if (rand < 0.5) return '4_0';
        else return '4_1';
      case '5':
        if (rand < 0.25) return '5_0';
        else if (rand < 0.6) return '5_1';
        else if (rand < 0.9) return '5_2';
        else return '5_3';
      case '6':
        if (rand < 0.3) return '6_0';
        else if (rand < 0.6) return '6_1';
        else if (rand < 0.7) return '6_2';
        else if (rand < 0.8) return '6_3';
        return '6_4';
      default:
        return '1';
    }
  };

  const [modelName, setModelName] = useState();
  const [model, setModel] = useState();
  useEffect(() => {
    var name = get_model_name(type);
    setModelName(name);
    setModel(models[name].clone());
  }, [type]);

  const models = useMemo(
    () => ({
      1: model1.scene,
      '4_0': model4_0.scene,
      '4_1': model4_1.scene,
      '5_0': model5_0.scene,
      '5_1': model5_1.scene,
      '5_2': model5_2.scene,
      '5_3': model5_3.scene,
      '6_0': model6_0.scene,
      '6_1': model6_1.scene,
      '6_2': model6_2.scene,
      '6_3': model6_3.scene,
      '6_4': model6_4.scene,
      7: model7.scene,
      8: model8.scene,
      9: model9.scene,
      10: model10.scene,
    }),
    [
      model1,
      model4_0,
      model4_1,
      model5_0,
      model5_1,
      model5_2,
      model5_3,
      model6_0,
      model6_1,
      model6_2,
      model6_3,
      model6_4,
      model7,
      model8,
      model9,
      model10,
    ]
  );

  return model == undefined ? (
    <></>
  ) : (
    <>
      <primitive
        object={model}
        position={position}
        scale={scale}
        rotation={rotation}
      />
      <meshStandardMaterial toneMapped={false} />
    </>
  );
}
