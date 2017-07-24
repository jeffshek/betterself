import React, { Component, PropTypes } from "react";
import moment from "moment";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";

export const SupplementHistoryRow = props => {
  // Used to render the data from the API
  const data = props.object;

  const uuid = data.uuid;
  const supplementName = data.supplement_name;
  const servingSize = data.quantity;
  const source = data.source;
  const supplementTime = data.time;
  // const duration = data.duration_minutes;
  const timeFormatted = moment(supplementTime).format(
    "dddd, MMMM Do YYYY, h:mm:ss a"
  );

  return (
    <tr>
      <td>{supplementName}</td>
      <td>{servingSize}</td>
      <td>{timeFormatted}</td>
      {/*<td>{duration}</td>*/}
      <td className="center-source">
        <div
          onClick={e =>
            props.confirmDelete(uuid, supplementName, timeFormatted)}
        >
          <div className="remove-icon">
            <i className="fa fa-remove" />
          </div>
        </div>
      </td>
      <td className="center-source">
        <span className="badge badge-success">{source}</span>
      </td>
    </tr>
  );
};

export const SupplementHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Supplement</th>
      <th>Serving Size</th>
      <th>Supplement Time</th>
      {/*<th>Duration (Minutes)</th>*/}
      <th className="center-source">Actions</th>
      <th className="center-source">Source</th>
    </tr>
  </thead>
);
