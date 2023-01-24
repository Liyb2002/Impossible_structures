import "./Modal.css";

import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";

import { useState, useEffect } from "react";

function IntersectionModal({
  show,
  onHide,
  layers,
  selectedIntersection,
  intersections,
  setIntersections,
}) {
  const DEFAULT_INTERSECTION = {
    layer1: -1,
    layer2: -1,
    u: 0.5,
    v: 0.5,
  };
  const [intersection, setIntersection] = useState(DEFAULT_INTERSECTION);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (show) {
      if (Number.isInteger(selectedIntersection)) {
        setIntersection(intersections[selectedIntersection]);
      } else {
        setIntersection(DEFAULT_INTERSECTION);
      }
      setErrors({});
    }
  }, [show]);

  const setField = (field, value) => {
    setIntersection({ ...intersection, [field]: Number(value) });
    if (!!errors[field]) {
      setErrors({ ...errors, [field]: null });
    }
  };

  const validate = () => {
    const { layer1, layer2, u, v } = intersection;
    const newErrors = {};

    // Check for layer selection
    if (layer1 < 0) newErrors.layer1 = "Please select a layer.";
    if (layer2 < 0) newErrors.layer2 = "Please select a layer.";
    if (layer1 >= 0 && layer1 === layer2)
      newErrors.layer2 = "Cannot select the same layer to connect.";

    // Check for duplicated intersections
    if (
      intersections.some(
        (int, i) =>
          int.layer1 === layer1 &&
          int.layer2 === layer2 &&
          int.u === u &&
          int.v === v &&
          i !== selectedIntersection
      )
    )
      newErrors.xy = "Duplicated intersections with the same xy coordinate.";

    return newErrors;
  };

  const handleDelete = () => {
    setIntersections(
      intersections.filter((l, i) => i !== selectedIntersection)
    );
    onHide();
  };

  const handleSave = () => {
    const newErrors = validate();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      if (Number.isInteger(selectedIntersection)) {
        setIntersections(
          intersections.map((int, i) => {
            if (i === selectedIntersection) {
              return intersection;
            } else {
              return int;
            }
          })
        );
      } else {
        setIntersections([...intersections, intersection]);
      }
      onHide();
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" centered>
      <Modal.Header style={{ border: "none" }} closeButton>
        <Modal.Title>Edit Intersection</Modal.Title>
      </Modal.Header>
      <Form className="form-container">
        <Form.Group className="mb-3" controlId="formIntersectionLayer1">
          <Form.Label>Layer 1: </Form.Label>
          <Form.Select
            value={intersection.layer1}
            onChange={(e) => setField("layer1", e.target.value)}
            isInvalid={!!errors.layer1}
          >
            <option value={-1}>Select Layer</option>
            {layers.map((l, i) => (
              <option key={"layer1-option-" + i} value={i}>
                {"Layer " + (i + 1) + " ( z = " + l.z + " )"}
              </option>
            ))}
          </Form.Select>
          <Form.Control.Feedback type="invalid">
            {errors.layer1}
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formIntersectionLayer2">
          <Form.Label>Layer 2: </Form.Label>
          <Form.Select
            value={intersection.layer2}
            onChange={(e) => setField("layer2", e.target.value)}
            isInvalid={!!errors.layer2}
          >
            <option value={-1}>Select Layer</option>
            {layers.map((l, i) => (
              <option key={"layer1-option-" + i} value={i}>
                {"Layer " + (i + 1) + " ( z = " + l.z + " )"}
              </option>
            ))}
          </Form.Select>
          <Form.Control.Feedback type="invalid">
            {errors.layer2}
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formIntersectionX">
          <Form.Label>
            X-Intersect: {Math.round(intersection.u * 800)}
          </Form.Label>
          <Form.Control
            type="range"
            min={0}
            max={800}
            step={1}
            value={intersection.u * 800}
            onChange={(e) => {
              setField("u", e.target.value / 800);
            }}
            isInvalid={!!errors.xy}
          ></Form.Control>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formIntersectionY">
          <Form.Label>
            Y-Intersect: {Math.round(intersection.v * 800)}
          </Form.Label>
          <Form.Control
            type="range"
            min={0}
            max={800}
            step={1}
            value={intersection.v * 800}
            onChange={(e) => {
              setField("v", e.target.value / 800);
            }}
            isInvalid={!!errors.xy}
          ></Form.Control>
          <Form.Control.Feedback type="invalid">
            {errors.xy}
          </Form.Control.Feedback>
        </Form.Group>
      </Form>
      <Modal.Footer style={{ border: "none" }}>
        {Number.isInteger(selectedIntersection) ? (
          <Button variant="outline-light" onClick={handleDelete}>
            Delete
          </Button>
        ) : (
          <></>
        )}
        <Button variant="outline-light" onClick={handleSave}>
          Save
        </Button>
      </Modal.Footer>
    </Modal>
  );
}

export default IntersectionModal;
