import React, { Component, PropTypes } from "react";
import moment from "moment";
import { CubeLoadingStyle } from "../animations/LoadingStyle";
import { BaseEventLogTable } from "../resources_table/resource_table";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import Datetime from "react-datetime";

export const TrueCheckBox = () => {
  return (
    <div className="true-icon">
      <i className="fa fa-check-circle" />
    </div>
  );
};

const UserActivityEventHistoryRow = props => {
  const data = props.object;

  const { source, time, duration_minutes, uuid } = data;
  const user_activity = data.user_activity;
  const name = user_activity.name;
  const is_negative_activity = user_activity["is_negative_activity"];
  const is_significant_activity = user_activity["is_significant_activity"];
  const timeFormatted = moment(time).format("dddd, MMMM Do YYYY, h:mm:ss a");

  return (
    <tr>
      <td>{timeFormatted}</td>
      <td>{name}</td>
      <td>{duration_minutes} minutes</td>
      <td>{is_significant_activity ? <TrueCheckBox /> : ""}</td>
      <td>{is_negative_activity ? <TrueCheckBox /> : ""}</td>
      <td className="center-source">
        <span className="badge badge-success">{source}</span>
      </td>
      <td>
        <div className="center-icon">
          <div className="edit-icon" onClick={e => props.selectModalEdit(data)}>
            <i className="fa fa-edit fa-1x" />
          </div>
          &nbsp;
          <div
            className="remove-icon"
            onClick={e => props.confirmDelete(uuid, name, timeFormatted)}
          >
            <i className="fa fa-remove fa-1x" />
          </div>
        </div>
      </td>
    </tr>
  );
};

const UserActivityEventHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Time</th>
      <th>Activity Type</th>
      <th>Duration (Minutes)</th>
      <th className="center-source">Significant</th>
      <th className="center-source">Negative</th>
      <th className="center-source">Source</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);

export class UserActivityEventLogTable extends BaseEventLogTable {
  constructor() {
    super();
    this.state = {
      modal: false,
      editObject: {
        name: null
      }
    };
    this.handleDatetimeChange = this.handleDatetimeChange.bind(this);
    this.submitEdit = this.submitEdit.bind(this);
    this.confirmDelete = this.confirmDelete.bind(this);
    this.resourceURL = "/api/v1/user_activity_events/";
  }

  handleDatetimeChange(moment) {
    let editObject = this.state.editObject;
    editObject.time = moment;

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
      name: this.state["activityName"],
      is_significant_activity: this.state["isSignificantActivity"],
      is_negative_activity: this.state["isNegativeActivity"]
    };

    this.putParamsUpdate(params);
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
            ref={input => this.activityUUID = input}
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
            name="activityName"
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
              {this.renderEditModal()}
            </div>}

      </div>
    );
  }
}
