import React, { Component, PropTypes } from "react";
import { CubeLoadingStyle } from "../animations/LoadingStyle";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { BaseEventLogTable } from "../resources_table/resource_table";

const confirmDelete = (uuid, name) => {
  const answer = confirm(
    `WARNING: This will delete the following Activity \n\n ${name} \n\nConfirm? `
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
      <td>{is_significant_activity ? "True" : ""}</td>
      <td>{is_negative_activity ? "True" : ""}</td>
      <td>
        <div onClick={e => confirmDelete(uuid, name)}>
          <div className="remove-icon">
            <i className="fa fa-remove" />
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
      <th>Significant</th>
      <th>Negative</th>
      <th><center>Actions</center></th>
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
