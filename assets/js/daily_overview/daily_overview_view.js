import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import LoggedInHeader from "../header/internal_header";
import Sidebar from "../sidebar/sidebar";
import moment from "moment";
import { DATE_REQUEST_FORMAT } from "../constants/dates_and_times";
import {
  SupplementsAndUserActivitiesMultiTab
} from "./supplements_and_events_historical_tables";
import { DailyOverviewWidgetsView } from "./supplements_and_events_widgets";
import { getDailyOverViewURLFromDate } from "./constants";

const updateWindowLocationOnInvalidDate = () => {
  // if invalid url, get the current date and go there instead
  // redirect to /dashboard/analytics/daily_overview/2017-08-01/ (or whatever today's date is)

  // Go to the previous day, since most of the time the current date will have no data
  const url = getDailyOverViewURLFromDate(moment().subtract(1, "days"));
  window.location.assign(url);
};

export class DailyOverviewAnalyticsView extends Component {
  constructor(props) {
    super(props);

    const { match } = props;

    // Parse date from URL
    let resourceDate = match.params.date;

    if (resourceDate) {
      resourceDate = moment(resourceDate);
      if (!resourceDate.isValid()) {
        updateWindowLocationOnInvalidDate();
      }
    } else if (!resourceDate) {
      updateWindowLocationOnInvalidDate();
      // Set resourceDate to today just so render doesn't complain if it gets there prior to reloading
      resourceDate = moment();
    }

    this.resourceDate = resourceDate;
  }

  render() {
    return (
      // Need to get the param from the Routh path, which is why this renders the rest of the page
      // Most pages don't need a param, but this one is customized
      (
        <div className="app">
          <LoggedInHeader />
          <div className="app-body">
            <Sidebar />
            <main className="main">
              <DailyOverviewWidgetsView
                date={this.resourceDate.format(DATE_REQUEST_FORMAT)}
              />
              <SupplementsAndUserActivitiesMultiTab
                date={this.resourceDate.format(DATE_REQUEST_FORMAT)}
              />
            </main>
          </div>
        </div>
      )
    );
  }
}
