import React, { Component, PropTypes } from "react";
import { CubeLoadingStyle } from "../animations/LoadingStyle";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { BaseEventLogTable } from "../resources_table/resource_table";
import {
  TrueCheckBox
} from "../user_activities_events/user_activities_events_table";
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from "reactstrap";

const confirmDelete = (uuid, name) => {
  const answer = confirm(
    `WARNING: This will delete the following Activity \n\n${name} \n\nConfirm? `
  );
  const params = {
    uuid: uuid
  };

  if (answer) {
    fetch("/api/v1/user_activities/", {
      method: "DELETE",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    }).then(
      // After deleting, just refresh the entire page. In the future, remove
      // from the array and setState
      location.reload()
    );
  }
};

const UserActivityEventHistoryRow = props => {
  const data = props.object;
  const { name, is_significant_activity, is_negative_activity, uuid } = data;

  return (
    <tr>
      <td>{name}</td>
      <td>{is_significant_activity ? <TrueCheckBox /> : ""}</td>
      <td>{is_negative_activity ? <TrueCheckBox /> : ""}</td>
      <td>
        <div className="center-icon">
          <div className="edit-icon" onClick={e => props.selectModalEdit(data)}>
            <i className="fa fa-edit fa-1x" />
          </div>
          &nbsp;
          <div className="remove-icon" onClick={e => confirmDelete(uuid, name)}>
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
      <th>Activity Name</th>
      <th className="center-source">Significant</th>
      <th className="center-source">Negative</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);

export class UserActivityLogTable extends BaseEventLogTable {
  constructor() {
    super();
    this.state = {
      modal: false,
      editObject: { name: null }
    };
    this.toggle = this.toggle.bind(this);
    this.selectModalEdit = this.selectModalEdit.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.submitEdit = this.submitEdit.bind(this);
  }

  toggle() {
    this.setState({
      modal: !this.state.modal
    });
  }

  selectModalEdit(object) {
    this.setState({ editObject: object });
    // Turn on modal to show for editing
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
            />
          ))}
        </tbody>
      </table>
    );
  }

  handleInputChange(event) {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  }

  submitEdit() {
    this.toggle();

    const params = {
      uuid: this.state.editObject["uuid"],
      name: this.state["activityName"],
      is_significant_activity: this.state["isSignificantActivity"],
      is_negative_activity: this.state["isNegativeActivity"]
    };

    fetch("/api/v1/user_activities/", {
      method: "PUT",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    }).then(location.reload());
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
