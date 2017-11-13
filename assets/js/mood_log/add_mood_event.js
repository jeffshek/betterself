import Datetime from "react-datetime";
import React, { Component } from "react";
import moment from "moment";
import { Link } from "react-router-dom";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/requests";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";
import {
  DATE_REQUEST_FORMAT,
  YEAR_MONTH_DAY_FORMAT
} from "../constants/dates_and_times";

export class AddSleepEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      eventStartTime: moment(),
      eventEndTime: moment(),
      fitbitAuthorized: false,
      fitbitImportModal: false,
      apiStartDate: moment().subtract(7, "days"),
      apiEndDate: moment()
    };
  }

  handleAPIStartTimeChange = moment => {
    this.setState({ apiStartDate: moment });
  };

  handleAPIEndTimeChange = moment => {
    this.setState({ apiEndDate: moment });
  };

  componentDidMount() {
    this.checkIfFitbitAuthorized();
  }

  toggle = () => {
    this.setState({
      fitbitImportModal: !this.state.fitbitImportModal
    });
  };

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
            "Input Error!\n\nCheck that end date is after the start date OR for overlapping periods."
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

  submitUpdateFitbitAPIRequest = e => {
    e.preventDefault();

    const postParams = {
      start_date: this.state.apiStartDate.format(DATE_REQUEST_FORMAT),
      end_date: this.state.apiEndDate.format(DATE_REQUEST_FORMAT)
    };

    fetch("/api/fitbit/update-sleep-history/", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(postParams)
    })
      .then(response => {
        {
          this.toggle();
        }
        return response;
      })
      .then(responseData => {
        alert("User's FitBit history will update in the next thirty minutes.");
        return responseData;
      })
      .catch(error => {
        alert("Invalid Error Occurred When Submitting Data " + error);
      });
  };

  renderFitbitButton() {
    // Either show a logged in Fitbit Button (ie. import) or a setup FitBit
    if (this.state.fitbitAuthorized) {
      return (
        <div className="float-right">
          <button
            type="submit"
            id="setup-fitbit-button"
            className="btn btn-sm btn-success"
            onClick={this.toggle}
          >
            <i className="fa fa-dot-circle-o" /> Import from FitBit
          </button>
        </div>
      );
    } else {
      // if user doesn't have oauth setup with us yet, need to get it setup
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

  renderImportFitbitModal() {
    return (
      <Modal isOpen={this.state.fitbitImportModal} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>
          Import Sleep History from Fitbit
        </ModalHeader>
        <ModalBody>
          <label className="form-control-label add-event-label">
            Start Date
          </label>
          <Datetime
            onChange={this.handleAPIStartTimeChange}
            value={this.state.apiStartDate.format(YEAR_MONTH_DAY_FORMAT)}
          />
          <br />
          <label className="form-control-label add-event-label">
            End Date
          </label>
          <Datetime
            onChange={this.handleAPIEndTimeChange}
            value={this.state.apiEndDate.format(YEAR_MONTH_DAY_FORMAT)}
          />
          <br />
          {/*the curse of prettier*/}
          This will <b> OVERWRITE </b> any <b> OVERLAPPING </b>
          days stored. Data may take up to
          <b> THIRTY </b>
          minutes to be reflected.
          <br />
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.submitUpdateFitbitAPIRequest}>
            Update
          </Button>
          <Button color="decline-modal" onClick={this.toggle}>Cancel</Button>
        </ModalFooter>
      </Modal>
    );
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
        {this.renderImportFitbitModal()}
      </div>
    );
  }
}
