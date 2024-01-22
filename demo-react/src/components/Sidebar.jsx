import './Sidebar.css';

import Dropdown from 'react-bootstrap/Dropdown';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import { useState } from 'react';

function SideBar({
  resetCamera,
  showIntersections,
  setShowIntersections,
  handleGenerate,
  screenshotToggle,
  setScreenshotToggle,
  setScene,
  bgColor,
  setBgColor,
  errors,
}) {
  const [startX, setStartX] = useState(400);
  const [startY, setStartY] = useState(400);
  const [fgI, setFgI] = useState(3);
  const [bgI, setBgI] = useState(6);
  const [numVB, setNumVB] = useState(1);
  const [numStep, setNumStep] = useState(3);

  const handleScreenshot = () => {
    setScreenshotToggle(!screenshotToggle);
    setScreenshotToggle(!screenshotToggle);
  };

  return (
    <>
      <div className="nav-backplate" />
      <Col className="sidebar prevent-select">
        <div className="section">
          <h3 className="label">Display</h3>
          <Form className="my-3 col-7 pl-3">
            <Form.Label>Background Color</Form.Label>
            <Form.Control
              type="color"
              value={bgColor}
              onChange={(e) => setBgColor(e.target.value)}
            />
          </Form>
          <Form className="mt-2 mb-3">
            <Form.Label>Show Visual Bridges</Form.Label>
            <Form.Check
              type="switch"
              checked={showIntersections}
              onChange={(e) => {
                setShowIntersections(e.target.checked);
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
          <h3 className="label prevent-select">General</h3>
          <Form className="my-3 col-5">
            <Form.Label>Scene</Form.Label>
            <Dropdown onSelect={setScene}>
              <Dropdown.Toggle variant="outline-light">Select</Dropdown.Toggle>
              <Dropdown.Menu
                style={{ maxHeight: '175px', overflowY: 'scroll' }}
              >
                <Dropdown.Item eventKey={'za'}>Ruins</Dropdown.Item>
                <Dropdown.Item eventKey={'mt'}>Factory</Dropdown.Item>
                <Dropdown.Item eventKey={'tr'}>Branches</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </Form>
          <Form className="mt-2 mb-3">
            <Form.Label>Start Position - X ({startX})</Form.Label>
            <Form.Control
              type="range"
              min={100}
              max={600}
              step={1}
              value={startX}
              onChange={(e) => {
                setStartX(e.target.value);
              }}
            ></Form.Control>
          </Form>
          <Form className="mt-2 mb-3">
            <Form.Label>Start Position - Y ({startY})</Form.Label>
            <Form.Control
              type="range"
              min={100}
              max={600}
              step={1}
              value={startY}
              onChange={(e) => {
                setStartY(e.target.value);
              }}
            ></Form.Control>
          </Form>
          <Form className="mt-2 mb-3">
            <Form.Label>Foreground Index ({fgI})</Form.Label>
            <Form.Control
              type="range"
              min={1}
              max={4}
              step={0.1}
              value={fgI}
              onChange={(e) => {
                setFgI(e.target.value);
              }}
            ></Form.Control>
          </Form>
          <Form className="mt-2 mb-3">
            <Form.Label>Background Index ({bgI})</Form.Label>
            <Form.Control
              type="range"
              min={1}
              max={6}
              step={0.1}
              value={bgI}
              onChange={(e) => {
                setBgI(e.target.value);
              }}
              isInvalid={errors.bgi !== ''}
            ></Form.Control>
            <Form.Control.Feedback type="invalid">
              {errors.bgi}
            </Form.Control.Feedback>
          </Form>
          <Form className="mt-2 mb-3">
            <Form.Label>Number of Visual Bridges ({numVB})</Form.Label>
            <Form.Control
              type="range"
              min={1}
              max={4}
              step={1}
              value={numVB}
              onChange={(e) => {
                setNumVB(e.target.value);
              }}
              isInvalid={errors.numVB !== ''}
            ></Form.Control>
            <Form.Control.Feedback type="invalid">
              {errors.numVB}
            </Form.Control.Feedback>
          </Form>
          <Form className="mt-2 mb-3">
            <Form.Label>Number of Steps ({numStep})</Form.Label>
            <Form.Control
              type="range"
              min={3}
              max={50}
              step={1}
              value={numStep}
              onChange={(e) => {
                setNumStep(e.target.value);
              }}
            ></Form.Control>
          </Form>
        </div>
        <Col className="justify-content-around">
          <Button
            variant="outline-light"
            className="col-12 mb-5"
            onClick={() => {
              handleGenerate(startX, startY, fgI, bgI, numVB, numStep);
            }}
          >
            Generate Structure
          </Button>
        </Col>
      </Col>
    </>
  );
}

export default SideBar;
