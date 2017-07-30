import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { DefaultLineChartDataset } from "../constants/charts";
import {
  DISTRACTING_MINUTES_LABEL,
  DISTRACTING_MINUTES_VARIABLE,
  NEUTRAL_MINUTES_LABEL,
  NEUTRAL_MINUTES_VARIABLE,
  PRODUCTIVE_MINUTES_LABEL,
  PRODUCTIVE_MINUTES_VARIABLE,
  VERY_DISTRACTING_MINUTES_LABEL,
  VERY_DISTRACTING_MINUTES_VARIABLE,
  VERY_PRODUCTIVE_MINUTES_LABEL,
  VERY_PRODUCTIVE_MINUTES_VARIABLE
} from "../constants/productivity";
import { BaseAnalyticsView } from "../analytics/base";

const ProductivityColumnMappingToKey = {
  "Very Productive Minutes": VERY_PRODUCTIVE_MINUTES_VARIABLE,
  "Productive Minutes": PRODUCTIVE_MINUTES_VARIABLE,
  "Neutral Minutes": NEUTRAL_MINUTES_VARIABLE,
  "Distracting Minutes": DISTRACTING_MINUTES_VARIABLE,
  "Very Distracting Minutes": VERY_DISTRACTING_MINUTES_VARIABLE
};

const ProductivityHistoryChart = {
  labels: [],
  datasets: [Object.assign({}, DefaultLineChartDataset)]
};

export class DailyOverviewAnalyticsView extends BaseAnalyticsView {
  constructor() {
    super();
    const updateState = {
      productivityHistoryChart: ProductivityHistoryChart,
      //
      selectedProductivityHistoryChartData: [],
      selectedProductivityHistoryType: VERY_PRODUCTIVE_MINUTES_LABEL
    };
    // Update state (from base class) with the above
    this.state = Object.assign(this.state, updateState);

    this.state.productivityHistoryChart.datasets[
      0
    ].label = this.state.selectedProductivityHistoryType;

    this.supplementCorrelationsURL =
      "api/v1/productivity_log/supplements/correlations";
    this.supplementsCorrelationsChartLabel =
      "Supplements and Productivity Correlation (Last 60 Days)";
    this.userActivitiesCorrelationsURL =
      "api/v1/productivity_log/user_activities/correlations";
    this.userActivitiesCorrelationsChartLabel =
      "User Activities and Productivity Correlation";

    this.handleSelectedProductivityHistoryType = this.handleSelectedProductivityHistoryType.bind(
      this
    );
  }

  componentDidMount() {
    this.getHistory();
    this.getSupplementsCorrelations();
    this.getUserActivitiesCorrelations();
  }

  // Choose between "Very Productive Minutes", "Neutral Minutes", "Negative Minutes" etc
  handleSelectedProductivityHistoryType(event) {
    const selectedProductivityHistoryType = event.target.value;
    const column_key =
      ProductivityColumnMappingToKey[selectedProductivityHistoryType];

    const arrayValues = this.state.selectedProductivityHistoryChartData.map(
      key => key[column_key]
    );

    this.state.selectedProductivityHistoryType = selectedProductivityHistoryType;
    this.state.productivityHistoryChart.datasets[0].data = arrayValues;
    this.state.productivityHistoryChart.datasets[
      0
    ].label = this.state.selectedProductivityHistoryType;

    this.setState({
      productivityHistoryChart: this.state.productivityHistoryChart
    });
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

        this.state.productivityHistoryChart.labels = labelDates;
        this.state.productivityHistoryChart.datasets[0].data = arrayValues;

        this.setState({
          productivityHistoryChart: this.state.productivityHistoryChart,
          selectedProductivityHistoryChartData: reverseResponseData
        });
      });
  }

  renderHistoryChart() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          <span className="font-2xl">Daily Overview - June 5th, 2017</span>
          <span className="float-right">
            Chart Selection
            <select
              className="form-control chart-selector"
              onChange={this.handleSelectedProductivityHistoryType}
              value={this.state.selectedProductivityHistoryType}
              size="1"
            >
              <option>{VERY_PRODUCTIVE_MINUTES_LABEL}</option>
              <option>{PRODUCTIVE_MINUTES_LABEL}</option>
              <option>{NEUTRAL_MINUTES_LABEL}</option>
              <option>{DISTRACTING_MINUTES_LABEL}</option>
              <option>{VERY_DISTRACTING_MINUTES_LABEL}</option>
            </select>
          </span>
        </div>
        <div className="card-block">
          <div className="chart-wrapper">
            <Line
              data={this.state.productivityHistoryChart}
              options={{
                maintainAspectRatio: false
              }}
            />
          </div>
        </div>
      </div>
    );
  }

  renderOverviewWidgets() {
    return (
      <div className="row">
        <div className="col-sm-6 col-lg-3">
          <div className="social-box facebook widgets">
            <i className="widgets-analytics">Productivity</i>
            <div className="chart-wrapper">
              <canvas id="social-box-chart-1" height="90" />
            </div>
            <ul>
              <li>
                <strong>7.5 Hours</strong>
                <span>Today</span>
              </li>
              <li>
                <strong>4.5 Hours</strong>
                <span>Yesterday</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="col-sm-6 col-lg-3">
          <div className="social-box twitter">
            <i className="widgets-analytics">Distractions</i>
            <div className="chart-wrapper">
              <canvas id="social-box-chart-2" height="90" />
            </div>
            <ul>
              <li>
                <strong>7.5 Hours</strong>
                <span>Today</span>
              </li>
              <li>
                <strong>4.5 Hours</strong>
                <span>Yesterday</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="col-sm-6 col-lg-3">
          <div className="social-box linkedin">
            <i className="widgets-analytics">Sleep</i>
            <div className="chart-wrapper">
              <canvas id="social-box-chart-3" height="90" />
            </div>
            <ul>
              <li>
                <strong>8:13 AM</strong>
                <span>Wake Up Time</span>
              </li>
              <li>
                <strong>6.5 Hours</strong>
                <span>Total Rest</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="col-sm-6 col-lg-3">
          <div className="social-box google-plus">
            <i className="widgets-analytics">Supplements</i>
            <div className="chart-wrapper">
              <canvas id="social-box-chart-4" height="90" />
            </div>
            <ul>
              <li>
                <strong>23</strong>
                <span>Today</span>
              </li>
              <li>
                <strong>13</strong>
                <span>Today</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  render() {
    return (
      <div className="animated fadeIn">
        {this.renderHistoryChart()}
        {this.renderOverviewWidgets()}
        {this.renderSupplementsCorrelations()}
        {this.renderUserActivitiesCorrelations()}
      </div>
    );
  }
}
