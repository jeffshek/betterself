import React, { Component, PropTypes } from "react";
import moment from "moment";
import { CubeLoadingStyle } from "../animations/LoadingStyle";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { BaseEventLogTable } from "../resources_table/resource_table";

const confirmDelete = (uuid, name, eventDate) => {
  const answer = confirm(
    `WARNING: This will delete the following Activity \n\n ${name} on ${eventDate} \n\nConfirm? `
  );
  const params = {
    uuid: uuid
  };

  if (answer) {
    fetch("/api/v1/user_activity_events/", {
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
      <td>{duration_minutes}</td>
      <td>{is_significant_activity ? "True" : ""}</td>
      <td>{is_negative_activity ? "True" : ""}</td>
      <td className="center-source">
        <span className="badge badge-success">{source}</span>
      </td>
      <td>
        <div onClick={e => confirmDelete(uuid, name, timeFormatted)}>
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
      <th>Time</th>
      <th>Activity</th>
      <th>Duration Minutes</th>
      <th>Significant</th>
      <th>Negative</th>
      <th className="center-source">Source</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);

export class UserActivityEventLogTable extends BaseEventLogTable {
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
          <strong>Productivity History</strong>
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
