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
