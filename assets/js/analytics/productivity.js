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
    this.state.productivityHistory.datasets[0].label = "Time (Minutes)";
  }

  componentDidMount() {
    this.getHistory();
  }

  getHistory() {
    fetch("/api/v1/productivity_log/", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const reverseResponseData = responseData.results.reverse();
        console.log(reverseResponseData);
        const labelDates = reverseResponseData.map(key => key.date);
        const arrayValues = reverseResponseData.map(
          key => key.very_productive_time_minutes
        );

        this.state.productivityHistory.labels = labelDates;
        this.state.productivityHistory.datasets[0].data = arrayValues;

        this.setState({ productivityHistory: this.state.productivityHistory });
      });
  }
  renderHistoryChart() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          <span className="font-2xl">Productivity History</span>
          <span className="float-right">
            <input
              type="text"
              id="text-input"
              name="text-input"
              className="form-control center-source"
              placeholder="Very Productive"
            />
          </span>
        </div>

        <div className="card-block">
          <div className="chart-wrapper">
            <Line
              data={this.state.productivityHistory}
              options={{
                maintainAspectRatio: false
              }}
            />
          </div>
        </div>
      </div>
    );
  }

  render() {
    return (
      <div className="animated fadeIn">
        {this.renderHistoryChart()}
      </div>
    );
  }
}
