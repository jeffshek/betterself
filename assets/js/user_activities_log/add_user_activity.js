import React, { Component } from "react";
import moment from "moment";
import { USER_ACTIVITIES_RESOURCE_URL } from "../constants/urls";
import { postFetchJSONAPI } from "../utils/fetch_utils";
import { RenderCreateActivityButton } from "./constants";

export class AddUserActivity extends Component {
  constructor(props) {
    super(props);
    this.state = {
      inputDateTime: moment()
    };

    this.submitEventDetails = this.submitEventDetails.bind(this);
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

  renderInputRow(label, inputName) {
    return (
      <div className="col-sm-7">
        <div className="form-group">
          <label className="add-event-label">
            {label}
          </label>
          <input
            name={inputName}
            type="text"
            className="form-control"
            defaultValue="Add Activity Type"
            onChange={this.handleInputChange}
          />
        </div>
      </div>
    );
  }

  submitEventDetails(e) {
    e.preventDefault();

    const postParams = {
      is_significant_activity: this.isSignificant.value,
      is_negative_activity: this.isNegative.value,
      is_all_day_activity: this.isAllDay.value,
      name: this.state["activityName"]
    };

    postFetchJSONAPI(USER_ACTIVITIES_RESOURCE_URL, postParams)
      .then(responseData => {
        this.props.addEventEntry(responseData);
        return responseData;
      })
      .catch(error => {
        alert("Invalid Error Occurred When Submitting Data " + error);
      });
  }

  renderSubmitEventForm() {
    return (
      <div className="card">
        <div className="card-block">
          <form onSubmit={e => this.submitEventDetails(e)}>
            {this.renderInputRow("Activity Name", "activityName")}
            <label className="col-md-3 form-control-label add-event-label">
              Is Significant?
            </label>
            <div className="col-md-4">
              <select
                id="select"
                name="select"
                className="form-control"
                size="1"
                defaultValue={false}
                ref={input => this.isSignificant = input}
              >
                <option value={true}>True</option>
                <option value={false}>False</option>
              </select>
            </div>
            <br />
            <label className="col-md-3 form-control-label add-event-label">
              Is All Day?
            </label>
            <div className="col-md-4">
              <select
                id="select"
                name="select"
                className="form-control"
                size="1"
                defaultValue={false}
                ref={input => this.isAllDay = input}
              >
                &gt;
                <option value={true}>True</option>
                <option value={false}>False</option>
              </select>
            </div>
            <br />
            <label className="col-md-3 form-control-label add-event-label">
              Is Negative?
            </label>
            <div className="col-md-4">
              <select
                id="select"
                name="select"
                className="form-control"
                size="1"
                defaultValue={false}
                ref={input => this.isNegative = input}
              >
                &gt;
                <option value={true}>True</option>
                <option value={false}>False</option>
              </select>
            </div>
            <div className="float-right">
              <button
                type="submit"
                id="event-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.submitEventDetails(e)}
              >
                <i className="fa fa-dot-circle-o" /> Create Activity Type
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
        <RenderCreateActivityButton />
        {this.renderSubmitEventForm()}
      </div>
    );
  }
}
