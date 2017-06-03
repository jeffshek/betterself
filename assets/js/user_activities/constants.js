import React, { Component, PropTypes } from "react";
import { TrueCheckBox } from "../constants/designs";

export const UserActivityHistoryRow = props => {
  const data = props.object;
  const { name, is_significant_activity, is_negative_activity, uuid } = data;

  return (
    <tr>
      <td>{name}</td>
      <td>{is_significant_activity ? <TrueCheckBox /> : ""}</td>
      <td>{is_negative_activity ? <TrueCheckBox /> : ""}</td>
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
    </tr>
  );
};

export const UserActivityHistoryTableHeader = () => (
  <thead>
    <tr>
      <th>Activity Name</th>
      <th className="center-source">Significant</th>
      <th className="center-source">Negative</th>
      <th className="center-source">Actions</th>
    </tr>
  </thead>
);
