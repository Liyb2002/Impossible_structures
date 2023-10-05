import { useGLTF } from '@react-three/drei';
import { useEffect, useState, useMemo } from 'react';

const ZA_GLBS = [
  '1',
  '4_0',
  '4_1',
  '5_0',
  '5_1',
  '5_2',
  '5_3',
  '6_0',
  '6_1',
  '6_2',
  '6_3',
  '6_4',
  '7',
  '8',
  '9',
  '10',
];

const MT_GLBS = [
  '1_0',
  '3',
  '4',
  '6',
  '9',
  '1_n',
  '3n',
  '4n',
  '6n',
  'x_0',
  'x_1',
  'x_2',
  'z_0',
  'z_1',
  'z_2',
  'y_0',
];

const TR_GLBS = [
  '3',
  '9',
  '10',
  '11',
  '12',
  '13',
  '14',
  'x_1',
  'x',
  'y_1',
  'y',
  'z',
];

function Structure({ objects, scene }) {
  const [models, setModels] = useState([]);
  const baseModels = useMemo(() => {
    var bms = { za: {}, mt: {}, tr: {} };
    ZA_GLBS.forEach(
      (f) => (bms['za'][f] = useGLTF('./glb/za/' + f + '.glb').scene)
    );
    MT_GLBS.forEach(
      (f) => (bms['mt'][f] = useGLTF('./glb/mt/' + f + '.glb').scene)
    );
    TR_GLBS.forEach(
      (f) => (bms['tr'][f] = useGLTF('./glb/tr/' + f + '.glb').scene)
    );
    return bms;
  }, []);

  const getZaModelName = (type) => {
    var rand = Math.random();
    switch (type) {
      case '1':
      case '7':
      case '8':
      case '9':
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
    }
  };

  const getMtModelName = (type) => {
    var rand = Math.random();
    switch (type) {
      case '1':
        return '1_0';
      case '3':
      case '8':
        return '3';
      case '4':
      case '5':
        return '4';
      case '6':
      case '7':
        return '6';
      case '9':
        return '9';
      case '10':
        if (rand < 0.4) return 'x_0';
        else if (rand < 0.7) return 'x_1';
        else return 'x_2';
      case '11':
        if (rand < 0.4) return 'z_0';
        else if (rand < 0.7) return 'z_1';
        else return 'z_2';
      case '12':
        return 'y_0';
      case 101:
        return '1_n';
      case 103:
      case 108:
        return '3n';
      case 104:
      case 105:
        return '4n';
      case 106:
      case 107:
        return '6n';
    }
  };

  const getTrModelName = (type) => {
    var rand = Math.random();
    switch (type) {
      case '9':
        return '9';
      case '10':
        return '10';
      case '11':
        return '11';
      case '12':
        return '12';
      case '13':
        return '13';
      case '14':
        return '14';
      case '5':
      case '6':
        if (rand < 0.5) return 'y';
        else return 'y_1';
      case '3':
      case '4':
        return 'x_1';
      case '7':
      case '8':
        return 'z';
    }
  };

  useEffect(() => {
    var newModels = [];
    var getModelName;
    switch (scene) {
      case 'za':
        getModelName = getZaModelName;
        break;
      case 'mt':
        getModelName = getMtModelName;
        break;
      case 'tr':
        getModelName = getTrModelName;
        break;
      default:
        return;
    }

    objects.forEach((obj, i) => {
      var modelName = getModelName(obj.type);
      if (modelName != undefined) {
        newModels.push(
          <group key={i}>
            <primitive
              object={baseModels[scene][modelName].clone()}
              position={obj.position}
              rotation={obj.rotation}
              scale={obj.scale}
            />
            <meshStandardMaterial toneMapped={false} />
          </group>
        );
      }
    });
    setModels(newModels);
  }, [objects]);

  return (
    <>
      <group>{models}</group>
    </>
  );
}

export default Structure;
