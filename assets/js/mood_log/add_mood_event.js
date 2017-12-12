import Datetime from "react-datetime";
import React, { Component } from "react";
import moment from "moment";
import { MOOD_RESOURCE_URL } from "../constants/urls";
import { postFetchJSONAPI } from "../utils/fetch_utils";

export class AddMoodEvent extends Component {
  constructor() {
    super();
    this.state = {
      inputDateTime: moment(),
      moodValue: 5,
      notes: ""
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

  renderInputRow = (label, inputName) => {
    return (
      <div className="col-sm-3">
        <div className="form-group">
          <label className="add-event-label">
            {label}
          </label>
          <input
            name={inputName}
            type="number"
            className="form-control"
            defaultValue={5}
            onChange={this.handleInputChange}
          />
        </div>
      </div>
    );
  };

  renderTextInputRow = (label, inputName) => {
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
            onChange={this.handleInputChange}
          />
        </div>
      </div>
    );
  };

  submitEventDetails = e => {
    e.preventDefault();

    const postParams = {
      value: this.state.moodValue,
      time: this.state.inputDateTime.toISOString(),
      source: "web"
    };

    if (this.state.notes !== "") {
      postParams.notes = this.state.notes;
    }

    postFetchJSONAPI(MOOD_RESOURCE_URL, postParams)
      .then(responseData => {
        window.location.reload();
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
            <div className="form-group col-sm-3">
              <label className="add-event-label">
                Time
              </label>
              <Datetime
                onChange={this.handleDatetimeChange}
                value={this.state.inputDateTime}
              />
            </div>
            {this.renderInputRow(
              "Mood - Score of 1 to 10, 10 being the happiest!",
              "moodValue"
            )}
            {this.renderTextInputRow(
              "Notes / Details (ie. Got a promotion!)",
              "notes"
            )}
            <div className="float-right">
              <button
                type="submit"
                id="event-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.submitEventDetails(e)}
              >
                <i className="fa fa-dot-circle-o" /> Log Mood
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
        {this.renderSubmitEventForm()}
      </div>
    );
  }
}
