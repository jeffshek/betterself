import React, { Component, PropTypes } from "react";
import { CubeLoadingStyle } from "../animations/LoadingStyle";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { BaseEventLogTable } from "../resources_table/resource_table";
import {
  TrueCheckBox
} from "../user_activities_events/user_activities_events_table";

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
          <div className="edit-icon">
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
            />
          ))}
        </tbody>
      </table>
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
      </div>
    );
  }
}
