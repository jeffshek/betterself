import React, { Component } from "react";
import { CreateSupplementThenReload } from "./constants";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";

export class AddSupplementModal extends Component {
  constructor({}) {
    super();

    this.state = {
      supplementName: null
    };
  }

  componentWillReceiveProps(props) {
    const { defaultSupplementName } = props;
    if (defaultSupplementName) {
      this.setState({ supplementName: defaultSupplementName });
    }
  }

  handleInputChange = event => {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  };

  createSupplement = () => {
    CreateSupplementThenReload(this.state.supplementName);
  };

  render() {
    if (!this.props.showModal) {
      return <div />;
    }

    return (
      <Modal isOpen={this.props.showModal} toggle={this.props.toggleModal}>
        <ModalHeader toggle={this.props.toggleModal}>
          Create New Supplement
        </ModalHeader>
        <ModalBody>
          <div>
            <label><strong>Supplement Name</strong></label>
            <input
              type="text"
              name="supplementName"
              className="form-control"
              // Passed from whatever was put in the add Supplement Log
              defaultValue={this.props.defaultSupplementName}
              onChange={this.handleInputChange}
            />
          </div>
        </ModalBody>
        <ModalFooter>
          <Button color="decline-modal" onClick={this.props.toggleModal}>
            Cancel
          </Button>
          <Button color="primary" onClick={this.createSupplement}>
            Create
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}
