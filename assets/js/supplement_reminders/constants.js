import React from "react";
import { Link } from "react-router-dom";
import { getSupplementOverviewURLFromUUID } from "../routing/routing_utils";
import { RenderTrueFalseCheckBox } from "../constants/designs";

export const SupplementReminderTableHeader = () => (
  <thead>
    <tr>
      <th>Supplement</th>
      <th>Reminder Time</th>
      <th>Quantity</th>
      <th>Text Number</th>
      <th className="center-source">Text Verified</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);

export const SupplementReminderRow = props => {
  const data = props.object;
  const phoneNumber = data.phone_number;
  const { phone_number, is_verified } = phoneNumber;
  const { supplement, reminder_time, quantity, uuid } = data;
  const name = supplement.name;
  const supplementUUID = supplement.uuid;

  // const dateCreated = data.created;
  // const timeFormatted = moment(dateCreated).format(DATETIME_CREATED_FORMAT);
  const supplementOverviewLink = getSupplementOverviewURLFromUUID(
    supplementUUID
  );

  const renderCheckBox = RenderTrueFalseCheckBox(is_verified);

  return (
    <tr>
      <td><Link to={supplementOverviewLink}>{name}</Link></td>
      <td>{reminder_time}</td>
      <td>{quantity}</td>
      <td>{phone_number}</td>
      <td>{renderCheckBox}</td>
      <td>
        <div className="center-icon">
          <div
            className="remove-icon"
            onClick={e => props.confirmDelete(uuid, name, reminder_time)}
          >
            <i className="fa fa-remove fa-1x" />
          </div>
        </div>
      </td>
      {/*<td>{timeFormatted}</td>*/}
    </tr>
  );
};
