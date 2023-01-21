import "./Modal.css";

import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";

import { useState, useEffect } from "react";

function LayerModal({
  show,
  onHide,
  selectedLayer,
  layers,
  setLayers,
  intersections,
  setIntersections,
}) {
  const DEFAULT_LAYER = { z: 12, num_blocks: 10 };
  const [layer, setLayer] = useState(DEFAULT_LAYER);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (show) {
      if (Number.isInteger(selectedLayer)) {
        setLayer(layers[selectedLayer]);
      } else {
        setLayer(DEFAULT_LAYER);
      }
      setErrors({});
    }
  }, [show]);

  const setField = (field, value) => {
    setLayer({ ...layer, [field]: Number(value) });
    if (!!errors[field]) {
      setErrors({ ...errors, [field]: null });
    }
  };

  const validate = () => {
    const newErrors = {};

    // Check for duplicated z index
    if (layers.some((l, i) => l.z === layer.z && i !== selectedLayer)) {
      newErrors.z = "Duplicated layers with the same z-value.";
    }

    return newErrors;
  };

  const handleDelete = () => {
    // Update affected intersections
    setIntersections(
      intersections
        .filter(
          (int) => int.layer1 != selectedLayer && int.layer2 != selectedLayer
        )
        .map((int) => {
          let newLayer1 =
            int.layer1 > selectedLayer ? int.layer1 - 1 : int.layer1;
          let newLayer2 =
            int.layer2 > selectedLayer ? int.layer2 - 1 : int.layer2;
          return { ...int, layer1: newLayer1, layer2: newLayer2 };
        })
    );

    setLayers(layers.filter((l, i) => i !== selectedLayer));

    onHide();
  };

  const handleSave = () => {
    const newErrors = validate();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      if (Number.isInteger(selectedLayer)) {
        setLayers(
          layers.map((l, i) => {
            if (i === selectedLayer) {
              return layer;
            } else {
              return l;
            }
          })
        );
      } else {
        setLayers([...layers, layer]);
      }
      onHide();
    }
  };

  return (
    <Modal show={show} onHide={onHide} size="lg" centered>
      <Modal.Header style={{ border: "none" }} closeButton>
        <Modal.Title>Edit Layer</Modal.Title>
      </Modal.Header>
      <Form className="form-container">
        <Form.Group className="mb-3" controlId="formLayerZ">
          <Form.Label>Z-Index: {layer.z}</Form.Label>
          <Form.Control
            type="range"
            min={4}
            max={20}
            step={1}
            value={layer.z}
            onChange={(e) => {
              setField("z", e.target.value);
            }}
            isInvalid={!!errors.z}
          ></Form.Control>
          <Form.Control.Feedback type="invalid">
            {errors.z}
          </Form.Control.Feedback>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formLayerNumBlocks">
          <Form.Label>Number of blocks: {layer.num_blocks}</Form.Label>
          <Form.Control
            type="range"
            min={5}
            max={15}
            step={1}
            value={layer.num_blocks}
            onChange={(e) => {
              setField("num_blocks", e.target.value);
            }}
            isInvalid={!!errors.num_blocks}
          ></Form.Control>
          <Form.Control.Feedback type="invalid">
            {errors.num_blocks}
          </Form.Control.Feedback>
        </Form.Group>
      </Form>
      <Modal.Footer style={{ border: "none" }}>
        {Number.isInteger(selectedLayer) ? (
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

export default LayerModal;
