import React, { Component, PropTypes } from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseEventLogTable } from "../resources_table/resource_table";
import {
  SupplementHistoryRow,
  SupplementHistoryTableHeader
} from "./constants";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import Datetime from "react-datetime";

export class SupplementEntryLogTable extends BaseEventLogTable {
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
    this.handleActivityTypeChangeOnEditObject = this.handleActivityTypeChangeOnEditObject.bind(
      this
    );
    this.resourceURL = "/api/v1/supplement_events/";
  }

  handleActivityTypeChangeOnEditObject(event) {
    const target = event.target;
    const value = target.value;

    let editObject = this.state.editObject;
    editObject["supplement"] = this.props.supplements[value];

    this.setState({ editObject: editObject });
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
      name: this.state["supplementName"]
    };

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
          {/*Supplement*/}
          <label className="form-control-label add-event-label">
            Supplement
          </label>

          <select
            className="form-control"
            name="activityTypeIndexSelected"
            onChange={this.handleActivityTypeChangeOnEditObject}
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
            name="supplementName"
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
            value={this.state.editObject.time}
          />
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
          <strong>Supplement History</strong>
        </div>
        {/*Conditional loading if ready to review or not yet*/}
        {!this.props.renderReady
          ? <CubeLoadingStyle />
          : <div className="card-block">
              <div className="float-right">
                {this.getNavPaginationControlRender()}
              </div>
              {this.getTableRender()}
              {this.getNavPaginationControlRender()}
            </div>}
        {this.state.modal ? <div>{this.renderEditModal()}</div> : <div> </div>}
      </div>
    );
  }
}
