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

const ProductivityColumnMappingToKey = {
  "Very Productive Minutes": "very_productive_time_minutes",
  "Productive Minutes": "productive_time_minutes",
  "Neutral Minutes": "neutral_time_minutes",
  "Distracting Minutes": "distracting_time_minutes",
  "Very Distracting Minutes": "very_distracting_time_minutes"
};

export class ProductivityAnalyticsView extends Component {
  constructor() {
    super();
    this.state = {
      chartHistoryData: [],
      selectedProductivityHistoryType: "Very Productive Minutes",
      productivityHistory: ProductivityHistoryChart
    };
    this.state.productivityHistory.datasets[
      0
    ].label = this.state.selectedProductivityHistoryType;
    this.handleSelectedProductivityHistory = this.handleSelectedProductivityHistory.bind(
      this
    );
  }

  handleSelectedProductivityHistory(event) {
    const selectedProductivityHistoryType = event.target.value;
    const column_key =
      ProductivityColumnMappingToKey[selectedProductivityHistoryType];

    const arrayValues = this.state.chartHistoryData.map(key => key[column_key]);

    this.state.selectedProductivityHistoryType = selectedProductivityHistoryType;
    this.state.productivityHistory.datasets[0].data = arrayValues;
    this.state.productivityHistory.datasets[
      0
    ].label = this.state.selectedProductivityHistoryType;

    this.setState({ productivityHistory: this.state.productivityHistory });
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

        const labelDates = reverseResponseData.map(key => key.date);
        const arrayValues = reverseResponseData.map(
          key => key.very_productive_time_minutes
        );

        this.state.productivityHistory.labels = labelDates;
        this.state.productivityHistory.datasets[0].data = arrayValues;

        this.setState({
          productivityHistory: this.state.productivityHistory,
          chartHistoryData: reverseResponseData
        });
      });
  }
  renderHistoryChart() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          <span className="font-2xl">Productivity History</span>
          <span className="float-right">
            Chart Selection
            <select
              className="form-control chart-selector"
              onChange={this.handleSelectedProductivityHistory}
              value={this.state.selectedProductivityHistoryType}
              size="1"
            >
              <option>Very Productive Minutes</option>
              <option>Productive Minutes</option>
              <option>Neutral Minutes</option>
              <option>Distracting Minutes</option>
              <option>Very Distracting Minutes</option>
            </select>
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
