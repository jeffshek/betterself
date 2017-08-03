import React from "react";
import { READABLE_TIME_FORMAT } from "../constants/dates_and_times";
import moment from "moment";

export const TableRow = props => {
  const { details } = props;
  const timeMoment = moment(details.time);
  const timeMomentFormatted = timeMoment.format(READABLE_TIME_FORMAT);
  return (
    <tr>
      <td>{timeMomentFormatted}</td>
      <td>{details.supplement_name}</td>
    </tr>
  );
};

export const minutesToHours = minutes => {
  return (minutes / 60).toFixed(2);
};

export const dateFilter = (result, dateString) => {
  if (result.date === dateString) {
    return result;
  }
};
