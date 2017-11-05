import React from "react";
import moment from "moment";
import { READABLE_DATE_TIME_FORMAT } from "../constants/dates_and_times";

export const SupplementStackRow = props => {
  const data = props.object;
  const { name, uuid, created, compositions } = data;
  const createTimeFormat = moment(created).format(READABLE_DATE_TIME_FORMAT);

  let compositionsFormat;
  if (compositions) {
    compositionsFormat = compositions.map(e => {
      return `${e.quantity} ${e.supplement.name}`;
    });
  }

  compositionsFormat = compositionsFormat.join(", ");

  return (
    <tr>
      <td>{name}</td>
      <td>
        {compositions.length > 0
          ? compositionsFormat
          : <div
              className="btn-link"
              onClick={e => props.selectedStackChange(data)}
            >
              Click to add a supplement
            </div>}
      </td>
      <td>
        <div className="center-icon">
          <div
            className="edit-icon"
            onClick={e => props.selectedStackChange(data)}
          >
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
