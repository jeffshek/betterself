import React, { Component } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import moment from "moment";
import { DATE_REQUEST_FORMAT } from "../constants/dates_and_times";
import { Calendar } from "react-yearly-calendar";
import {
  SupplementsAndProductivityChartView
} from "./supplements_overview_charts";

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
        const supplement = responseData[0];
        this.setState(
          {
            supplement: supplement
          },
          this.getSupplementsActivityCalendar
        );
      });
  }

  getSupplementsActivityCalendar() {
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

        // We do this weird thing where we set the activityDates here
        // because due to some bug, if it's rendered too early, it will
        // not rerender correctly.
        this.state.activityDates = {};
        this.state.activityDates.supplements = supplementDatesFormatted;

        this.setState({
          activityDates: this.state.activityDates
        });
      });
  }

  render() {
    if (!this.state.supplement || !this.state.activityDates) {
      return <div />;
    }

    return (
      <div>
        <SupplementsAndProductivityChartView
          supplement={this.state.supplement}
        />
        <Calendar year={2017} customClasses={this.state.activityDates} />
      </div>
    );
  }
}
