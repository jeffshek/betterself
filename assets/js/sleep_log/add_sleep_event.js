import Datetime from "react-datetime";
import React, { Component, PropTypes } from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/util_constants";
import moment from "moment";
import { DASHBOARD_SUPPLEMENTS_URL } from "../constants/urls";
import { Link } from "react-router-dom";

export class AddSupplementEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      formSupplementDateTime: moment(),
      supplements: []
    };

    this.submitSupplementEvent = this.submitSupplementEvent.bind(this);
    this.handleDateInputChange = this.handleDateInputChange.bind(this);
  }

  getPossibleSupplements() {
    fetch("/api/v1/supplements/", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({ supplements: responseData });
      });
  }

  componentDidMount() {
    this.getPossibleSupplements();
  }

  submitSupplementEvent(e) {
    e.preventDefault();

    const supplementLocation = this.supplementNameKey.value;
    const supplementSelected = this.state.supplements[supplementLocation];

    // api parameters used to send
    const supplementUUID = supplementSelected.uuid;
    const quantity = this.servingSize.value;
    const time = this.state.formSupplementDateTime.toISOString();
    const source = "web";
    const durationMinutes = this.durationMinutes.value;

    const postParams = {
      supplement_uuid: supplementUUID,
      quantity: quantity,
      time: time,
      source: source,
      duration_minutes: durationMinutes
    };

    fetch("/api/v1/supplement_events/", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(postParams)
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.props.addEventEntry(responseData);
      });
  }

  handleDateInputChange(moment) {
    this.setState({ formSupplementDateTime: moment });
  }

  renderCreateSupplementButton() {
    return (
      <div className="card-header">
        <strong id="add-supplement-entry-text">Add Supplement Entry</strong>
        <Link to={DASHBOARD_SUPPLEMENTS_URL}>
          <div className="float-right">
            <button
              type="submit"
              id="create-new-supplement-button"
              className="btn btn-sm btn-success"
            >
              <div id="white-text">
                <i className="fa fa-dot-circle-o" /> Create Supplement
              </div>
            </button>
          </div>
        </Link>
      </div>
    );
  }

  renderSubmitSupplementForm() {
    const supplementsKeys = Object.keys(this.state.supplements);

    return (
      <div className="card-block">
        <form onSubmit={e => this.submitSupplementEvent(e)}>
          <div className="row">
            <div className="col-sm-12">
              <div className="form-group">
                <label className="add-event-label">Supplement</label>
                <select
                  className="form-control"
                  ref={input => this.supplementNameKey = input}
                >
                  {/*List out all the possible supplements, use the index as the key*/}
                  {supplementsKeys.map(key => (
                    <option value={key} key={key}>
                      {this.state.supplements[key].name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="form-group col-sm-4">
              <label className="add-event-label">
                Quantity (Serving Size)
              </label>
              <input
                type="text"
                className="form-control"
                defaultValue="1"
                ref={input => this.servingSize = input}
              />
            </div>
            <div className="form-group col-sm-4">
              <label className="add-event-label">
                Date / Time of Ingestion
              </label>
              {/*Use the current datetime as a default */}
              <Datetime
                onChange={this.handleDateInputChange}
                value={this.state.formSupplementDateTime}
              />
            </div>
            <div className="col-sm-4">
              <div className="form-group">
                <label className="add-event-label">
                  Duration (Minutes)
                </label>
                <input
                  type="text"
                  className="form-control"
                  defaultValue="0"
                  ref={input => this.durationMinutes = input}
                />
              </div>
            </div>
          </div>
          <div className="float-right">
            <button
              type="submit"
              id="event-dashboard-submit"
              className="btn btn-sm btn-success"
              onClick={e => this.submitSupplementEvent(e)}
            >
              <i className="fa fa-dot-circle-o" /> Add Supplement Log
            </button>
          </div>
        </form>
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        {this.renderCreateSupplementButton()}
        {this.renderSubmitSupplementForm()}
      </div>
    );
  }
}
