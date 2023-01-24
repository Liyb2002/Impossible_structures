import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

import { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { EffectComposer, SSAO } from "@react-three/postprocessing";
import { BlendFunction } from "postprocessing";
import { Stats, OrbitControls } from "@react-three/drei";
import { useEffect, useRef } from "react";
import NavBar from "react-bootstrap/NavBar";
import Spinner from "react-bootstrap/Spinner";
import { BsFillGearFill } from "react-icons/bs";
import { useThree } from "@react-three/fiber";

import { gsap } from "gsap";

import Intersections from "./components/Intersections";
import Structure from "./components/Structure";
import SideBar from "./components/Sidebar";

function Effects() {
  return (
    <EffectComposer>
      <SSAO
        blendFunction={BlendFunction.MULTIPLY}
        samples={31}
        radius={5}
        intensity={30}
      />
    </EffectComposer>
  );
}

function Loading() {
  return (
    <div
      style={{
        position: "fixed",
        width: "100vw",
        height: "100vh",
        backgroundColor: "black",
        opacity: "0.8",
        zIndex: "100",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Spinner
        animation="border"
        role="status"
        style={{ width: "3rem", height: "3rem" }}
      >
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </div>
  );
}

function CameraControl({ resetCameraToggle, screenshotToggle }) {
  const { gl, scene, camera } = useThree();
  useEffect(() => {
    if (screenshotToggle) {
      gl.render(scene, camera);
      let alink = document.createElement("a");
      alink.setAttribute("download", "canvas.png");
      alink.setAttribute(
        "href",
        gl.domElement
          .toDataURL("image/png")
          .replace("image/png", "image/octet-stream")
      );
      alink.click();
    }
  }, [screenshotToggle]);
  useEffect(() => {
    camera.position.set(5, 5, 5);
  }, [resetCameraToggle]);
}

function App() {
  const comp = useRef();
  const [beams, setBeams] = useState([]);
  const [layerIndexMap, setLayerIndexMap] = useState({});
  const [showIntersections, setShowIntersections] = useState(true);
  const [showLayers, setShowLayers] = useState(false);
  const [center, setCenter] = useState();
  const [showSideBar, setShowSideBar] = useState(false);
  const [showLoading, setShowLoading] = useState(true);
  const [enableOrbit, setEnableOrbit] = useState(true);

  const DEFAULT_LAYERS = [
    { z: 8, num_blocks: 10 },
    { z: 12, num_blocks: 10 },
  ];
  const [layers, setLayers] = useState(DEFAULT_LAYERS);

  const DEFAULT_INTERSECTIONS = [
    { layer1: 0, layer2: 1, u: 0.625, v: 0.625 },
    { layer1: 0, layer2: 1, u: 0.5, v: 0.5 },
  ];
  const [paramIntersections, setParamIntersections] = useState(
    DEFAULT_INTERSECTIONS
  );

  const DEFAULT_COLORS = ["#d88293", "#ecec51", "#584b19"];
  const COLOR_THEMES = {
    default: ["#d88293", "#ecec51", "#584b19"],
    blue: ["#0077b6", "#00b4d8", "#03045e"],
    green: ["#2d6a4f", "#74c69d", "#081c15"],
    purple: ["#9d4edd", "#e0aaff", "#3c096c"],
    orange: ["#e85d04", "#ffea00", "#6a040f"],
  };

  const LAYER_COLORS = [
    ["#0077b6", "#00b4d8", "#03045e"], // blue
    ["#e85d04", "#ffea00", "#6a040f"], // orange
    ["#9d4edd", "#e0aaff", "#3c096c"], // purple
  ];

  const INTERSECTION_COLORS = [
    "#00ffff", // cyan
    "#ff00ff", // magenta
    "#ffff00", // yellow
  ];

  const [colors, setColors] = useState(DEFAULT_COLORS);
  const selectColors = (theme) => {
    setColors(COLOR_THEMES[theme]);
  };

  const [resetCameraToggle, setResetCameraToggle] = useState(false);
  const [screenshotToggle, setScreenshotToggle] = useState(false);

  const parseJSON = (json) => {
    let min_x = Number.MAX_VALUE;
    let max_x = Number.MIN_VALUE;
    let min_y = Number.MAX_VALUE;
    let max_y = Number.MIN_VALUE;
    let min_z = Number.MAX_VALUE;
    let max_z = Number.MIN_VALUE;

    let newLayerIndexMap = {};

    setBeams(
      json
        .filter((data) => data["type"] === "beam")
        .map((obj) => {
          let start_x = obj["obj"]["start_x"];
          let start_y = obj["obj"]["start_y"];
          let start_z = obj["obj"]["start_z"];

          let scale_x = obj["obj"]["scale_x"];
          let scale_y = obj["obj"]["scale_y"];
          let scale_z = obj["obj"]["scale_z"];

          let center_x = start_x + scale_x / 2;
          let center_y = start_y + scale_y / 2;
          let center_z = start_z + scale_z / 2;

          min_x = Math.min(min_x, start_x);
          max_x = Math.max(max_x, start_x + scale_x);
          min_y = Math.min(min_y, start_y);
          max_y = Math.max(max_y, start_y + scale_y);
          min_z = Math.min(min_z, start_z);
          max_z = Math.max(max_z, start_z + scale_z);

          let layer = obj["layer"];

          if (layer !== undefined) {
            if (!(layer in newLayerIndexMap)) {
              newLayerIndexMap[layer] = Object.keys(newLayerIndexMap).length;
            }
          }

          return {
            position: [center_x, center_y, center_z],
            scale: [scale_x, scale_y, scale_z],
            layer: newLayerIndexMap[layer],
          };
        })
    );

    setLayerIndexMap(newLayerIndexMap);

    let mid = (min_x + min_y + min_z + max_x + max_y + max_z) / 6;
    setCenter(mid, mid, mid);
    // setCenter([(min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2]);
  };

  useEffect(() => {
    fetch("./src/example.json", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Example file not found.");
        }
        return res.json();
      })
      .then((json) => parseJSON(json))
      .catch((e) => {
        console.log(e);
      });
    setShowLoading(false);
  }, []);

  useEffect(() => {
    let ctx = gsap.context(() => {
      if (showSideBar) {
        gsap.to(".sidebar", { left: "0", display: "block" });
        gsap.to(".sidebar-toggle", { color: "white", rotate: "90deg" });
        gsap.to(".sidebar-title", { display: "block" });
      } else {
        gsap.to(".sidebar", { left: "-100%", display: "none" });
        gsap.to(".sidebar-toggle", { color: "black", rotate: "0" });
        gsap.to(".sidebar-title", { display: "none" });
      }
    }, comp);
  }, [showSideBar]);

  // TODO: Add form validation
  // const validate = () => {
  //   const newErrors = {layers: [], intersections: []};

  // }

  const handleGenerate = async (ls, is) => {
    setShowLoading(true);
    await fetch("http://127.0.0.1:5000/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ layers: ls, intersections: is }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to generate structure.");
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

  const handleDefault = () => {
    setLayers(DEFAULT_LAYERS);
    setParamIntersections(DEFAULT_INTERSECTIONS);
    setBeams([]);
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
        showIntersections={showIntersections}
        setShowIntersections={setShowIntersections}
        showLayers={showLayers}
        setShowLayers={setShowLayers}
        handleGenerate={handleGenerate}
        resetCameraToggle={resetCameraToggle}
        setResetCameraToggle={setResetCameraToggle}
        colors={colors}
        setColors={setColors}
        selectColors={selectColors}
        layerColors={LAYER_COLORS}
        intersectionColors={INTERSECTION_COLORS}
        screenshotToggle={screenshotToggle}
        setScreenshotToggle={setScreenshotToggle}
        intersections={paramIntersections}
        setIntersections={setParamIntersections}
        layers={layers}
        setLayers={setLayers}
        handleDefault={handleDefault}
        setBeams={setBeams}
      ></SideBar>
      <Canvas camera={{ position: [5, 5, 5], fov: 60 }}>
        <ambientLight></ambientLight>
        <Structure
          beams={beams}
          colors={colors}
          themes={LAYER_COLORS}
          showLayers={showLayers}
        />
        {showIntersections ? (
          <Intersections
            layers={layers}
            intersections={paramIntersections}
            setIntersections={setParamIntersections}
            themes={INTERSECTION_COLORS}
            setEnableOrbit={setEnableOrbit}
            showIntersections={showIntersections}
          />
        ) : (
          <></>
        )}
        {/* <Effects /> */}
        <CameraControl
          resetCameraToggle={resetCameraToggle}
          screenshotToggle={screenshotToggle}
        />
        {enableOrbit ? <OrbitControls target={center} /> : <></>}
        {/* <Stats className="fixed-stats" /> */}
      </Canvas>
    </div>
  );
}

export default App;
