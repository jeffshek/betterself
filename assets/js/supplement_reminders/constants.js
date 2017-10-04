import React from "react";
import moment from "moment";
import { Link } from "react-router-dom";
import { getSupplementOverviewURLFromUUID } from "../routing/routing_utils";
import { DATETIME_CREATED_FORMAT } from "../constants/dates_and_times";

export const SupplementReminderTableHeader = () => (
  <thead>
    <tr>
      <th>Supplement</th>
      <th>Reminder Time</th>
      <th>Quantity</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);

export const SupplementReminderRow = props => {
  // console.log(props)
  const data = props.object;

  const { supplement, reminder_time, quantity } = data;
  const name = supplement.name;
  const supplementUUID = supplement.uuid;

  // const dateCreated = data.created;
  // const timeFormatted = moment(dateCreated).format(DATETIME_CREATED_FORMAT);
  const supplementOverviewLink = getSupplementOverviewURLFromUUID(
    supplementUUID
  );

  return (
    <tr>
      <td><Link to={supplementOverviewLink}>{name}</Link></td>
      <td>{reminder_time}</td>
      <td>{quantity}</td>
      <td>
        <div className="center-icon">
          <div
            className="remove-icon"
            onClick={e => props.confirmDelete(uuid, name)}
          >
            <i className="fa fa-remove fa-1x" />
          </div>
        </div>
      </td>
      {/*<td>{timeFormatted}</td>*/}
    </tr>
  );
};
