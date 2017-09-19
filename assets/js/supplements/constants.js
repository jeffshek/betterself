import React from "react";
import moment from "moment";
import { Link } from "react-router-dom";
import { getSupplementOverviewURLFromUUID } from "../routing/routing_utils";
import { DATETIME_CREATED_FORMAT } from "../constants/dates_and_times";

export const SupplementHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Name</th>
      <th className="center-source">Actions</th>
      <th>Date Added</th>
    </tr>
  </thead>
);

export const SupplementRow = props => {
  const data = props.object;

  const { uuid, name } = data;
  const dateCreated = data.created;
  const timeFormatted = moment(dateCreated).format(DATETIME_CREATED_FORMAT);
  const supplementOverviewLink = getSupplementOverviewURLFromUUID(uuid);

  return (
    <tr>
      <td><Link to={supplementOverviewLink}>{name}</Link></td>
      <td>
        <div className="center-icon">
          <div className="edit-icon" onClick={e => props.selectModalEdit(data)}>
            <i className="fa fa-edit fa-1x" />
          </div>
          &nbsp;
          <div
            className="remove-icon"
            onClick={e => props.confirmDelete(uuid, name)}
          >
            <i className="fa fa-remove fa-1x" />
          </div>
        </div>
      </td>
      <td>{timeFormatted}</td>
    </tr>
  );
};
