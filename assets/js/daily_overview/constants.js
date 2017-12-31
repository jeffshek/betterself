import React from "react";
import {
  READABLE_DATE_TIME_FORMAT,
  READABLE_TIME_FORMAT
} from "../constants/dates_and_times";
import moment from "moment";
import { Link } from "react-router-dom";
import { getSupplementOverviewURLFromUUID } from "../routing/routing_utils";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";
import { SUPPLEMENT_EVENTS_RESOURCE_URL } from "../constants/urls";

const DeleteSupplementFromDailyOverview = ({ uuid, supplement_name, time }) => {
  const timeFormatted = moment(time).format(READABLE_DATE_TIME_FORMAT);
  const answer = confirm(
    `WARNING: THIS WILL DELETE THE FOLLOWING EVENT \n\n${supplement_name} at ${timeFormatted}!\n\nConfirm? `
  );

  if (answer) {
    const params = {
      uuid: uuid
    };
    fetch(SUPPLEMENT_EVENTS_RESOURCE_URL, {
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
      <td>
        <div
          className="remove-icon"
          onClick={e => DeleteSupplementFromDailyOverview(details)}
        >
          <i className="fa fa-remove fa-1x" />
        </div>
      </td>
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
