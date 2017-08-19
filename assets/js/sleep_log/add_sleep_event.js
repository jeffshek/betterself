import Datetime from "react-datetime";
import React, { Component } from "react";
import moment from "moment";
import { Link } from "react-router-dom";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/requests";

export class AddSleepEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      eventStartTime: moment(),
      eventEndTime: moment(),
      fitbitAuthorized: false
    };
  }

  componentDidMount() {
    this.checkIfFitbitAuthorized();
  }

  checkIfFitbitAuthorized = () => {
    const url = "/api/fitbit/user-auth-check";
    fetch(url, {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({
          fitbitAuthorized: responseData
        });
      });
  };

  submitSleepEvent = e => {
    e.preventDefault();

    const params = {
      start_time: this.state.eventStartTime.toISOString(),
      end_time: this.state.eventEndTime.toISOString(),
      source: "web"
    };

    fetch("/api/v1/sleep_activities/", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    })
      .then(response => {
        if (!response.ok) {
          alert(
            "Input Error!\n\nCheck that end date is after the start date and for overlapping periods."
          );
        }
        return response.json();
      })
      .then(responseData => {
        this.props.addEventEntry(responseData);
      });
  };

  handleStartTimeChange = moment => {
    this.setState({ eventStartTime: moment });
  };

  handleEndTimeChange = moment => {
    this.setState({ eventEndTime: moment });
  };

  renderFitbitButton() {
    if (this.state.fitbitAuthorized) {
      return (
        <div className="float-right">
          <button
            type="submit"
            id="setup-fitbit-button"
            className="btn btn-sm btn-success"
          >
            <i className="fa fa-dot-circle-o" /> Import from FitBit
          </button>
        </div>
      );
    } else {
      return (
        <div className="float-right">
          <a href="/api/fitbit/oauth2/login/">
            <button
              type="submit"
              id="setup-fitbit-button"
              className="btn btn-sm btn-success"
            >
              <i className="fa fa-dot-circle-o" /> Setup FitBit Access
            </button>
          </a>
        </div>
      );
    }
  }

  renderSubmitSleepForm() {
    return (
      <div className="card">
        <div className="card-block card-block-no-padding-bottom">
          {this.renderFitbitButton()}
          <form onSubmit={e => this.submitSleepEvent(e)}>
            <div className="row">
              <div className="form-group col-sm-4">
                <label className="add-event-label">
                  Sleep Start Time
                </label>
                <Datetime
                  onChange={this.handleStartTimeChange}
                  value={this.state.eventStartTime}
                />
              </div>
              <div className="form-group col-sm-4">
                <label className="add-event-label">
                  Sleep End Time
                </label>
                <Datetime
                  onChange={this.handleEndTimeChange}
                  value={this.state.eventEndTime}
                />
              </div>
            </div>
            <div className="float-left">
              <button
                type="submit"
                id="event-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.submitSleepEvent(e)}
              >
                <i className="fa fa-dot-circle-o" /> Log Sleep Entry
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.renderSubmitSleepForm()}
      </div>
    );
  }
}
