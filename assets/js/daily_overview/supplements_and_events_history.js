import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import { MultiTabTableView } from "../resources_table/multi_tab_table";
import moment from "moment";
import { TableRow } from "./constants";

export class SupplementsAndUserActivitiesMultiTab extends Component {
  constructor(props) {
    super(props);

    const { date } = props;

    this.resourceDate = moment(date);
    this.previousResourceDate = moment(date).subtract(1, "days");

    this.tableNavTabs = ["Today", "Yesterday"];

    this.state = {};
    this.state.supplementsHistory = [[], []];
    this.state.supplementsHistoryToday = [];
    this.state.supplementsHistoryYesterday = [];

    this.state.userActivityEventsHistory = [[], []];
    this.state.userActivityEventsHistoryToday = [];
    this.state.userActivityEventsHistoryYesterday = [];
  }

  getUrlForSupplementsHistory(startDate) {
    const endTime = moment(startDate).add(24, "hours");
    // We don't want to get the full 24 hours since that will include the next day results
    endTime.subtract(1, "seconds");

    const startTimeString = startDate.toISOString();
    const endTimeString = endTime.toISOString();

    return `/api/v1/supplement_events/?start_time=${startTimeString}&end_time=${endTimeString}`;
  }

  getUrlForUserActivityEventsHistory(startDate) {
    const endTime = moment(startDate).add(24, "hours");
    // We don't want to get the full 24 hours since that will include the next day results
    endTime.subtract(1, "seconds");

    const startTimeString = startDate.toISOString();
    const endTimeString = endTime.toISOString();

    return `/api/v1/user_activity_events/?start_time=${startTimeString}&end_time=${endTimeString}`;
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

  componentDidMount() {
    this.getSupplementsHistory();
  }

  renderUserActivitiesHistory() {
    return (
      <MultiTabTableView
        tableNavTabs={this.tableNavTabs}
        tableColumnHeaders={["Time", "Activity"]}
        tableData={this.state.supplementsHistory}
        tableRowRenderer={TableRow}
        tableName="User Activities"
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

  render() {
    return (
      <div className="card-columns cols-2">
        {this.renderSupplementsHistory()}
        {/*{this.renderUserActivitiesHistory()}*/}
      </div>
    );
  }
}
