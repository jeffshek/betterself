import React from "react";
import { Bar } from "react-chartjs-2";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import moment from "moment";
import { GenerateHistoryChartTemplate } from "../constants/charts";
import { BaseAnalyticsView } from "./base";
import {
  ABBREVIATED_CHART_DATE,
  minutesToHours
} from "../constants/dates_and_times";

const SleepHistoryChart = GenerateHistoryChartTemplate("Sleep Time (Hours)");

// TODO - Refactor this file completely to the multitab format

export class SleepAnalyticsView extends BaseAnalyticsView {
  constructor() {
    super();

    const analyticsSettings = {
      periodsLookback: 60,
      rollingWindow: 1
    };

    const updateState = {
      sleepHistory: SleepHistoryChart
    };

    this.state = Object.assign(this.state, updateState, analyticsSettings);

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
          moment(key).format(ABBREVIATED_CHART_DATE)
        );

        const dataParsed = sleepDates.map(key => {
          return minutesToHours(responseData[key]);
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
