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
}) {
  const [complexity, setComplexity] = useState(1);

  const handleScreenshot = () => {
    setScreenshotToggle(!screenshotToggle);
    setScreenshotToggle(!screenshotToggle);
  };

  return (
    <>
      <Col className="sidebar">
        <div className="section">
          <h3 className="label prevent-select">Display</h3>
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
                <Dropdown.Item eventKey={'za'}>ZA Extended</Dropdown.Item>
                <Dropdown.Item eventKey={'mt'}>Matryoshka</Dropdown.Item>
                <Dropdown.Item eventKey={'tp'}>Temple</Dropdown.Item>
              </Dropdown.Menu>
            </Dropdown>
          </Form>
          <Form className="mt-2 mb-3">
            <Form.Label>Complexity ({complexity})</Form.Label>
            <Form.Control
              type="range"
              min={1}
              max={3}
              step={1}
              value={complexity}
              onChange={(e) => {
                setComplexity(e.target.value);
              }}
            ></Form.Control>
          </Form>
        </div>
        <Col className="justify-content-around">
          <Button
            variant="outline-light"
            className="col-12 mb-5"
            onClick={() => {
              handleGenerate(complexity);
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
