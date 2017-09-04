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
      if (!resourceDate.isValid()) {
        resourceDate = moment();
      }
    } else if (!resourceDate) {
      resourceDate = moment();
    }

    this.state = {
      resourceDate: resourceDate
    };
  }

  updateResourceDate = date => {
    this.setState({
      resourceDate: date
    });
  };

  render() {
    return (
      // Need to get the param from the Route path, which is why this renders the rest of the page
      // Most pages don't need a param, but this one is customized
      (
        <div className="app">
          <LoggedInHeader />
          <div className="app-body">
            <Sidebar />
            <main className="main">
              <DailyOverviewWidgetsView
                date={this.state.resourceDate.format(DATE_REQUEST_FORMAT)}
                resourceDateController={this.updateResourceDate}
              />
              <SupplementsAndUserActivitiesMultiTab
                date={this.state.resourceDate.format(DATE_REQUEST_FORMAT)}
              />
            </main>
          </div>
        </div>
      )
    );
  }
}
