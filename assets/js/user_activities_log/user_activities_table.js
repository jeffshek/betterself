import React from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseLogTable } from "../resources_table/resource_table";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import {
  UserActivityHistoryRow,
  UserActivityHistoryTableHeader
} from "./constants";
import { USER_ACTIVITIES_RESOURCE_URL } from "../constants/api_urls";

export class UserActivityLogTable extends BaseLogTable {
  constructor() {
    super();
    this.state = {
      modal: false,
      editObject: { name: null }
    };

    this.resourceURL = USER_ACTIVITIES_RESOURCE_URL;
  }

  confirmDelete = (uuid, name) => {
    const answer = confirm(
      `WARNING: This will delete the following Activity \n\n${name} \n\nConfirm? `
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  };

  submitEdit = () => {
    const params = {
      uuid: this.state.editObject["uuid"],
      name: this.state["activityName"],
      is_significant_activity: this.state["isSignificantActivity"],
      is_negative_activity: this.state["isNegativeActivity"],
      is_all_day_activity: this.state["isAllDayActivity"]
    };

    this.putParamsUpdate(params);
    this.toggle();
  };

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
          <br />
          <label className="form-control-label add-event-label">
            Is All Day
          </label>
          <select
            name="isAllDayActivity"
            className="form-control"
            size="1"
            defaultValue={this.state.editObject["is_all_day_activity"]}
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
          <strong>Activities List</strong>
        </div>
        {this.renderReady()}
        {this.renderEditModal()}
      </div>
    );
  }
}
