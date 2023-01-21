import "./Sidebar.css";

import LayerModal from "./LayerModal";
import IntersectionModal from "./IntersectionModal";

import ListGroup from "react-bootstrap/ListGroup";
import Dropdown from "react-bootstrap/Dropdown";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { useState } from "react";

function SideBar({
  showIntersections,
  setShowIntersections,
  showLayers,
  setShowLayers,
  handleGenerate,
  resetCameraToggle,
  setResetCameraToggle,
  colors,
  setColors,
  selectColors,
  layerColors,
  intersectionColors,
  screenshotToggle,
  setScreenshotToggle,
}) {
  const DEFAULT_LAYERS = [
    { z: 8, num_blocks: 10 },
    { z: 12, num_blocks: 10 },
  ];
  const [layers, setLayers] = useState(DEFAULT_LAYERS);

  const DEFAULT_INTERSECTIONS = [
    { layer1: 0, layer2: 1, x: 500, y: 500 },
    { layer1: 0, layer2: 1, x: 400, y: 400 },
  ];
  const [intersections, setIntersections] = useState(DEFAULT_INTERSECTIONS);

  const [showLayerModal, setShowLayerModal] = useState(false);
  const [selectedLayer, setSelectedLayer] = useState();
  const handleEditLayer = (index) => {
    setSelectedLayer(index);
    setShowLayerModal(true);
  };

  const [showIntersectionModal, setShowIntersectionModal] = useState(false);
  const [selectedIntersection, setSelectedIntersection] = useState();
  const handleEditIntersection = (index) => {
    setSelectedIntersection(index);
    setShowIntersectionModal(true);
  };

  const handleReset = () => {
    setLayers([]);
    setIntersections([]);
  };

  const handleDefault = () => {
    setLayers(DEFAULT_LAYERS);
    setIntersections(DEFAULT_INTERSECTIONS);
  };

  const handleEditColor = (index, e) => {
    setColors(
      colors.map((c, i) => {
        if (i == index) {
          return e.target.value;
        } else {
          return c;
        }
      })
    );
  };

  const resetCamera = () => {
    setResetCameraToggle(!resetCameraToggle);
  };

  const handleScreenshot = () => {
    setScreenshotToggle(!screenshotToggle);
    setScreenshotToggle(!screenshotToggle);
  };

  return (
    <>
      <Col className="sidebar">
        <div className="section">
          <h3 className="label">Display</h3>
          <Form className="my-3">
            <Form.Label>Preset Color</Form.Label>
            <Dropdown onSelect={selectColors}>
              <Dropdown.Toggle variant="outline-light">
                Select Theme
              </Dropdown.Toggle>
              <Dropdown.Menu
                style={{ maxHeight: "175px", overflowY: "scroll" }}
              >
                <Dropdown.Item eventKey={"default"}>Default</Dropdown.Item>
                <Dropdown.Item eventKey={"blue"}>Blue</Dropdown.Item>
                <Dropdown.Item eventKey={"green"}>Green</Dropdown.Item>
                <Dropdown.Item eventKey={"purple"}>Purple</Dropdown.Item>
                <Dropdown.Item eventKey={"orange"}>Orange</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </Form>
          <Form className="my-3">
            <Form.Label>Color Palette</Form.Label>
            <Row style={{ margin: "0" }}>
              <Form.Control
                type="color"
                value={colors[0]}
                onChange={(e) => handleEditColor(0, e)}
              />
              <Form.Control
                type="color"
                value={colors[1]}
                onChange={(e) => handleEditColor(1, e)}
              />
              <Form.Control
                type="color"
                value={colors[2]}
                onChange={(e) => handleEditColor(2, e)}
              />
            </Row>
          </Form>
          <Form className="my-3">
            <Form.Label>Show Intersections</Form.Label>
            <Form.Check
              type="switch"
              checked={showIntersections}
              onChange={(e) => {
                setShowIntersections(e.target.checked);
              }}
            />
          </Form>
          <Form className="my-3">
            <Form.Label>Show Layers</Form.Label>
            <Form.Check
              type="switch"
              checked={showLayers}
              onChange={(e) => {
                setShowLayers(e.target.checked);
              }}
            />
          </Form>
          <Button
            variant="outline-light"
            className="col-12 mb-3"
            onClick={resetCamera}
          >
            Reset Camera
          </Button>
          <Button
            variant="outline-light"
            className="col-12 mb-3"
            onClick={handleScreenshot}
          >
            Save Screenshot
          </Button>
        </div>
        <div className="divider" />
        <div className="section">
          <h3 className="label">Layers</h3>
          <ListGroup variant="flush">
            {layers.map((l, i) => {
              return (
                <ListGroup.Item
                  action
                  key={"layer-" + i}
                  onClick={() => handleEditLayer(i)}
                  style={{ color: showLayers ? layerColors[i][0] : "inherit" }}
                >
                  {"Layer " + (i + 1)}
                </ListGroup.Item>
              );
            })}
            {layers.length < 3 ? (
              <ListGroup.Item action onClick={() => handleEditLayer(null)}>
                Add Layer...
              </ListGroup.Item>
            ) : (
              <></>
            )}
          </ListGroup>
        </div>
        <div className="section">
          <h3 className="label">Intersections</h3>
          <ListGroup variant="flush">
            {intersections.map((l, i) => {
              return (
                <ListGroup.Item
                  action
                  key={"intersection-" + i}
                  onClick={() => handleEditIntersection(i)}
                  style={{
                    color: showIntersections
                      ? intersectionColors[i]
                      : "inherit",
                  }}
                >
                  {"Intersection " + (i + 1)}
                </ListGroup.Item>
              );
            })}
            {layers.length > 1 && intersections.length < 3 ? (
              <ListGroup.Item
                action
                onClick={() => handleEditIntersection(null)}
              >
                Add Intersection...
              </ListGroup.Item>
            ) : intersections.length < 3 ? (
              <ListGroup.Item disabled>
                {"<Need at least 2 layers to create an intersection>"}
              </ListGroup.Item>
            ) : (
              <></>
            )}
          </ListGroup>
        </div>
        <Col className="justify-content-around">
          <Button
            variant="outline-light"
            className="col-12 mb-3"
            onClick={handleReset}
          >
            Reset Config
          </Button>
          <Button
            variant="outline-light"
            className="col-12 mb-3"
            onClick={handleDefault}
          >
            Default Config
          </Button>
          <Button
            variant="outline-light"
            className="col-12 mb-3"
            onClick={() => {
              handleGenerate(layers, intersections);
              resetCamera();
            }}
          >
            Generate Structure
          </Button>
        </Col>
      </Col>
      <LayerModal
        show={showLayerModal}
        onHide={() => setShowLayerModal(false)}
        selectedLayer={selectedLayer}
        layers={layers}
        setLayers={setLayers}
        intersections={intersections}
        setIntersections={setIntersections}
      />
      <IntersectionModal
        show={showIntersectionModal}
        onHide={() => setShowIntersectionModal(false)}
        layers={layers}
        selectedIntersection={selectedIntersection}
        intersections={intersections}
        setIntersections={setIntersections}
      />
    </>
  );
}

export default SideBar;
