import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, OrthographicCamera } from '@react-three/drei';
import { useEffect, useRef } from 'react';
import NavBar from 'react-bootstrap/NavBar';
import Spinner from 'react-bootstrap/Spinner';
import { BsFillGearFill } from 'react-icons/bs';
import { useThree } from '@react-three/fiber';

import { gsap } from 'gsap';

import Intersections from './components/Intersections';
import Structure from './components/Structure';
import SideBar from './components/Sidebar';

import za_example from './json/za_example.json';
import mt_example from './json/mt_example.json';
import tp_example from './json/tp_example.json';

function Loading() {
  return (
    <div
      style={{
        position: 'fixed',
        width: '100vw',
        height: '100vh',
        backgroundColor: 'black',
        opacity: '0.8',
        zIndex: '100',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <Spinner
        animation="border"
        role="status"
        style={{ width: '3rem', height: '3rem' }}
      >
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </div>
  );
}

function CanvasControl({ screenshotToggle, bgColor }) {
  const { gl, scene, camera } = useThree();
  useEffect(() => {
    gl.setClearColor(bgColor);
  }, [bgColor]);
  useEffect(() => {
    if (screenshotToggle) {
      gl.render(scene, camera);
      let alink = document.createElement('a');
      alink.setAttribute('download', 'canvas.png');
      alink.setAttribute(
        'href',
        gl.domElement
          .toDataURL('image/png')
          .replace('image/png', 'image/octet-stream')
      );
      alink.click();
    }
  }, [screenshotToggle]);
}

function App() {
  const [resetCameraToggle, setResetCameraToggle] = useState(false);
  const [showIntersections, setShowIntersections] = useState(false);
  const [showSideBar, setShowSideBar] = useState(false);
  const [showLoading, setShowLoading] = useState(true);
  const [intersections, setIntersections] = useState();
  const [bgColor, setBgColor] = useState('#ffffff');
  const [scene, setScene] = useState('za');
  const [center, setCenter] = useState([0, 0, 0]);
  const [objects, setObjects] = useState([]);
  const controlRef = useRef();
  const cameraRef = useRef();
  const comp = useRef();

  const INTERSECTION_COLORS = [
    '#00ffff', // cyan
    '#ff00ff', // magenta
    '#ffff00', // yellow
  ];

  const [screenshotToggle, setScreenshotToggle] = useState(false);

  const parseJSON = (json) => {
    let min_x = Number.MAX_VALUE;
    let max_x = Number.MIN_VALUE;
    let min_y = Number.MAX_VALUE;
    let max_y = Number.MIN_VALUE;
    let min_z = Number.MAX_VALUE;
    let max_z = Number.MIN_VALUE;

    setIntersections(
      json
        .filter((e) => 'intersection' in e)
        .map((e) => e['intersection']['position'])
    );

    setObjects(
      json
        .filter((entry) => 'obj' in entry)
        .map((obj) => {
          let type = obj['obj']['type'];

          let start_x = obj['obj']['start_x'];
          let start_y = obj['obj']['start_y'];
          let start_z = obj['obj']['start_z'];

          let scale_x = obj['obj']['scale_x'];
          let scale_y = obj['obj']['scale_y'];
          let scale_z = obj['obj']['scale_z'];

          let rotation_x = obj['obj']['rotation_x'];
          let rotation_y = obj['obj']['rotation_y'];
          let rotation_z = obj['obj']['rotation_z'];

          min_x = Math.min(min_x, start_x);
          max_x = Math.max(max_x, start_x + scale_x);
          min_y = Math.min(min_y, start_y);
          max_y = Math.max(max_y, start_y + scale_y);
          min_z = Math.min(min_z, start_z);
          max_z = Math.max(max_z, start_z + scale_z);

          return {
            type: type,
            position: [start_x, start_y, start_z],
            scale: [scale_x, scale_y, scale_z],
            rotation: [rotation_x, rotation_y, rotation_z],
          };
        })
    );

    let mid_x = (min_x + max_x) / 2;
    let mid_y = (min_y + max_y) / 2;
    let mid_z = (min_z + max_z) / 2;
    setCenter([mid_x, mid_y, mid_z]);
  };

  useEffect(() => {
    switch (scene) {
      case 'za':
        parseJSON(za_example);
        break;
      case 'mt':
        parseJSON(mt_example);
        break;
      case 'tp':
        parseJSON(tp_example);
        break;
      default:
        return;
    }
    setShowLoading(false);
  }, [scene]);

  useEffect(() => {
    let ctx = gsap.context(() => {
      if (showSideBar) {
        gsap.to('.sidebar', { left: '0', display: 'block' });
        gsap.to('.sidebar-toggle', { color: 'white', rotate: '90deg' });
        gsap.to('.sidebar-title', { display: 'block' });
      } else {
        gsap.to('.sidebar', { left: '-100%', display: 'none' });
        gsap.to('.sidebar-toggle', { color: 'black', rotate: '0' });
        gsap.to('.sidebar-title', { display: 'none' });
      }
    }, comp);
  }, [showSideBar]);

  useEffect(() => {
    if (cameraRef.current != undefined && controlRef.current != undefined) {
      let pos = center;
      pos[0] += 5;
      pos[1] += 5;
      pos[2] += 5;
      cameraRef.current.position.set(...pos);
      cameraRef.current.lookAt(...center);
      controlRef.current.reset();
    }
  }, [resetCameraToggle, center]);

  const handleGenerate = async (c) => {
    setShowLoading(true);
    await fetch('http://127.0.0.1:5000', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ complexity: c, scene: scene }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error('Failed to generate structure.');
        }
        return res.json();
      })
      .then((json) => {
        return parseJSON(json);
      })
      .catch((e) => {
        console.log(e);
      });
    setShowLoading(false);
  };

  return (
    <div className="app" ref={comp}>
      {showLoading ? <Loading></Loading> : <></>}
      <NavBar className="fixed-navbar">
        <BsFillGearFill
          className="sidebar-toggle"
          onClick={() => setShowSideBar(!showSideBar)}
        />
        <div className="sidebar-title prevent-select">Settings</div>
      </NavBar>
      <SideBar
        show={showSideBar}
        resetCamera={() => {
          setResetCameraToggle(!resetCameraToggle);
        }}
        showIntersections={showIntersections}
        setShowIntersections={setShowIntersections}
        handleGenerate={handleGenerate}
        screenshotToggle={screenshotToggle}
        setScreenshotToggle={setScreenshotToggle}
        setScene={setScene}
        bgColor={bgColor}
        setBgColor={setBgColor}
      ></SideBar>
      <Canvas shadows>
        <OrthographicCamera
          makeDefault
          ref={cameraRef}
          zoom={150}
          left={-5.2}
          right={5.2}
          top={3.9}
          bottom={-3.9}
          near={0.01}
          far={100}
          position={[5, 5, 5]}
        />
        <ambientLight></ambientLight>
        <directionalLight
          color={0xffffff}
          intensity={3.0}
          position={[-3.25, 3, 3.25]}
        />
        <Structure objects={objects} scene={scene} />
        {showIntersections && intersections != undefined ? (
          <Intersections
            intersections={intersections}
            themes={INTERSECTION_COLORS}
          />
        ) : (
          <></>
        )}
        <CanvasControl screenshotToggle={screenshotToggle} bgColor={bgColor} />
        <OrbitControls ref={controlRef} />
      </Canvas>
    </div>
  );
}

export default App;
