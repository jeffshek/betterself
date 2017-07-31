import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { DefaultLineChartDataset } from "../constants/charts";
import { BaseAnalyticsView } from "../analytics/base";
import { MultiTabTableView } from "../resources_table/multi_tab_table";

const TableRow = props => {
  const { details } = props;
  return (
    <tr>
      <td>{details[0]}</td>
      <td>{details[1]}</td>
    </tr>
  );
};

const ProductivityHistoryChart = {
  labels: [],
  datasets: [Object.assign({}, DefaultLineChartDataset)]
};

export class DailyOverviewAnalyticsView extends BaseAnalyticsView {
  constructor() {
    super();
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

        this.state.productivityHistoryChart.labels = labelDates;
        this.state.productivityHistoryChart.datasets[0].data = arrayValues;

        this.setState({
          productivityHistoryChart: this.state.productivityHistoryChart,
          selectedProductivityHistoryChartData: reverseResponseData
        });
      });
  }

  renderWidgets() {
    return (
      <div className="card">
        <div className="card-header analytics-text-box-label">
          <span className="font-2xl username-text">
            Tuesday - June 5th, 2017
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
            <div className="social-box gray-background">
              <i className="widgets-analytics icon-ban">
                <span className="widget-font"> Distractions</span>
              </i>
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
      <div className="animated fadeIn">
        {this.renderWidgets()}
        {this.renderSupplementsAndUserActivitiesHistory()}
      </div>
    );
  }
}
