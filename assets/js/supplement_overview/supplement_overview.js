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
import { getDailyOverViewURLFromDate } from "../routing/routing_utils";

export class SupplementsOverview extends Component {
  constructor(props) {
    super(props);

    const { match } = props;

    let supplementUUID = match.params.supplementUUID;

    this.state = {
      supplement: null,
      activityDates: null
    };

    fetch(`/api/v1/supplements/?uuid=${supplementUUID}`, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        // Get the first one because this API endpoint returns back a list of supplements
        // in this case because of the filter, we are being exact and know we should only return one
        const supplement = responseData[0];
        // Then get all the history surrounding this supplement
        this.setState(
          {
            supplement: supplement
          },
          this.getSupplementHistory
        );
      });
  }

  getSupplementHistory() {
    const start_date = moment().startOf("year").format(DATE_REQUEST_FORMAT);
    const url = `/api/v1/supplements/${this.state.supplement.uuid}/log/?frequency=daily&start_date=${start_date}`;

    fetch(url, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
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
        // not rerender correctly.
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
            <SupplementsAndProductivityChartView
              supplement={this.state.supplement}
            />
            <div className="card-block">
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
          </main>
        </div>
      </div>
    );
  }
}
