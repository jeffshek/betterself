import Datetime from "react-datetime";
import React, { Component, PropTypes } from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/util_constants";
import moment from "moment";
import { Link } from "react-router-dom";

export class AddProductivityEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      inputDate: moment(),
      // Default state for productivity, 0.
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

  getPossibleSupplements() {
    fetch("/api/v1/supplements", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        const supplementNames = responseData.map(object => object.name);
        this.setState({ supplements: responseData });
        this.setState({ supplementNames: supplementNames });
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

  componentDidMount() {
    this.getPossibleSupplements();
  }

  submitProductivityEvent(e) {
    e.preventDefault();
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
              <label className="add-supplement-label">
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
                id="supplement-dashboard-submit"
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
