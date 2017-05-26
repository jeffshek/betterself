import Datetime from "react-datetime";
import React, { Component, PropTypes } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import moment from "moment";
import { Link } from "react-router-dom";

export class AddProductivityEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      inputDate: moment(),
      veryProductiveMinutes: 0,
      productiveMinutes: 0,
      neutralMinutes: 0,
      distractingMinutes: 0,
      veryDistractingMinutes: 0
    };

    this.submitProductivityEvent = this.submitProductivityEvent.bind(this);
    this.handleDateChange = this.handleDateChange.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.addInputRow = this.addInputRow.bind(this);
  }

  handleInputChange(event) {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  }

  addInputRow(label, inputName) {
    return (
      <div className="col-sm-4">
        <div className="form-group">
          <label>
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

  submitProductivityEvent(e) {
    e.preventDefault();

    const postParams = {
      very_productive_time_minutes: this.state.veryProductiveMinutes,
      productive_time_minutes: this.state.productiveMinutes,
      neutral_time_minutes: this.state.neutralMinutes,
      distracting_time_minutes: this.state.distractingMinutes,
      very_distracting_time_minutes: this.state.veryDistractingMinutes,
      date: this.state.inputDate.format("YYYY-MM-D")
    };

    fetch("api/v1/productivity_log", {
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

  handleDateChange(moment) {
    this.setState({ inputDate: moment });
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <strong id="add-supplement-entry-text">
            Log Daily Productivity Time
          </strong>
        </div>

        <div className="card-block">
          <form onSubmit={e => this.submitProductivityEvent(e)}>

            <div className="form-group col-sm-4">
              <label className="add-event-label">
                Date
              </label>
              {/*Use the current datetime as a default */}
              <Datetime
                onChange={this.handleDateChange}
                value={this.state.inputDate.format("MMMM Do YYYY")}
              />
            </div>

            {this.addInputRow(
              "Very Productive (Minutes)",
              "veryProductiveMinutes"
            )}
            {this.addInputRow("Productive (Minutes)", "productiveMinutes")}
            {this.addInputRow("Neutral Time (Minutes)", "neutralMinutes")}
            {this.addInputRow(
              "Distracting Time (Minutes)",
              "distractingMinutes"
            )}
            {this.addInputRow(
              "Very Distracting Time (Minutes)",
              "veryDistractingMinutes"
            )}

            <div className="float-right">
              <button
                type="submit"
                id="event-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.submitProductivityEvent(e)}
              >
                <i className="fa fa-dot-circle-o" /> Log Productivity
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }
}
