import React, { Component, PropTypes } from "react";
import { CubeLoadingStyle } from "../animations/loading_styles";
import { BaseEventLogTable } from "../resources_table/resource_table";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import {
  UserActivityHistoryRow,
  UserActivityHistoryTableHeader
} from "./constants";

export class UserActivityLogTable extends BaseEventLogTable {
  constructor() {
    super();
    this.state = {
      modal: false,
      editObject: { name: null }
    };

    this.submitEdit = this.submitEdit.bind(this);
    this.confirmDelete = this.confirmDelete.bind(this);
    this.resourceURL = "/api/v1/user_activities/";
  }

  confirmDelete(uuid, name) {
    const answer = confirm(
      `WARNING: This will delete the following Activity \n\n${name} \n\nConfirm? `
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  }

  submitEdit() {
    const params = {
      uuid: this.state.editObject["uuid"],
      name: this.state["activityName"],
      is_significant_activity: this.state["isSignificantActivity"],
      is_negative_activity: this.state["isNegativeActivity"]
    };

    this.putParamsUpdate(params);
    this.toggle();
  }

  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <UserActivityHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <UserActivityHistoryRow
              key={key}
              object={historicalData[key]}
              selectModalEdit={this.selectModalEdit}
              confirmDelete={this.confirmDelete}
            />
          ))}
        </tbody>
      </table>
    );
  }

  renderEditModal() {
    return (
      <Modal isOpen={this.state.modal} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>Edit Activity Type</ModalHeader>
        <ModalBody>
          <label className="form-control-label add-event-label">
            Activity Name
          </label>
          <input
            name="activityName"
            type="text"
            className="form-control"
            defaultValue={this.state.editObject["name"]}
            onChange={this.handleInputChange}
          />
          <br />

          <label className="form-control-label add-event-label">
            Is Significant
          </label>
          <select
            name="isSignificantActivity"
            className="form-control"
            size="1"
            defaultValue={this.state.editObject["is_significant_activity"]}
            onChange={this.handleInputChange}
          >
            <option value={true}>True</option>
            <option value={false}>False</option>
          </select>
          <br />

          <label className="form-control-label add-event-label">
            Is Negative
          </label>
          <select
            name="isNegativeActivity"
            className="form-control"
            size="1"
            defaultValue={this.state.editObject["is_negative_activity"]}
            onChange={this.handleInputChange}
          >
            <option value={true}>True</option>
            <option value={false}>False</option>
          </select>

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
          <strong>Activities List</strong>
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
        {this.renderEditModal()}
      </div>
    );
  }
}
