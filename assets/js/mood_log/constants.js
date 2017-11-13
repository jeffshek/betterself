import React from "react";
import moment from "moment";
import { READABLE_DATE_TIME_FORMAT } from "../constants/dates_and_times";

export const MoodHistoryRow = props => {
  // Used to render the data from the API
  const data = props.object;
  const { uuid, time, value, notes, source } = data;
  const timeFormatted = moment(time).format(READABLE_DATE_TIME_FORMAT);

  return (
    <tr>
      <td>{timeFormatted}</td>
      <td>{value}</td>
      <td>{notes}</td>
      <td className="center-source">
        <span className="badge badge-success">{source}</span>
      </td>
      <td>
        <div className="center-icon">
          <div
            className="remove-icon"
            onClick={e =>
              props.confirmDelete(uuid, timeFormatted, value, notes)}
          >
            <i className="fa fa-remove fa-1x" />
          </div>
        </div>
      </td>
    </tr>
  );
};

export const MoodHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Time</th>
      <th>Mood Value</th>
      <th className="center-source">Notes</th>
      <th className="center-source">Source</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);
