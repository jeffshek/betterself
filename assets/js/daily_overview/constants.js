import React from "react";
import { READABLE_TIME_FORMAT } from "../constants/dates_and_times";
import moment from "moment";
import { Link } from "react-router-dom";
import { getSupplementOverviewURLFromUUID } from "../routing/routing_utils";

export const SupplementTableRow = props => {
  const { details } = props;
  const timeMoment = moment(details.time);
  const timeMomentFormatted = timeMoment.format(READABLE_TIME_FORMAT);
  const supplementOverviewLink = getSupplementOverviewURLFromUUID(
    details.supplement_uuid
  );

  return (
    <tr>
      <td>{timeMomentFormatted}</td>
      <td>
        <Link to={supplementOverviewLink}>{details.supplement_name}</Link>
      </td>
      <td>{details.quantity}</td>
    </tr>
  );
};

export const UserActivityEventTableRow = props => {
  const { details } = props;
  const timeMoment = moment(details.time);
  const timeMomentFormatted = timeMoment.format(READABLE_TIME_FORMAT);

  return (
    <tr>
      <td>{timeMomentFormatted}</td>
      <td>{details.user_activity.name}</td>
      <td>{details.duration_minutes}</td>
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

export const getUrlForSupplementsHistory = startDate => {
  const endTime = moment(startDate).add(24, "hours");
  // We don't want to get the full 24 hours since that will include the next day results
  endTime.subtract(1, "seconds");

  const startTimeString = startDate.toISOString();
  const endTimeString = endTime.toISOString();

  return `/api/v1/supplement_events/?start_time=${startTimeString}&end_time=${endTimeString}`;
};

export const getUrlForUserActivityEventsHistory = startDate => {
  const endTime = moment(startDate).add(24, "hours");
  // We don't want to get the full 24 hours since that will include the next day results
  endTime.subtract(1, "seconds");

  const startTimeString = startDate.toISOString();
  const endTimeString = endTime.toISOString();

  return `/api/v1/user_activity_events/?start_time=${startTimeString}&end_time=${endTimeString}`;
};
