import React, { Component, PropTypes } from "react";
import moment from "moment";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { BaseEventLogTable } from "../resources_table/resource_table";

const confirmDelete = (uuid, supplementName, supplementTime) => {
  const answer = confirm(
    `WARNING: THIS WILL DELETE THE FOLLOWING EVENT \n\n${supplementName} at ${supplementTime}!\n\nConfirm? `
  );
  const params = {
    uuid: uuid
  };

  if (answer) {
    fetch("/api/v1/sleep_activities/", {
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

const SleepHistoryRow = props => {
  // Used to render the data from the API
  const data = props.object;

  // const uuid = data.uuid;
  const startTime = moment(data.start_time);
  const endTime = moment(data.end_time);
  const source = data.source;

  const startTimeFormatted = startTime.format("dddd, MMMM Do YYYY, h:mm:ss a");
  const endTimeFormatted = endTime.format("dddd, MMMM Do YYYY, h:mm:ss a");
  const duration = moment.duration(endTime.diff(startTime));
  const durationFormatted = duration.asMinutes();

  return (
    <tr>
      <td>{startTimeFormatted}</td>
      <td>{endTimeFormatted}</td>
      <td>{durationFormatted} minutes</td>
      <td className="center-source">
        <span className="badge badge-success">{source}</span>
      </td>
    </tr>
  );
};

const SleepHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Sleep - Start Time</th>
      <th>Sleep - End Time </th>
      <th>Time Slept</th>
      <th className="center-source">Source</th>
    </tr>
  </thead>
);

export class SleepEntryLogTable extends BaseEventLogTable {
  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <SleepHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <SleepHistoryRow key={key} object={historicalData[key]} />
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
          <strong>Sleep History</strong>
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
