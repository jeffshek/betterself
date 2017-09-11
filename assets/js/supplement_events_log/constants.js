import React from "react";
import moment from "moment";
import { READABLE_DATE_TIME_FORMAT } from "../constants/dates_and_times";
import { Link } from "react-router-dom";
import {
  getSupplementOverviewURLFromUUID,
  getDailyOverViewURLFromDate
} from "../routing/routing_utils";

export const SupplementHistoryRow = props => {
  const data = props.object;
  const uuid = data.uuid;
  const supplementName = data.supplement_name;
  const servingSize = data.quantity;
  const source = data.source;
  const supplementTime = data.time;
  // const duration = data.duration_minutes;
  const timeFormatted = moment(supplementTime).format(
    READABLE_DATE_TIME_FORMAT
  );
  const supplementOverviewLink = getSupplementOverviewURLFromUUID(
    data.supplement_uuid
  );
  const dailyOverviewLink = getDailyOverViewURLFromDate(moment(supplementTime));

  return (
    <tr>
      <td><Link to={supplementOverviewLink}>{supplementName}</Link></td>
      <td>{servingSize}</td>
      <td><Link to={dailyOverviewLink}>{timeFormatted}</Link></td>
      <td>
        <div className="center-icon">
          <div className="edit-icon" onClick={e => props.selectModalEdit(data)}>
            <i className="fa fa-edit fa-1x" />
          </div>
          &nbsp;
          <div
            className="remove-icon"
            onClick={e =>
              props.confirmDelete(uuid, supplementName, timeFormatted)}
          >
            <i className="fa fa-remove fa-1x" />
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
