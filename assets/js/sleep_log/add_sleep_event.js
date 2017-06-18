import Datetime from "react-datetime";
import React, { Component, PropTypes } from "react";
import moment from "moment";
import { Link } from "react-router-dom";

export class AddSleepEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      eventStartTime: moment(),
      eventEndTime: moment()
    };

    this.submitSleepEvent = this.submitSleepEvent.bind(this);
    this.handleStartTimeChange = this.handleStartTimeChange.bind(this);
    this.handleEndTimeChange = this.handleEndTimeChange.bind(this);
  }

  submitSleepEvent(e) {
    e.preventDefault();
  }

  handleStartTimeChange(moment) {
    this.setState({ eventStartTime: moment });
  }

  handleEndTimeChange(moment) {
    this.setState({ eventEndTime: moment });
  }

  renderSubmitSleepForm() {
    return (
      <div className="card-block">
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
          <div className="float-right">
            <button
              type="submit"
              id="event-dashboard-submit"
              className="btn btn-sm btn-success"
              onClick={e => this.submitSleepEvent(e)}
            >
              <i className="fa fa-dot-circle-o" /> Add Sleep Log
            </button>
          </div>
        </form>
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        {this.renderSubmitSleepForm()}
      </div>
    );
  }
}
