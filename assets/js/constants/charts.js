import React, { PropTypes, Component } from "react";

export const CHARTS_BACKGROUND_COLOR = "#193441";
export const CHART_HOVER_COLOR = "rgba(255,99,132,0.4)";
export const CHART_HOVER_BORDER_COLOR = "rgba(255,99,132,1)";
export const DefaultLineChartDataset = {
  label: "",
  fill: false,
  lineTension: 0.1,
  backgroundColor: CHARTS_BACKGROUND_COLOR,
  borderColor: CHARTS_BACKGROUND_COLOR,
  borderCapStyle: "butt",
  borderDash: [],
  borderDashOffset: 0.0,
  borderJoinStyle: "miter",
  pointBorderColor: "black",
  pointBackgroundColor: "#fff",
  pointBorderWidth: 1,
  pointHoverRadius: 5,
  pointHoverBackgroundColor: "rgba(75,192,192,1)",
  pointHoverBorderColor: "black",
  pointHoverBorderWidth: 2,
  pointRadius: 1,
  pointHitRadius: 10,
  data: []
};

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
