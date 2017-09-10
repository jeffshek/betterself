import { Link } from "react-router-dom";
import React, { Component } from "react";
import { Bar, Doughnut, Line, Pie, Polar, Radar } from "react-chartjs-2";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/requests";
import moment from "moment";
import { DATE_REQUEST_FORMAT } from "../constants/dates_and_times";
import {
  dateFilter,
  getUrlForSupplementsHistory,
  minutesToHours
} from "./constants";
import { getDailyOverViewURLFromDate } from "../routing/routing_utils";

const LEFT_ARROW = require("../../img/navigation/restart.svg");

export class DailyOverviewWidgetsView extends Component {
  constructor(props) {
    super(props);

    const { date } = props;

    this.state = {
      resourceDate: moment(date),
      previousResourceDate: moment(date).subtract(1, "days"),
      nextResourceDate: moment(date).add(1, "days"),
      productivityTimeToday: 0,
      productivityTimeYesterday: 0,
      distractingTimeYesterday: 0,
      distractingTimeToday: 0,
      supplementsHistory: [[], []],
      supplementsHistoryToday: [],
      supplementsHistoryYesterday: []
    };
  }

  componentDidMount() {
    this.updateResources();
  }

  componentWillReceiveProps(props) {
    const { date } = props;

    this.setState(
      {
        resourceDate: moment(date),
        previousResourceDate: moment(date).subtract(1, "days"),
        nextResourceDate: moment(date).add(1, "days")
      },
      this.updateResources
    );
  }

  updateResources = () => {
    this.getProductivityHistory();
    this.getSupplementsHistory();
  };

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
      this.state.resourceDate,
      "supplementsHistoryToday"
    );
  }

  getSupplementsHistoryYesterday() {
    return this.fetchSupplementsHistory(
      this.state.previousResourceDate,
      "supplementsHistoryYesterday"
    );
  }

  fetchSupplementsHistory(historyDate, supplementHistoryKey) {
    const url = getUrlForSupplementsHistory(historyDate);

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
    const startDateString = this.state.previousResourceDate.format(
      DATE_REQUEST_FORMAT
    );
    const endDateString = this.state.resourceDate.format(DATE_REQUEST_FORMAT);
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

  renderHeader() {
    const previousDayURL = getDailyOverViewURLFromDate(
      this.state.previousResourceDate
    );
    const nextDayURL = getDailyOverViewURLFromDate(this.state.nextResourceDate);

    return (
      <div className="card-header analytics-text-box-label">
        <Link to={previousDayURL}>
          <img
            src={LEFT_ARROW}
            className="daily-overview-navigation"
            width="40px"
            height="30px"
            onClick={e =>
              this.props.resourceDateController(
                this.state.previousResourceDate
              )}
          />
        </Link>

        <span className="font-2xl username-text">
          {this.state.resourceDate.format("dddd - MMMM Do YYYY")}
        </span>
        <Link to={nextDayURL}>
          <img
            src={LEFT_ARROW}
            className="daily-overview-navigation-flip"
            width="40px"
            height="30px"
            onClick={e =>
              this.props.resourceDateController(this.state.nextResourceDate)}
          />
        </Link>
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        {this.renderHeader()}
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
}
