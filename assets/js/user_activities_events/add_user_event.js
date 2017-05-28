import Datetime from "react-datetime";
import React, { Component, PropTypes } from "react";
import {
  JSON_POST_AUTHORIZATION_HEADERS,
  JSON_AUTHORIZATION_HEADERS
} from "../constants/util_constants";
import moment from "moment";
import { Link } from "react-router-dom";

export class AddUserActivityEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      inputDateTime: moment(),
      userActivities: []
    };

    this.submitEventDetails = this.submitEventDetails.bind(this);
    this.handleDatetimeChange = this.handleDatetimeChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.renderInputRow = this.renderInputRow.bind(this);
  }

  componentDidMount() {
    this.getPossibleActivities();
  }

  getPossibleActivities() {
    fetch("/api/v1/user_activities", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({ userActivities: responseData });
      });
  }

  handleInputChange(event) {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  }

  handleDatetimeChange(moment) {
    this.setState({ inputDateTime: moment });
  }

  renderActivitySelect() {
    const activitiesKeys = Object.keys(this.state.userActivities);

    return (
      <select
        className="form-control"
        ref={input => this.activityNameKey = input}
      >
        {/*List out all the possible supplements, use the index as the key*/}
        {activitiesKeys.map(key => (
          <option value={key} key={key}>
            {this.state.userActivities[key].name}
          </option>
        ))}
      </select>
    );
  }

  renderInputRow(label, inputName) {
    return (
      <div className="col-sm-4">
        <div className="form-group">
          <label className="add-event-label">
            {label}
          </label>
          <input
            name={inputName}
            type="text"
            className="form-control"
            defaultValue={0}
            onChange={this.handleInputChange}
          />
        </div>
      </div>
    );
  }

  submitEventDetails(e) {
    e.preventDefault();

    const postParams = {
      very_productive_time_minutes: this.state.veryProductiveMinutes,
      productive_time_minutes: this.state.productiveMinutes,
      neutral_time_minutes: this.state.neutralMinutes,
      distracting_time_minutes: this.state.distractingMinutes,
      very_distracting_time_minutes: this.state.veryDistractingMinutes,
      time: this.state.inputDateTime.toISOString()
    };

    fetch("api/v1/user_activity_events/", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(postParams)
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.props.addEventEntry(responseData);
        return responseData;
      })
      .catch(error => {
        alert("Invalid Error Occurred When Submitting Data");
      });
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <strong id="add-supplement-entry-text">
            Log Event
          </strong>
        </div>

        <div className="card-block">
          <form onSubmit={e => this.submitEventDetails(e)}>
            <div className="form-group col-sm-4">
              <label className="add-event-label">
                Date
              </label>
              <Datetime
                onChange={this.handleDatetimeChange}
                value={this.state.inputDateTime}
              />
            </div>

            {this.renderActivitySelect()}
            {this.renderInputRow("Duration (Minutes)", "durationMinutes")}

            <div className="float-right">
              <button
                type="submit"
                id="event-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.submitEventDetails(e)}
              >
                <i className="fa fa-dot-circle-o" /> Log Event
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }
}
