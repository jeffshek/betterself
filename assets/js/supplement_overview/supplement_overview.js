import React, { Component } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import moment from "moment";
import { DATE_REQUEST_FORMAT } from "../constants/dates_and_times";
import { Calendar } from "react-yearly-calendar";
import {
  SupplementsAndProductivityChartView
} from "./supplements_overview_charts";
import LoggedInHeader from "../header/internal_header";
import Sidebar from "../sidebar/sidebar";
import {
  getDailyOverViewURLFromDate,
  getSupplementAggregatesAnalyticsURL,
  getSupplementAnalyticsSummaryURL,
  getSupplementDosagesAnalyticsURL,
  getSupplementProductivityAnalyticsURL,
  getSupplementSleepAnalyticsURL
} from "../routing/routing_utils";
import { MultiTabTableView } from "../resources_table/multi_tab_table";
import { AnalyticsSummaryRowDisplay, HistoryRowDisplay } from "./constants";

const getFetchJSONAPI = url => {
  return fetch(url, {
    method: "GET",
    headers: JSON_AUTHORIZATION_HEADERS
  }).then(response => {
    return response.json();
  });
};

export class SupplementsOverview extends Component {
  constructor(props) {
    super(props);

    const { match } = props;

    let supplementUUID = match.params.supplementUUID;

    this.state = {
      supplement: null,
      activityDates: null,
      // empty array sets for now to be populated by API calls
      supplementHistory: [[], [], [], []],
      // individual, daily, monthly
      supplementAnalytics: [[], [], []]
    };

    const url = `/api/v1/supplements/?uuid=${supplementUUID}`;
    getFetchJSONAPI(url).then(responseData => {
      // Get the first one because this API endpoint returns back a list of supplements
      // in this case because of the filter, we are being exact and know we should only return one
      const supplement = responseData[0];
      // Then get all the history surrounding this supplement
      this.setState(
        {
          supplement: supplement
        },
        this.getSupplementData
      );
    });
  }

  getSupplementData() {
    this.getHistory();
    this.getAnalyticsSummary();
    this.getSleepHistory();
    this.getProductivityHistory();
    this.getDosages();
    this.getAggregateHistory();
    this.getAggregateDailyHistory();
    this.getAggregateMonthlyHistory();
  }

  getAggregateHistory() {
    const url = getSupplementAggregatesAnalyticsURL(this.state.supplement);
    getFetchJSONAPI(url).then(responseData => {
      responseData.reverse();
      this.state.supplementHistory[0] = responseData;
      this.setState({ supplementAnalytics: this.state.supplementAnalytics });
    });
  }

  getAggregateDailyHistory() {
    const baseUrl = getSupplementAggregatesAnalyticsURL(this.state.supplement);
    const url = `${baseUrl}?frequency=daily`;
    getFetchJSONAPI(url).then(responseData => {
      responseData.reverse();
      this.state.supplementHistory[1] = responseData;
      this.setState({ supplementAnalytics: this.state.supplementAnalytics });
    });
  }

  getAggregateMonthlyHistory() {
    const baseUrl = getSupplementAggregatesAnalyticsURL(this.state.supplement);
    const url = `${baseUrl}?frequency=monthly`;
    getFetchJSONAPI(url).then(responseData => {
      responseData.reverse();
      this.state.supplementHistory[2] = responseData;
      this.setState({ supplementAnalytics: this.state.supplementAnalytics });
    });
  }

  getDosages() {
    const url = getSupplementDosagesAnalyticsURL(this.state.supplement);
    getFetchJSONAPI(url).then(responseData => {
      this.state.supplementAnalytics[3] = responseData;
      this.setState({ supplementAnalytics: this.state.supplementAnalytics });
    });
  }

  getProductivityHistory() {
    const url = getSupplementProductivityAnalyticsURL(this.state.supplement);
    getFetchJSONAPI(url).then(responseData => {
      this.state.supplementAnalytics[2] = responseData;
      this.setState({ supplementAnalytics: this.state.supplementAnalytics });
    });
  }

  getSleepHistory() {
    const url = getSupplementSleepAnalyticsURL(this.state.supplement);
    getFetchJSONAPI(url).then(responseData => {
      this.state.supplementAnalytics[1] = responseData;
      this.setState({ supplementAnalytics: this.state.supplementAnalytics });
    });
  }

  getAnalyticsSummary() {
    const url = getSupplementAnalyticsSummaryURL(this.state.supplement);
    getFetchJSONAPI(url).then(responseData => {
      this.state.supplementAnalytics[0] = responseData;
      this.setState({ supplementAnalytics: this.state.supplementAnalytics });
    });
  }

  getHistory() {
    const start_date = moment().startOf("year").format(DATE_REQUEST_FORMAT);
    const url = `/api/v1/supplements/${this.state.supplement.uuid}/log/?frequency=daily&start_date=${start_date}`;

    getFetchJSONAPI(url).then(responseData => {
      // Loop through a response of key:value from API to get any
      // dates that are valid
      const responseDataDates = Object.keys(responseData);
      const validResponseDates = responseDataDates.filter(e => {
        return responseData[e];
      });
      validResponseDates.sort();

      const supplementDatesFormatted = validResponseDates.map(key =>
        moment(key).format(DATE_REQUEST_FORMAT)
      );

      // Do this weird thing where we set the activityDates ...
      // Due to a bug, if it's rendered too early, it will
      // not rerender correctly. I mean it's probably because I suck.
      this.state.activityDates = {};
      this.state.activityDates.supplements = supplementDatesFormatted;

      this.setState({
        activityDates: this.state.activityDates
      });
    });
  }

  redirectDailyCalendarDate = date => {
    const daily_overview_url = getDailyOverViewURLFromDate(date);
    this.props.history.push(daily_overview_url);
  };

  renderSupplementAnalytics() {
    return (
      <MultiTabTableView
        tableNavTabs={["Summary", "Sleep", "Productivity", "Dosages"]}
        tableColumnHeaders={["Metric", "Result"]}
        tableData={this.state.supplementAnalytics}
        tableRowRenderer={AnalyticsSummaryRowDisplay}
        tableName="Analytics (365 Days)"
      />
    );
  }

  renderSupplementHistory() {
    return (
      <MultiTabTableView
        tableNavTabs={["Event", "Daily", "Monthly"]}
        tableColumnHeaders={[
          "Date",
          "Quantity",
          "Productivity (Hours)",
          "Sleep (Hours)"
        ]}
        tableData={this.state.supplementHistory}
        tableRowRenderer={HistoryRowDisplay}
        tableName="Historical (90 Days)"
      />
    );
  }

  //# TODO - Refactor all of this after Twilio integration!
  render() {
    if (!this.state.supplement || !this.state.activityDates) {
      return <div />;
    }

    return (
      <div className="app">
        <LoggedInHeader />
        <div className="app-body">
          <Sidebar />
          <main className="main">
            <div className="card-block">
              <SupplementsAndProductivityChartView
                supplement={this.state.supplement}
              />
              <div className="card-header analytics-text-box-label">
                <span className="font-1xl">
                  {this.state.supplement.name} Usage (Current Year)
                </span>
              </div>
              <Calendar
                year={2017}
                customClasses={this.state.activityDates}
                onPickDate={this.redirectDailyCalendarDate}
              />
            </div>
            <div className="card-block">
              <div className="card-columns cols-2">
                {this.renderSupplementAnalytics()}
                {this.renderSupplementHistory()}
              </div>
            </div>
          </main>
        </div>
      </div>
    );
  }
}
