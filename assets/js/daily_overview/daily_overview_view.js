import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { MultiTabTableView } from "../resources_table/multi_tab_table";
import LoggedInHeader from "../header/internal_header";
import Sidebar from "../sidebar/sidebar";
import moment from "moment";
import {
  DATE_REQUEST_FORMAT,
  READABLE_TIME_FORMAT
} from "../constants/dates_and_times";

const TableRow = props => {
  const { details } = props;
  const timeMoment = moment(details.time);
  const timeMomentFormatted = timeMoment.format(READABLE_TIME_FORMAT);
  return (
    <tr>
      <td>{timeMomentFormatted}</td>
      <td>{details.supplement_name}</td>
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

export class DailyOverviewAnalyticsView extends Component {
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

    this.tableNavTabs = ["Today", "Yesterday"];
    this.tableColumnHeaders = ["dog", "cat"];
    this.tableData = [
      [[0, 1], [2, 3], [4, 5], [9, 1], ["lo", 3], [41, 5]],
      [["a", 1], ["b", 3], ["c", 5], ["d", 1], ["e", 3], ["f", 5]]
    ];

    this.state = {};
    this.state.productivityTimeToday = 0;
    this.state.productivityTimeYesterday = 0;
    this.state.distractingTimeYesterday = 0;
    this.state.distractingTimeToday = 0;

    this.state.supplementsHistory = [[], []];
    this.state.supplementsHistoryToday = [];
    this.state.supplementsHistoryYesterday = [];
  }

  getUrlForSupplementsHistory(startDate) {
    const endTime = moment(startDate).add(24, "hours");
    // We don't want to get the full 24 hours since that will include the next day results
    endTime.subtract(1, "seconds");

    const startTimeString = startDate.toISOString();
    const endTimeString = endTime.toISOString();

    return `/api/v1/supplement_events/?start_time=${startTimeString}&end_time=${endTimeString}`;
  }

  getSupplementsHistory() {
    const historyToday = this.getSupplementsHistoryToday();
    const historyYesterday = this.getSupplementsHistoryYesterday();

    Promise.all([historyToday, historyYesterday]).then(result => {
      const supplementsHistory = [
        this.state.supplementsHistoryToday,
        this.state.supplementsHistoryYesterday
      ];

      this.setState({ supplementsHistory: supplementsHistory });
    });
  }

  getSupplementsHistoryToday() {
    return this.fetchSupplementsHistory(
      this.resourceDate,
      "supplementsHistoryToday"
    );
  }

  getSupplementsHistoryYesterday() {
    return this.fetchSupplementsHistory(
      this.previousResourceDate,
      "supplementsHistoryYesterday"
    );
  }

  fetchSupplementsHistory(historyDate, supplementHistoryKey) {
    const url = this.getUrlForSupplementsHistory(historyDate);

    return fetch(url, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const { results } = responseData;

        const resultsWithHash = results.map(details => {
          // Table Row rendering needs to know what are unique keys
          // Create a unique hash based on what we know about supplements and what time they're taken
          const uniqueKey = `${details.time}-${details.supplement_name}`;
          details.uniqueKey = uniqueKey;
          return details;
        });

        // Dynamically set state
        this.setState({
          [supplementHistoryKey]: resultsWithHash
        });
        return results;
      });
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
        // Filter any results that match the date
        const startDateResult = results.filter(element =>
          dateFilter(element, startDateString)
        )[0];
        const endDateResult = results.filter(element =>
          dateFilter(element, endDateString)
        )[0];

        let distractingTimeYesterday = 0;
        let productivityTimeYesterday = 0;
        let distractingTimeToday = 0;
        let productivityTimeToday = 0;

        if (startDateResult) {
          distractingTimeYesterday = minutesToHours(
            startDateResult.very_distracting_time_minutes +
              startDateResult.distracting_time_minutes
          );
          productivityTimeYesterday = minutesToHours(
            startDateResult.very_productive_time_minutes +
              startDateResult.productive_time_minutes
          );
        }

        if (endDateResult) {
          distractingTimeToday = minutesToHours(
            endDateResult.very_distracting_time_minutes +
              endDateResult.distracting_time_minutes
          );
          productivityTimeToday = minutesToHours(
            endDateResult.very_productive_time_minutes +
              endDateResult.productive_time_minutes
          );
        }

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
    this.getSupplementsHistory();
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
                  <strong>{this.state.supplementsHistoryToday.length}</strong>
                  <span>Today</span>
                </li>
                <li>
                  <strong>
                    {this.state.supplementsHistoryYesterday.length}
                  </strong>
                  <span>Yesterday</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }

  renderUserActivitiesHistory() {
    return (
      <MultiTabTableView
        tableNavTabs={this.tableNavTabs}
        tableColumnHeaders={["Time", "Activity"]}
        tableData={this.tableData}
        tableRowRenderer={TableRow}
      />
    );
  }

  renderSupplementsHistory() {
    return (
      <MultiTabTableView
        tableNavTabs={this.tableNavTabs}
        tableColumnHeaders={["Time", "Supplement"]}
        tableData={this.state.supplementsHistory}
        tableRowRenderer={TableRow}
        tableName="Supplements Taken"
      />
    );
  }

  renderSupplementsAndUserActivitiesHistory() {
    return (
      <div className="card-columns cols-2">
        {this.renderSupplementsHistory()}
        {/*{this.renderUserActivitiesHistory()}*/}
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
              {this.renderWidgets()}
              {this.renderSupplementsAndUserActivitiesHistory()}
            </main>
          </div>
        </div>
      )
    );
  }
}
