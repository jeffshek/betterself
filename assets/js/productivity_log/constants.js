import React, { Component, PropTypes } from "react";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";
import { BaseEventLogTable } from "../resources_table/resource_table";
import {
  DISTRACTING_MINUTES_VARIABLE,
  NEUTRAL_MINUTES_VARIABLE,
  PRODUCTIVE_MINUTES_VARIABLE,
  VERY_DISTRACTING_MINUTES_VARIABLE,
  VERY_PRODUCTIVE_MINUTES_VARIABLE
} from "../constants/productivity";

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

export const ProductivityHistoryRow = props => {
  const data = props.object;

  const veryProductiveMinutes = data[VERY_PRODUCTIVE_MINUTES_VARIABLE];
  const productiveMinutes = data[PRODUCTIVE_MINUTES_VARIABLE];
  const neutralMinutes = data[NEUTRAL_MINUTES_VARIABLE];
  const distractingMinutes = data[DISTRACTING_MINUTES_VARIABLE];
  const veryDistractingMinutes = data[VERY_DISTRACTING_MINUTES_VARIABLE];
  const eventDate = data.date;
  const uuid = data.uuid;

  // TODO - Switch the minutes out to something that formats out to hours/mintutes
  // and looks cleaner than the current logic

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

export const ProductivityHistoryTableHeader = () => (
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
