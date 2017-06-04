import React, { Component, PropTypes } from "react";
import { CubeLoadingStyle } from "../animations/LoadingStyle";
import { BaseEventLogTable } from "../resources_table/resource_table";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import Datetime from "react-datetime";
import {
  UserActivityEventHistoryRow,
  UserActivityEventHistoryTableHeader
} from "./constants";

export class UserActivityEventLogTable extends BaseEventLogTable {
  constructor() {
    super();
    this.state = {
      modal: false
    };
    this.handleDatetimeChange = this.handleDatetimeChange.bind(this);
    this.submitEdit = this.submitEdit.bind(this);
    this.confirmDelete = this.confirmDelete.bind(this);
    this.resourceURL = "/api/v1/user_activity_events/";
    this.handleActivityTypeChange = this.handleActivityTypeChange.bind(this);
  }

  handleDatetimeChange(moment) {
    let editObject = this.state.editObject;
    editObject.time = moment;

    this.setState({ editObject: editObject });
  }

  handleActivityTypeChange(event) {
    const target = event.target;
    const value = target.value;

    let editObject = this.state.editObject;
    editObject["user_activity"] = this.props.userActivityTypes[value];

    this.setState({ editObject: editObject });
  }

  confirmDelete(uuid, name, eventDate) {
    const answer = confirm(
      `WARNING: This will delete the following Activity \n\n${name} on ${eventDate} \n\nConfirm?`
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  }

  submitEdit() {
    const params = {
      uuid: this.state.editObject["uuid"],
      time: this.state.editObject["time"],
      duration_minutes: this.state["durationMinutes"],
      user_activity_uuid: this.state.editObject["user_activity"].uuid
    };

    this.putParamsUpdate(params);
    this.toggle();
  }

  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <UserActivityEventHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <UserActivityEventHistoryRow
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
    const activitiesKeys = Object.keys(this.props.userActivityTypes);
    const activitiesNames = activitiesKeys.map(
      key => this.props.userActivityTypes[key].name
    );
    const indexOfActivityEditSelect = activitiesNames.indexOf(
      this.state.editObject["user_activity"].name
    );

    return (
      <Modal isOpen={this.state.modal} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>Edit Activity Type</ModalHeader>
        <ModalBody>
          <label className="add-event-label">
            Time
          </label>
          <Datetime
            onChange={this.handleDatetimeChange}
            value={this.state.editObject.time}
          />
          <br />

          <label className="form-control-label add-event-label">
            Activity Type
          </label>
          <select
            className="form-control"
            name="activityTypeIndexSelected"
            onChange={this.handleActivityTypeChange}
            value={indexOfActivityEditSelect}
          >
            {activitiesKeys.map(key => (
              <option value={key} key={key}>
                {this.props.userActivityTypes[key].name}
              </option>
            ))}
          </select>
          <br />

          <label className="form-control-label add-event-label">
            Duration (Minutes)
          </label>
          <input
            name="durationMinutes"
            type="integer"
            className="form-control"
            defaultValue={this.state.editObject["duration_minutes"]}
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
          <strong>Event History</strong>
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
        {this.state.modal ? <div> {this.renderEditModal()} </div> : <div />}
      </div>
    );
  }
}
