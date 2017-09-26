import React from "react";
import moment from "moment";
import { getDailyOverViewURLFromDate } from "../routing/routing_utils";
import { Link } from "react-router-dom";
import { DATE_REQUEST_FORMAT } from "../constants/dates_and_times";

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
