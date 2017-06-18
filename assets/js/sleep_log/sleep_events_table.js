import React, { Component, PropTypes } from "react";
import moment from "moment";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { BaseEventLogTable } from "../resources_table/resource_table";

const SleepHistoryRow = props => {
  // Used to render the data from the API
  const data = props.object;

  const uuid = data.uuid;
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
      <td>
        <div className="center-icon">
          <div
            className="remove-icon"
            onClick={e =>
              props.confirmDelete(uuid, startTimeFormatted, endTimeFormatted)}
          >
            <i className="fa fa-remove fa-1x" />
          </div>
        </div>
      </td>
    </tr>
  );
};

const SleepHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Sleep - Start Time</th>
      <th>Sleep - End Time </th>
      <th className="center-source">Time Slept</th>
      <th className="center-source">Source</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);

export class SleepEntryLogTable extends BaseEventLogTable {
  constructor() {
    super();
    this.confirmDelete = this.confirmDelete.bind(this);
    this.resourceURL = "/api/v1/sleep_activities/";
  }

  confirmDelete(uuid, startTime, endTime) {
    const answer = confirm(
      `WARNING: This will delete the following Sleep Log \n\nStart: ${startTime} \nEnd: ${endTime} \n\nConfirm?`
    );

    if (answer) {
      this.deleteUUID(uuid);
    }
  }

  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <SleepHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <SleepHistoryRow
              key={key}
              object={historicalData[key]}
              confirmDelete={this.confirmDelete}
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
