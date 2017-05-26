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
    this.state = {};

    this.submitProductivityEvent = this.submitProductivityEvent.bind(this);
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
    console.log("submit event");
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
            {this.addInputRow(
              "Very Productive (Minutes)",
              "veryProductiveMinutes"
            )}
            {this.addInputRow("Productive (Minutes)", "productiveMinutes")}
            {this.addInputRow("Neutral Time (Minutes)", "productiveMinutes")}
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
