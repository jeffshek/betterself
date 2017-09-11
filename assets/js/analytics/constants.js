import React from "react";
import { getSupplementOverviewURLFromUUID } from "../routing/routing_utils";
import { Link } from "react-router-dom";

// This entire analytics folder needs to be refactored and cleaned up

export const SupplementCorrelationTableRow = data => {
  const details = data.object;
  // Try to see if the details contain a supplement UUID, if so, render that way
  const supplementUUID = data.supplementUUID;
  const valueFormatted = details[1] ? details[1].toFixed(3) : null;

  if (supplementUUID) {
    const supplementOverviewLink = getSupplementOverviewURLFromUUID(
      supplementUUID
    );
    return (
      <tr>
        <td><Link to={supplementOverviewLink}>{details[0]}</Link></td>
        <td>{valueFormatted}</td>
      </tr>
    );
  }

  return (
    <tr>
      <td>{details[0]}</td>
      <td>{valueFormatted}</td>
    </tr>
  );
};

export const UserActivitiesCorrelationTableRow = data => {
  const details = data.object;
  const valueFormatted = details[1] ? details[1].toFixed(3) : null;

  return (
    <tr>
      <td>{details[0]}</td>
      <td>{valueFormatted}</td>
    </tr>
  );
};
