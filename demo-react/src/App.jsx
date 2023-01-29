import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

import { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { useEffect, useRef } from "react";
import NavBar from "react-bootstrap/NavBar";
import Spinner from "react-bootstrap/Spinner";
import { BsFillGearFill } from "react-icons/bs";
import { useThree } from "@react-three/fiber";

import { gsap } from "gsap";

import Intersections from "./components/Intersections";
import Structure from "./components/Structure";
import SideBar from "./components/Sidebar";

import example from "./example.json";

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
  const [showIntersections, setShowIntersections] = useState(true);
  const [showLayers, setShowLayers] = useState(false);
  const [center, setCenter] = useState();
  const [showSideBar, setShowSideBar] = useState(false);
  const [showLoading, setShowLoading] = useState(true);
  const [enableOrbit, setEnableOrbit] = useState(true);

  const DEFAULT_ERRORS = {
    layers: {},
    intersections: { layer1: {}, layer2: {} },
    general: {},
  };
  const [errors, setErrors] = useState(DEFAULT_ERRORS);

  const DEFAULT_LAYERS = [
    { z: 8, num_blocks: 10 },
    { z: 12, num_blocks: 10 },
  ];
  const [layers, setLayers] = useState(DEFAULT_LAYERS);

  const DEFAULT_INTERSECTIONS = [
    { layer1: 0, layer2: 1, u: 0.625, v: 0.625 },
    { layer1: 0, layer2: 1, u: 0.5, v: 0.5 },
  ];
  const [intersections, setIntersections] = useState(DEFAULT_INTERSECTIONS);

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

    let layerIndexMap = {};

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
            if (!(layer in layerIndexMap)) {
              layerIndexMap[layer] = Object.keys(layerIndexMap).length;
            }
          }

          return {
            position: [center_x, center_y, center_z],
            scale: [scale_x, scale_y, scale_z],
            layer: layerIndexMap[layer],
          };
        })
    );

    let mid = (min_x + min_y + min_z + max_x + max_y + max_z) / 6;
    setCenter(mid, mid, mid);
  };

  useEffect(() => {
    parseJSON(example);
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

  const validate = () => {
    const newErrors = DEFAULT_ERRORS;

    let zSet = new Set();
    layers.forEach((layer, i) => {
      if (zSet.has(layer.z)) {
        newErrors.layers = {
          ...newErrors.layers,
          [i]: "Duplicated layer with the same depth.",
        };
      } else {
        zSet.add(layer.z);
      }
    });

    intersections.forEach((int, i) => {
      if (int.layer1 === int.layer2) {
        newErrors.intersections.layer2 = {
          ...newErrors.intersections.layer2,
          [i]: "Cannot choose the same layer.",
        };
      }
      if (int.layer1 < 0) {
        newErrors.intersections.layer1 = {
          ...newErrors.intersections.layer1,
          [i]: "Please choose a valid layer.",
        };
      }
      if (int.layer2 < 0) {
        newErrors.intersections.layer2 = {
          ...newErrors.intersections.layer2,
          [i]: "Please choose a valid layer.",
        };
      }
      if (
        !(i in newErrors.intersections.layer1) &&
        !(i in newErrors.intersections.layer2) &&
        layers[int.layer1].z > layers[int.layer2].z
      ) {
        newErrors.intersections.layer2 = {
          ...newErrors.intersections.layer2,
          [i]: "This should be in the front.",
        };
      }
    });

    if (intersections.length === 0) {
      newErrors.general = "Please add at least one intersection.";
    }

    setErrors(newErrors);
    return newErrors;
  };

  const handleGenerate = async (ls, is) => {
    const newErrors = validate();
    if (
      Object.keys(newErrors.layers).length === 0 &&
      Object.keys(newErrors.intersections.layer1).length === 0 &&
      Object.keys(newErrors.intersections.layer2).length === 0 &&
      Object.keys(newErrors.general).length === 0
    ) {
      setShowLoading(true);
      await fetch(
        "https://9yn664nl68.execute-api.us-east-1.amazonaws.com/generate-structure",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({ layers: ls, intersections: is }),
        }
      )
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
    }
  };

  const handleDefault = () => {
    setLayers(DEFAULT_LAYERS);
    setIntersections(DEFAULT_INTERSECTIONS);
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
        intersections={intersections}
        setIntersections={setIntersections}
        layers={layers}
        setLayers={setLayers}
        handleDefault={handleDefault}
        setBeams={setBeams}
        errors={errors}
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
            intersections={intersections}
            setIntersections={setIntersections}
            themes={INTERSECTION_COLORS}
            setEnableOrbit={setEnableOrbit}
          />
        ) : (
          <></>
        )}
        <CameraControl
          resetCameraToggle={resetCameraToggle}
          screenshotToggle={screenshotToggle}
        />
        {enableOrbit ? <OrbitControls target={center} /> : <></>}
      </Canvas>
    </div>
  );
}

export default App;
