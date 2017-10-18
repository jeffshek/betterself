import React from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseLogTable } from "../resources_table/resource_table";
import {
  SupplementHistoryRow,
  SupplementHistoryTableHeader
} from "./constants";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import Datetime from "react-datetime";
import moment from "moment";

export class SupplementLogTable extends BaseLogTable {
  constructor() {
    super();

    this.state = {
      modal: false,
      editObject: {
        supplement: null,
        time: null,
        servingSize: null
      }
    };

    this.submitEdit = this.submitEdit.bind(this);
    this.confirmDelete = this.confirmDelete.bind(this);
    this.handleSupplementChangeOnEditObject = this.handleSupplementChangeOnEditObject.bind(
      this
    );
    this.resourceURL = "/api/v1/supplement_events/";
  }

  handleSupplementChangeOnEditObject(event) {
    const target = event.target;
    const value = target.value;

    const updatedSupplement = this.props.supplements[value];

    this.state.editObject["supplement_name"] = updatedSupplement.name;
    this.state.editObject["supplement_uuid"] = updatedSupplement.uuid;

    this.setState({ editObject: this.state.editObject });
  }

  confirmDelete = (uuid, supplementName, supplementTime) => {
    const answer = confirm(
      `WARNING: THIS WILL DELETE THE FOLLOWING EVENT \n\n${supplementName} at ${supplementTime}!\n\nConfirm? `
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  };

  submitEdit() {
    const params = {
      uuid: this.state.editObject["uuid"],
      quantity: this.state["servingSizeUpdate"],
      time: this.state.editObject["time"]
    };

    if (this.state.editObject["supplement_uuid"]) {
      params["supplement_uuid"] = this.state.editObject["supplement_uuid"];
    }

    this.putParamsUpdate(params);
    this.toggle();
  }

  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <SupplementHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <SupplementHistoryRow
              key={key}
              object={historicalData[key]}
              confirmDelete={this.confirmDelete}
              selectModalEdit={this.selectModalEdit}
            />
          ))}
        </tbody>
      </table>
    );
  }

  renderEditModal() {
    if (!this.state.modal) {
      return <div />;
    }

    const supplementKeys = Object.keys(this.props.supplements);
    const supplementNames = supplementKeys.map(
      key => this.props.supplements[key].name
    );
    const indexOfSupplementSelected = supplementNames.indexOf(
      this.state.editObject["supplement_name"]
    );

    return (
      <Modal isOpen={this.state.modal} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>Edit Supplement</ModalHeader>
        <ModalBody>
          <label className="form-control-label add-event-label">
            Supplement
          </label>
          <select
            className="form-control"
            name="activityTypeIndexSelected"
            onChange={this.handleSupplementChangeOnEditObject}
            value={indexOfSupplementSelected}
          >
            {supplementKeys.map(key => (
              <option value={key} key={key}>
                {this.props.supplements[key].name}
              </option>
            ))}
          </select>
          <br />
          <label className="form-control-label add-event-label">
            Serving Size
          </label>
          <input
            name="servingSizeUpdate"
            type="text"
            className="form-control"
            defaultValue={this.state.editObject["quantity"]}
            onChange={this.handleInputChange}
          />
          <br />
          <label className="form-control-label add-event-label">
            Time
          </label>
          <Datetime
            onChange={this.handleDatetimeChangeOnEditObject}
            defaultValue={moment(this.state.editObject.time)}
          />
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.submitEdit}>Update</Button>
          <Button color="decline-modal" onClick={this.toggle}>Cancel</Button>
        </ModalFooter>
      </Modal>
    );
  }

  renderReady() {
    if (!this.props.renderReady) {
      return <CubeLoadingStyle />;
    }
    return (
      <div className="card-block">
        <div className="float-right">
          {this.getNavPaginationControlRender()}
        </div>
        {this.getTableRender()}
        {this.getNavPaginationControlRender()}
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <i className="fa fa-align-justify" />
          <strong>Supplement History</strong>
        </div>
        {this.renderReady()}
        {this.renderEditModal()}
      </div>
    );
  }
}
