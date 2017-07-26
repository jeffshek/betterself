import React, { Component, PropTypes } from "react";
import moment from "moment";
import { READABLE_DATE_TIME_FORMAT } from "../constants/datesAndTimes";

const MinutesToHourMinutesFormat = minutes => {
  const durationFormattedRounded = Math.floor(minutes);

  const hoursSlept = Math.floor(durationFormattedRounded / 60);
  const minutesSlept = durationFormattedRounded % 60;
  return `${hoursSlept} hours ${minutesSlept} minutes`;
};

export const SleepHistoryRow = props => {
  // Used to render the data from the API
  const data = props.object;

  const uuid = data.uuid;
  const startTime = moment(data.start_time);
  const endTime = moment(data.end_time);
  const source = data.source;

  const startTimeFormatted = startTime.format(READABLE_DATE_TIME_FORMAT);
  const endTimeFormatted = endTime.format(READABLE_DATE_TIME_FORMAT);
  const duration = moment.duration(endTime.diff(startTime));
  const durationAsMinutes = duration.asMinutes();

  const timeSlept = MinutesToHourMinutesFormat(durationAsMinutes);

  return (
    <tr>
      <td>{startTimeFormatted}</td>
      <td>{endTimeFormatted}</td>
      <td>{timeSlept}</td>
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

export const SleepHistoryTableHeader = () => (
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
