import React, { Component, PropTypes } from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import { BaseEventLogTable } from "../resources_table/resource_table";

const confirmDelete = (uuid, eventDate) => {
  const answer = confirm(
    `WARNING: This will delete the following Productivity Log \n\n${eventDate} \n\nConfirm? `
  );
  const params = {
    uuid: uuid
  };

  if (answer) {
    fetch("/api/v1/productivity_log/", {
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

const ProductivityHistoryRow = props => {
  const data = props.object;

  const veryProductiveMinutes = data.very_productive_time_minutes;
  const productiveMinutes = data.productive_time_minutes;
  const neutralMinutes = data.neutral_time_minutes;
  const distractingMinutes = data.distracting_time_minutes;
  const veryDistractingMinutes = data.very_distracting_time_minutes;
  const eventDate = data.date;
  const uuid = data.uuid;

  return (
    <tr>
      <td>{eventDate}</td>
      {/*Append minutes at any data set we have so its easier to comprehend*/}
      <td>{veryProductiveMinutes ? veryProductiveMinutes + " Minutes" : ""}</td>
      <td>{productiveMinutes ? productiveMinutes + " Minutes" : ""}</td>
      <td>{neutralMinutes ? neutralMinutes + " Minutes" : ""}</td>
      <td>{distractingMinutes ? distractingMinutes + " Minutes" : ""}</td>
      <td>
        {veryDistractingMinutes ? veryDistractingMinutes + " Minutes" : ""}
      </td>
      <td>
        <div className="center-icon">
          <div onClick={e => confirmDelete(uuid, eventDate)}>
            <div className="remove-icon">
              <i className="fa fa-remove" />
            </div>
          </div>
        </div>
      </td>
    </tr>
  );
};

const ProductivityHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Date</th>
      <th>Very Productive Time</th>
      <th>Productive Time</th>
      <th>Neutral Time</th>
      <th>Distracting Time</th>
      <th>Very Distracting Time</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);

export class ProductivityLogTable extends BaseEventLogTable {
  getTableRender() {
    const historicalData = this.props.eventHistory;
    const historicalDataKeys = Object.keys(historicalData);

    return (
      <table className="table table-bordered table-striped table-condensed">
        <ProductivityHistoryTableHeader />
        <tbody>
          {historicalDataKeys.map(key => (
            <ProductivityHistoryRow key={key} object={historicalData[key]} />
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
