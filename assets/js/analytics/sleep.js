import React from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import moment from "moment";
import { DefaultLineChartDataset } from "../constants/charts";
import { BaseAnalyticsView } from "./base";

const SleepHistoryChart = {
  labels: [],
  datasets: [Object.assign({}, DefaultLineChartDataset)]
};

export class SleepAnalyticsView extends BaseAnalyticsView {
  constructor() {
    super();
    const updateState = {
      sleepHistory: SleepHistoryChart
    };
    // Update state (from base class) with the above
    this.state = Object.assign(this.state, updateState);
    this.state.sleepHistory.datasets[0].label = "Sleep Time (Hours)";

    this.supplementCorrelationsURL =
      "api/v1/sleep_activities/supplements/correlations";
    this.supplementsCorrelationsChartLabel =
      "Supplements and Sleep Correlation";
    this.userActivitiesCorrelationsURL =
      "api/v1/sleep_activities/user_activities/correlations";
    this.userActivitiesCorrelationsChartLabel =
      "User Activities and Sleep Correlation";
  }

  componentDidMount() {
    this.getHistory();
    this.getSupplementsCorrelations();
    this.getUserActivitiesCorrelations();
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
        // Sort by datetime
        const sleepDates = Object.keys(responseData);
        sleepDates.sort();

        const sleepDatesFormatted = sleepDates.map(key =>
          moment(key).format("l dd")
        );

        const dataParsed = sleepDates.map(key => {
          return (responseData[key] / 60).toFixed(2);
        });

        this.state.sleepHistory.labels = sleepDatesFormatted;
        this.state.sleepHistory.datasets[0].data = dataParsed;

        // Reset the historicalState of the graph after the data has been grabbed.
        this.setState({ sleepHistory: this.state.sleepHistory });
      });
  }

  renderHistoryChart() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          <span className="font-2xl">Sleep History</span>
        </div>
        <div className="card-block">
          <div className="chart-wrapper">
            <Bar
              data={this.state.sleepHistory}
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
        {this.renderSupplementsCorrelations()}
        {this.renderUserActivitiesCorrelations()}
      </div>
    );
  }
}
