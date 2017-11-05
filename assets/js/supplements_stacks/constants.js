import React from "react";
import moment from "moment";
import { READABLE_DATE_TIME_FORMAT } from "../constants/dates_and_times";
import { Link } from "react-router-dom";

export const SupplementStackRow = props => {
  const data = props.object;
  const { name, uuid, created, compositions } = data;
  const createTimeFormat = moment(created).format(READABLE_DATE_TIME_FORMAT);

  return (
    <tr>
      <td>{name}</td>
      <td>
        <Link to="www.google.com">Click here to add a supplement ... </Link>
      </td>
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
      <td>{createTimeFormat}</td>
    </tr>
  );
};

export const SupplementStackTableHeader = () => (
  <thead>
    <tr>
      <th>Stack Name</th>
      <th>Supplements</th>
      <th className="center-source">Actions</th>
      <th>Create Time</th>
    </tr>
  </thead>
);
