import React from "react";
import { TrueCheckBox } from "../constants/designs";
import moment from "moment";
import { READABLE_DATE_TIME_FORMAT } from "../constants/dates_and_times";

export const UserActivityEventHistoryRow = props => {
  const data = props.object;

  const { source, time, duration_minutes, uuid } = data;
  const user_activity = data.user_activity;
  const name = user_activity.name;
  const is_negative_activity = user_activity["is_negative_activity"];
  const is_significant_activity = user_activity["is_significant_activity"];
  const is_all_day_activity = user_activity["is_all_day_activity"];
  const timeFormatted = moment(time).format(READABLE_DATE_TIME_FORMAT);

  return (
    <tr>
      <td>{timeFormatted}</td>
      <td>{name}</td>
      <td>{duration_minutes} minutes</td>
      <td>{is_significant_activity ? <TrueCheckBox /> : <div />}</td>
      <td>{is_negative_activity ? <TrueCheckBox /> : <div />}</td>
      <td>{is_all_day_activity ? <TrueCheckBox /> : <div />}</td>
      <td className="center-source">
        <span className="badge badge-success">{source}</span>
      </td>
      <td>
        <div className="center-icon">
          <div className="edit-icon" onClick={e => props.selectModalEdit(data)}>
            <i className="fa fa-edit fa-1x" />
          </div>
          &nbsp;
          <div
            className="remove-icon"
            onClick={e => props.confirmDelete(uuid, name, timeFormatted)}
          >
            <i className="fa fa-remove fa-1x" />
          </div>
        </div>
      </td>
    </tr>
  );
};

export const UserActivityEventHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Time</th>
      <th>Activity Type</th>
      <th>Duration (Minutes)</th>
      <th className="center-source">Significant</th>
      <th className="center-source">Negative</th>
      <th className="center-source">All Day</th>
      <th className="center-source">Source</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);
