import React from "react";
import moment from "moment";
import { getDailyOverViewURLFromDate } from "../routing/routing_utils";
import { Link } from "react-router-dom";
import {
  DATE_REQUEST_FORMAT,
  DATETIME_CREATED_FORMAT,
  minutesToHours
} from "../constants/dates_and_times";

const RenderDateOverviewLink = value => {
  const valueDate = moment(value);
  const overviewURL = getDailyOverViewURLFromDate(valueDate);

  return (
    <Link key={value} to={overviewURL}>
      {valueDate.format(DATE_REQUEST_FORMAT)}<br />
    </Link>
  );
};

export const FormatValueToDataType = (value, data_type) => {
  if (data_type === "float" && value) {
    return value.toFixed(3);
  } else if (data_type === "list-datetime") {
    return value.map(RenderDateOverviewLink);
  } else if (data_type === "string-datetime") {
    return RenderDateOverviewLink(value);
  } else {
    return <span>{value}</span>;
  }
};

export const AnalyticsSummaryRowDisplay = props => {
  const { details } = props;
  const { value, label, data_type } = details;

  return (
    <tr>
      <td>{label}</td>
      <td>{FormatValueToDataType(value, data_type)}</td>
    </tr>
  );
};

export const HistoryRowDisplay = props => {
  const { time, quantity, productivity_time, sleep_time } = props.details;

  const timeMoment = moment(time);
  const overviewURL = getDailyOverViewURLFromDate(timeMoment);

  let timeFormatted;
  // If it's 12:00AM, assume we just want to see the date.
  if (timeMoment.hour() === 0 && timeMoment.minute() === 0) {
    timeFormatted = timeMoment.format(DATE_REQUEST_FORMAT);
  } else {
    timeFormatted = timeMoment.format(DATETIME_CREATED_FORMAT);
  }

  const productiveHours = minutesToHours(productivity_time);
  const sleepHours = minutesToHours(sleep_time);

  return (
    <tr>
      <td><Link to={overviewURL}>{timeFormatted}</Link></td>
      <td>{quantity}</td>
      <td>{productiveHours}</td>
      <td>{sleepHours}</td>
    </tr>
  );
};
