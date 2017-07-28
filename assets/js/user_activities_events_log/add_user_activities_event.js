import Datetime from "react-datetime";
import React, { Component, PropTypes } from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/requests";
import moment from "moment";
import { Link } from "react-router-dom";
import { DASHBOARD_USER_ACTIVITIES_URL } from "../constants/urls";
import { CubeLoadingStyle } from "../constants/loading_styles";

export class AddUserActivityEvent extends Component {
  constructor() {
    super();
    this.state = {
      inputDateTime: moment()
    };

    this.submitEventDetails = this.submitEventDetails.bind(this);
    this.handleDatetimeChange = this.handleDatetimeChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.renderInputRow = this.renderInputRow.bind(this);
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
    const activitiesKeys = Object.keys(this.props.userActivityTypes);

    return (
      <div className="col-sm-4">
        <div className="form-group">
          <label className="add-event-label">
            Activity Type
          </label>
          <select
            className="form-control"
            ref={input => this.activityTypeIndexSelected = input}
          >
            {/*List out all the possible supplements, use the index as the key*/}
            {activitiesKeys.map(key => (
              <option value={key} key={key}>
                {this.props.userActivityTypes[key].name}
              </option>
            ))}
          </select>
        </div>
      </div>
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
    const indexSelected = this.activityTypeIndexSelected.value;
    const userActivityUUIDSelected = this.props.userActivityTypes[indexSelected]
      .uuid;

    const postParams = {
      user_activity_uuid: userActivityUUIDSelected,
      duration_minutes: this.state.durationMinutes,
      time: this.state.inputDateTime.toISOString(),
      source: "web"
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
        alert("Invalid Error Occurred When Submitting Data " + error);
      });
  }

  renderCreateActivityButton() {
    return (
      <div className="card-header">
        <strong id="add-supplement-entry-text">Add Activity Event</strong>
        <Link to={DASHBOARD_USER_ACTIVITIES_URL}>
          <div className="float-right">
            <button
              type="submit"
              id="add-new-object-button"
              className="btn btn-sm btn-success"
            >
              <div id="white-text">
                <i className="fa fa-dot-circle-o" /> Create Activity Type
              </div>
            </button>
          </div>
        </Link>
      </div>
    );
  }

  renderSubmitEventForm() {
    return (
      <div className="card">
        <div className="card-block">
          <form onSubmit={e => this.submitEventDetails(e)}>
            <div className="form-group col-sm-4">
              <label className="add-event-label">
                Time
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

  render() {
    return (
      <div>
        {!this.props.renderReady
          ? <CubeLoadingStyle />
          : <div>
              {this.renderCreateActivityButton()}
              {this.renderSubmitEventForm()}
            </div>}
      </div>
    );
  }
}
