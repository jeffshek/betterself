import React from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { Link } from "react-router-dom";
import { SupplementHistoryTableHeader, SupplementRow } from "./constants";
import { BaseEventLogTable } from "../resources_table/resource_table";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";

export class SupplementTable extends BaseEventLogTable {
  constructor() {
    super();
    this.state = {
      ready: false,
      modal: false,
      editObject: { name: null }
    };

    this.submitEdit = this.submitEdit.bind(this);
    this.confirmDelete = this.confirmDelete.bind(this);
    this.resourceURL = "/api/v1/supplements/";
  }

  componentDidMount() {
    this.getSupplements();
  }

  confirmDelete(uuid, name) {
    const answer = confirm(
      `WARNING: This will delete the following supplement \n\n${name} \n\nConfirm? `
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  }

  submitEdit() {
    const params = {
      uuid: this.state.editObject["uuid"],
      name: this.state["supplementName"]
    };

    this.putParamsUpdate(params);
    this.toggle();
  }

  getSupplements() {
    fetch(`api/v1/supplements/`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({
          supplements: responseData
        });
        this.setState({ ready: true });
      });
  }

  renderTable() {
    if (!this.state.ready) {
      return <div />;
    }

    const supplements = this.state.supplements;
    const supplementsKeys = Object.keys(supplements);

    return (
      <div className="card-block">
        <table className="table table-bordered table-striped table-condensed">
          <SupplementHistoryTableHeader />
          <tbody>
            {supplementsKeys.map(key => (
              <SupplementRow
                key={key}
                object={supplements[key]}
                selectModalEdit={this.selectModalEdit}
                confirmDelete={this.confirmDelete}
              />
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  renderEditModal() {
    return (
      <Modal isOpen={this.state.modal} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>Edit Supplement</ModalHeader>
        <ModalBody>
          <label className="form-control-label add-event-label">
            Supplement Name
          </label>
          <input
            name="supplementName"
            type="text"
            className="form-control"
            defaultValue={this.state.editObject["name"]}
            onChange={this.handleInputChange}
          />
          <br />
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.submitEdit}>Update</Button>
          <Button color="decline-modal" onClick={this.toggle}>Cancel</Button>
        </ModalFooter>
      </Modal>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Supplements</strong>
        </div>
        {this.renderTable()}
        {this.renderEditModal()}
      </div>
    );
  }
}
