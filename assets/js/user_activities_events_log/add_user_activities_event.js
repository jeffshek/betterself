import Datetime from "react-datetime";
import React, { Component } from "react";
import moment from "moment";
import { CubeLoadingStyle } from "../constants/loading_styles";
import { Creatable } from "react-select";
import { SelectDetailsSerializer } from "../utils/select_utils";
import { USER_ACTIVITIES_EVENTS_RESOURCE_URL } from "../constants/urls";
import { postFetchJSONAPI } from "../utils/fetch_utils";
import { RenderCreateActivityButton } from "../user_activities_log/constants";
import { USER_ACTIVITIES_RESOURCE_URL } from "../constants/urls";

export class AddUserActivityEvent extends Component {
  constructor() {
    super();
    this.state = {
      inputDateTime: moment()
    };
  }

  handleInputChange = event => {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  };

  handleDatetimeChange = moment => {
    this.setState({ inputDateTime: moment });
  };

  handleIndexChange = val => {
    this.setState({
      activityTypeIndexSelected: val.value
    });
  };

  onNewOptionClick = props => {
    const { label } = props;
    const postParams = {
      name: label
    };

    postFetchJSONAPI(
      USER_ACTIVITIES_RESOURCE_URL,
      postParams
    ).then(responseData => {
      window.location.reload();
    });
  };

  renderActivitySelect() {
    const activitiesDetails = SelectDetailsSerializer(
      this.props.userActivityTypes
    );

    return (
      <div className="col-sm-4">
        <div className="form-group">
          <label className="add-event-label">
            Activity Type
          </label>
          <Creatable
            name="form-field-name"
            value={this.state.activityTypeIndexSelected}
            onNewOptionClick={this.onNewOptionClick}
            options={activitiesDetails}
            onChange={this.handleIndexChange}
          />
        </div>
      </div>
    );
  }

  renderInputRow = (label, inputName) => {
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
  };

  submitEventDetails = e => {
    e.preventDefault();
    const indexSelected = this.state.activityTypeIndexSelected;
    const userActivityUUIDSelected = this.props.userActivityTypes[indexSelected]
      .uuid;

    const postParams = {
      user_activity_uuid: userActivityUUIDSelected,
      duration_minutes: this.state.durationMinutes,
      time: this.state.inputDateTime.toISOString(),
      source: "web"
    };

    postFetchJSONAPI(USER_ACTIVITIES_EVENTS_RESOURCE_URL, postParams)
      .then(responseData => {
        this.props.addEventEntry(responseData);
        return responseData;
      })
      .catch(error => {
        alert("Invalid Error Occurred When Submitting Data " + error);
      });
  };

  renderSubmitEventForm() {
    return (
      <div className="card">
        <div className="card-block card-block-no-padding-bottom">
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
    if (!this.props.renderReady) {
      return <CubeLoadingStyle />;
    }

    return (
      <div>
        <RenderCreateActivityButton />
        {this.renderSubmitEventForm()}
      </div>
    );
  }
}
