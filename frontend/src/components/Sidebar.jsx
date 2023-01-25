import "./Sidebar.css";

import ListGroup from "react-bootstrap/ListGroup";
import Dropdown from "react-bootstrap/Dropdown";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import { BsTrash, BsPlus } from "react-icons/bs";

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
  intersections,
  setIntersections,
  layers,
  setLayers,
  handleDefault,
  setBeams,
  errors,
}) {
  const DEFAULT_LAYER = { z: 10, num_blocks: 10 };
  const handleAddLayer = () => {
    if (layers.length < 3) setLayers([...layers, DEFAULT_LAYER]);
  };

  const DEFAULT_INTERSECTION = {
    layer1: -1,
    layer2: -1,
    u: 0.5,
    v: 0.5,
  };
  const handleAddIntersection = () => {
    if (layers.length > 1 && intersections.length < 3)
      setIntersections([...intersections, DEFAULT_INTERSECTION]);
  };

  const handleReset = () => {
    setLayers([]);
    setIntersections([]);
    setBeams([]);
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

  const setLayerField = (index, field, value) => {
    setLayers(
      layers.map((l, i) => {
        if (i === index) {
          return { ...l, [field]: Number(value) };
        } else {
          return l;
        }
      })
    );
  };

  const handleDeleteLayer = (index) => {
    // Update affected intersections
    if (layers.length < 3) setIntersections([]);
    else
      setIntersections(
        intersections
          .filter((int) => int.layer1 != index && int.layer2 != index)
          .map((int) => {
            let newLayer1 = int.layer1 > index ? int.layer1 - 1 : int.layer1;
            let newLayer2 = int.layer2 > index ? int.layer2 - 1 : int.layer2;
            return { ...int, layer1: newLayer1, layer2: newLayer2 };
          })
      );

    setLayers(layers.filter((l, i) => i !== index));
  };

  const handleDeleteIntersection = (index) => {
    setIntersections(intersections.filter((l, i) => i !== index));
  };

  const setIntersectionField = (index, field, value) => {
    setIntersections(
      intersections.map((int, i) => {
        if (i === index) {
          return { ...int, [field]: Number(value) };
        } else {
          return int;
        }
      })
    );
  };

  return (
    <>
      <Col className="sidebar">
        <div className="section">
          <h3 className="label">Display</h3>
          <Row>
            <Form className="my-3 col-5">
              <Form.Label>Preset Color</Form.Label>
              <Dropdown onSelect={selectColors}>
                <Dropdown.Toggle variant="outline-light">
                  Select
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
            <Form className="my-3 col-7 pl-3">
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
          </Row>
          <Form className="mt-2 mb-3">
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
          <h3 className="label prevent-select">
            Layers
            <BsPlus className="add" onClick={handleAddLayer} />
          </h3>
          <ListGroup variant="flush">
            {layers.map((l, i) => {
              return (
                <ListGroup.Item
                  action
                  key={"layer-" + i}
                  style={{ color: showLayers ? layerColors[i][0] : "inherit" }}
                >
                  <Row className="mb-1">
                    <div className="col-6">
                      {"Layer " + (i + 1)}
                      <BsTrash
                        className="trash"
                        onClick={() => {
                          handleDeleteLayer(i);
                        }}
                      />
                    </div>
                    <div className="col-6" style={{ textAlign: "right" }}>
                      {" (depth = " + layers[i].z + ")"}
                    </div>
                  </Row>
                  <Form.Group className="mb-3" controlId="formLayerZ">
                    <Form.Control
                      type="range"
                      min={6}
                      max={14}
                      step={1}
                      value={layers[i].z}
                      onChange={(e) => {
                        setLayerField(i, "z", e.target.value);
                      }}
                      isInvalid={i in errors.layers}
                    ></Form.Control>
                    <Form.Control.Feedback type="invalid">
                      {errors.layers[i]}
                    </Form.Control.Feedback>
                  </Form.Group>
                </ListGroup.Item>
              );
            })}
          </ListGroup>
        </div>
        <div className="section">
          <h3 className="label prevent-select">
            Intersections
            <BsPlus className="add" onClick={handleAddIntersection} />
          </h3>
          <ListGroup variant="flush">
            {intersections.map((int, i) => {
              return (
                <ListGroup.Item
                  action
                  key={"intersection-" + i}
                  style={{
                    color: showIntersections
                      ? intersectionColors[i]
                      : "inherit",
                  }}
                >
                  <div className="mb-1">
                    {"Intersection " + (i + 1)}
                    <BsTrash
                      className="trash"
                      onClick={() => {
                        handleDeleteIntersection(i);
                      }}
                    />
                  </div>
                  <Row>
                    <Form.Group
                      className="mb-3 col-6"
                      controlId="formIntersectionLayer1"
                    >
                      <Form.Label className="small">First Layer:</Form.Label>
                      <Form.Select
                        value={int.layer1}
                        onChange={(e) =>
                          setIntersectionField(i, "layer1", e.target.value)
                        }
                        isInvalid={i in errors.intersections.layer1}
                      >
                        <option value={-1}>Select</option>
                        {layers.map((l, i) => (
                          <option key={"layer1-option-" + i} value={i}>
                            {"Layer " + (i + 1)}
                          </option>
                        ))}
                      </Form.Select>
                      <Form.Control.Feedback type="invalid">
                        {errors.intersections.layer1[i]}
                      </Form.Control.Feedback>
                    </Form.Group>
                    <Form.Group
                      className="mb-3 col-6"
                      controlId="formIntersectionLayer2"
                    >
                      <Form.Label className="small">Second Layer:</Form.Label>
                      <Form.Select
                        value={int.layer2}
                        onChange={(e) =>
                          setIntersectionField(i, "layer2", e.target.value)
                        }
                        isInvalid={i in errors.intersections.layer2}
                      >
                        <option value={-1}>Select</option>
                        {layers.map((l, i) => (
                          <option key={"layer2-option-" + i} value={i}>
                            {"Layer " + (i + 1)}
                          </option>
                        ))}
                      </Form.Select>
                      <Form.Control.Feedback type="invalid">
                        {errors.intersections.layer2[i]}
                      </Form.Control.Feedback>
                    </Form.Group>
                  </Row>
                </ListGroup.Item>
              );
            })}
            {layers.length < 2 ? (
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
            className="col-12 mb-5"
            onClick={() => {
              handleGenerate(layers, intersections);
              resetCamera();
            }}
            disabled
          >
            Generate Structure
          </Button>
        </Col>
      </Col>
    </>
  );
}

export default SideBar;
