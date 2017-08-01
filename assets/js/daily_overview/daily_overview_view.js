import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { DefaultLineChartDataset } from "../constants/charts";
import { BaseAnalyticsView } from "../analytics/base";
import { MultiTabTableView } from "../resources_table/multi_tab_table";
import LoggedInHeader from "../header/internal_header";
import Sidebar from "../sidebar/sidebar";
import moment from "moment";
import { DATE_REQUEST_FORMAT } from "../constants/dates_and_times";

const TableRow = props => {
  const { details } = props;
  return (
    <tr>
      <td>{details[0]}</td>
      <td>{details[1]}</td>
    </tr>
  );
};

const minutesToHours = minutes => {
  return (minutes / 60).toFixed(2);
};

const dateFilter = (result, dateString) => {
  if (result.date === dateString) {
    return result;
  }
};

const ProductivityHistoryChart = {
  labels: [],
  datasets: [Object.assign({}, DefaultLineChartDataset)]
};

export class DailyOverviewAnalyticsView extends BaseAnalyticsView {
  constructor(props) {
    super(props);

    const { match } = props;

    // Parse date from URL
    let resourceDate = match.params.date;

    if (resourceDate) {
      resourceDate = moment(resourceDate);
      // If the date isn't valid, default to today
      if (!resourceDate.isValid()) {
        resourceDate = moment();
      }
    } else if (!resourceDate) {
      resourceDate = moment();
    }

    this.resourceDate = resourceDate;
    this.previousResourceDate = moment(resourceDate).subtract(1, "days");

    const updateState = {
      productivityHistoryChart: ProductivityHistoryChart
    };
    // Update state (from base class) with the above
    this.state = Object.assign(this.state, updateState);

    this.state.productivityHistoryChart.datasets[
      0
    ].label = this.state.selectedProductivityHistoryType;

    this.tableNavTabs = ["dog", "cat"];
    this.tableColumnHeaders = ["dog", "cat"];
    this.tableData = [
      [[0, 1], [2, 3], [4, 5], [9, 1], ["lo", 3], [41, 5]],
      [["a", 1], ["b", 3], ["c", 5], ["d", 1], ["e", 3], ["f", 5]]
    ];

    this.state.productivityTimeToday = 0;
    this.state.productivityTimeYesterday = 0;
    this.state.distractingTimeYesterday = 0;
    this.state.distractingTimeToday = 0;
  }

  getProductivityHistory() {
    const startDateString = this.previousResourceDate.format(
      DATE_REQUEST_FORMAT
    );
    const endDateString = this.resourceDate.format(DATE_REQUEST_FORMAT);

    const url = `/api/v1/productivity_log/?start_date=${startDateString}&end_date=${endDateString}`;

    fetch(url, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const { results } = responseData;
        const startDateResult = results.filter(element =>
          dateFilter(element, startDateString)
        )[0];
        const endDateResult = results.filter(element =>
          dateFilter(element, endDateString)
        )[0];

        const distractingTimeYesterday = minutesToHours(
          startDateResult.very_distracting_time_minutes +
            startDateResult.distracting_time_minutes
        );
        const productivityTimeYesterday = minutesToHours(
          startDateResult.very_productive_time_minutes +
            startDateResult.productive_time_minutes
        );
        const distractingTimeToday = minutesToHours(
          endDateResult.very_distracting_time_minutes +
            endDateResult.distracting_time_minutes
        );
        const productivityTimeToday = minutesToHours(
          endDateResult.very_productive_time_minutes +
            endDateResult.productive_time_minutes
        );

        this.setState({
          distractingTimeToday: distractingTimeToday,
          distractingTimeYesterday: distractingTimeYesterday,
          productivityTimeToday: productivityTimeToday,
          productivityTimeYesterday: productivityTimeYesterday
        });
      });
  }

  componentDidMount() {
    this.getProductivityHistory();
  }

  renderWidgets() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          <span className="font-2xl username-text">
            {this.resourceDate.format("dddd - MMMM Do YYYY")}
          </span>
        </div>
        <br />
        <div className="row">
          <div className="col-sm-6 col-lg-3">
            <div className="social-box default-background">
              <i className="widgets-analytics icon-speedometer">
                <span className="widget-font"> Productivity</span>
              </i>
              <ul>
                <li>
                  <strong>{this.state.productivityTimeToday} Hours</strong>
                  <span>Today</span>
                </li>
                <li>
                  <strong>{this.state.productivityTimeYesterday} Hours</strong>
                  <span>Yesterday</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="col-sm-6 col-lg-3">
            <div className="social-box gray-background">
              <i className="widgets-analytics icon-ban">
                <span className="widget-font"> Distractions</span>
              </i>
              <ul>
                <li>
                  <strong>{this.state.distractingTimeToday} Hours</strong>
                  <span>Today</span>
                </li>
                <li>
                  <strong>{this.state.distractingTimeYesterday} Hours</strong>
                  <span>Yesterday</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="col-sm-6 col-lg-3">
            <div className="social-box default-background">
              <i className="widgets-analytics icon-volume-off">
                <span className="widget-font"> Sleep</span>
              </i>
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
            <div className="social-box gray-background">
              <i className="widgets-analytics icon-chemistry">
                <span className="widget-font"> Supplements</span>
              </i>
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

  renderUserActivitiesHistory() {
    return (
      <MultiTabTableView
        tableNavTabs={this.tableNavTabs}
        tableColumnHeaders={["Jump", "High"]}
        tableData={this.tableData}
        tableRowRenderer={TableRow}
      />
    );
  }

  renderSupplementsHistory() {
    return (
      <MultiTabTableView
        tableNavTabs={this.tableNavTabs}
        tableColumnHeaders={["Jump", "High"]}
        tableData={this.tableData}
        tableRowRenderer={TableRow}
      />
    );
  }

  renderSupplementsAndUserActivitiesHistory() {
    return (
      <div className="card-columns cols-2">
        {this.renderSupplementsHistory()}
        {this.renderUserActivitiesHistory()}
      </div>
    );
  }

  render() {
    return (
      // Need to get the param from the Routh path, which is why this renders the rest of the page
      // Since I'm an idiot, I don't know how to do that just yet ...
      (
        <div className="app">
          <LoggedInHeader />
          <div className="app-body">
            <Sidebar />
            <main className="main">
              <div className="animated fadeIn">
                {this.renderWidgets()}
                {this.renderSupplementsAndUserActivitiesHistory()}
              </div>
            </main>
          </div>
        </div>
      )
    );
  }
}
