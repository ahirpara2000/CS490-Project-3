import React from "react";
import { Button, Modal } from "react-bootstrap";
import PropTypes from "prop-types";

export function View({ list, show, onHide, toggleUpdate }) {
  return (
    <Modal show={show} onHide={onHide} backdrop="static" keyboard={false}>
      <Modal.Header closeButton>
        <Modal.Title>Details</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div>
          Amount:
          {list.amount}
        </div>
        <div>
          Date:
          {list.date}
        </div>
        <div>
          Location:
          {list.location}
        </div>
        <div>
          Description:
          {list.description}
        </div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={toggleUpdate}>
          Update
        </Button>
      </Modal.Footer>
    </Modal>
  );
}
View.propTypes = {
  show: PropTypes.bool,
  updateData: PropTypes.instanceOf(Array),
  onHide: PropTypes.bool,
  toggleUpdate: PropTypes.bool,
  list: PropTypes.instanceOf(Array),
};
View.defaultProps = {
  show: PropTypes.bool,
  updateData: PropTypes.instanceOf(Array),
  onHide: PropTypes.bool,
  toggleUpdate: PropTypes.bool,
  list: PropTypes.instanceOf(Array),
};
export default View;
