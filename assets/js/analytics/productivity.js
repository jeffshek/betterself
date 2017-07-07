import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { Nav, NavItem, NavLink } from "reactstrap";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import moment from "moment";
import { DefaultLineChartDataset } from "../constants/charts";

const ProductivityHistoryChart = {
  labels: [],
  datasets: [Object.assign({}, DefaultLineChartDataset)]
};

export class ProductivityAnalyticsView extends Component {
  constructor() {
    super();
    this.state = {
      productivityHistory: ProductivityHistoryChart
    };
  }

  componentDidMount() {
    this.getHistory();
  }

  getHistory() {
    fetch(`api/v1/sleep_activities/aggregates`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        console.log(responseData);
      });
  }
  render() {
    return <div />;
  }
}
