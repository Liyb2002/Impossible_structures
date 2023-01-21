import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const loader = new THREE.FileLoader();

//load a text file and output the result to the console
loader.load(
  // resource URL
  "./result.json",

  // onLoad callback
  function (data) {
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      75,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );

    const controls = new OrbitControls(camera, renderer.domElement);

    const geometry = new THREE.BoxGeometry(1, 1, 1).toNonIndexed();
    const material = new THREE.MeshBasicMaterial({ vertexColors: true });

    const positionAttribute = geometry.getAttribute("position");
    const colors = [];
    const color = new THREE.Color();

    var count = 0;
    for (let i = 0; i < positionAttribute.count; i += 12) {
      if (count == 0) {
        color.set(0xd88293);
      }
      if (count == 1) {
        color.set(0xecec51);
      }
      if (count == 2) {
        color.set(0x584b19);
      }
      for (let j = 0; j < 12; j++) {
        colors.push(color.r, color.g, color.b);
      }
      count += 1;
    }

    // define the new attribute
    geometry.setAttribute("color", new THREE.Float32BufferAttribute(colors, 3));

    // output the text to the console
    var jsonData = JSON.parse(data);
    var objects_num = Object.keys(jsonData).length;

    let min_x = Number.MAX_VALUE;
    let max_x = Number.MIN_VALUE;
    let min_y = Number.MAX_VALUE;
    let max_y = Number.MIN_VALUE;
    let min_z = Number.MAX_VALUE;
    let max_z = Number.MIN_VALUE;

    for (var i = 0; i < objects_num; i++) {
      let start_x = jsonData[i]["obj"]["start_x"];
      let start_y = jsonData[i]["obj"]["start_y"];
      let start_z = jsonData[i]["obj"]["start_z"];

      let scale_x = jsonData[i]["obj"]["scale_x"];
      let scale_y = jsonData[i]["obj"]["scale_y"];
      let scale_z = jsonData[i]["obj"]["scale_z"];

      let center_x = start_x + scale_x / 2;
      let center_y = start_y + scale_y / 2;
      let center_z = start_z + scale_z / 2;

      min_x = Math.min(min_x, start_x);
      max_x = Math.max(max_x, start_x + scale_x);
      min_y = Math.min(min_y, start_y);
      max_y = Math.max(max_y, start_y + scale_y);
      min_z = Math.min(min_z, start_z);
      max_z = Math.max(max_z, start_z + scale_z);

      const cube = new THREE.Mesh(geometry, material);
      cube.position.set(center_x, center_y, center_z);
      cube.scale.set(scale_x, scale_y, scale_z);

      scene.add(cube);
    }

    // let avg_mid = (min_x + min_y + min_z + max_x + max_y + max_z) / 6;
    // controls.target.set(avg_mid, avg_mid, avg_mid);

    let center = new THREE.Vector3(
      (min_x + max_x) / 2,
      (min_y + max_y) / 2,
      (min_z + max_z) / 2
    );

    controls.target = center;

    camera.position.set(5, 5, 5);
    console.log("Camera: " + camera.position.toArray());

    controls.update();

    function animate() {
      requestAnimationFrame(animate);

      // controls.update();

      renderer.render(scene, camera);
    }

    animate();
  },

  // onProgress callback
  function (xhr) {
    console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
  },

  // onError callback
  function (err) {
    console.error("An error happened");
  }
);

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  renderer.setSize(window.innerWidth, window.innerHeight);
}
