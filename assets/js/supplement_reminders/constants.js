import React from "react";
import { Link } from "react-router-dom";
import { getSupplementOverviewURLFromUUID } from "../routing/routing_utils";
import { RenderTrueFalseCheckBox } from "../constants/designs";
import moment from "moment";
import { TEXT_TIME_FORMAT } from "../constants/dates_and_times";

export const SupplementReminderTableHeader = () => (
  <thead>
    <tr>
      <th>Supplement</th>
      <th>Reminder Time</th>
      <th>Quantity</th>
      <th>Text Number</th>
      <th className="center-source">Number Verified</th>
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

  const supplementOverviewLink = getSupplementOverviewURLFromUUID(
    supplementUUID
  );

  // Parse the time in as UTC, so you can format it
  const currentTimeParsed = moment.utc(reminder_time, ["h:m a", "H:m"]);

  // Don't want to show things in UTC, that's confusing
  currentTimeParsed.local();

  const localTimeFormat = currentTimeParsed.format(TEXT_TIME_FORMAT);

  const renderCheckBox = RenderTrueFalseCheckBox(is_verified);

  return (
    <tr>
      <td><Link to={supplementOverviewLink}>{name}</Link></td>
      <td>{localTimeFormat}</td>
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
    </tr>
  );
};
