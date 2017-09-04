import React from "react";

export const CorrelationTableRow = data => {
  const details = data.object;
  const valueFormatted = details[1] ? details[1].toFixed(3) : null;

  return (
    <tr>
      <td>{details[0]}</td>
      <td>{valueFormatted}</td>
    </tr>
  );
};
