import Datetime from "react-datetime";
import React, { Component } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";
import moment from "moment";
import { DASHBOARD_SUPPLEMENTS_URL } from "../constants/urls";
import { Link } from "react-router-dom";
import Select from "react-select";

const CreateSupplementsStackButton = () => {
  {
    return (
      <div className="card-header">
        <strong id="add-supplement-entry-text">Create Supplement Stack</strong>
      </div>
    );
  }
};

export class AddSupplementsStack extends Component {
  constructor(props) {
    super(props);

    const { supplements } = props;

    this.state = {
      formSupplementDateTime: moment(),
      supplements: supplements
    };
  }

  componentWillReceiveProps(props) {
    const { supplements } = props;
    this.setState({ supplements: supplements });
  }

  submitSupplementEvent = e => {
    e.preventDefault();

    const supplementSelected = this.state.supplements[
      this.state.selectedSupplementIndex
    ];

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
  };

  handleDateInputChange = moment => {
    this.setState({ formSupplementDateTime: moment });
  };

  handleSupplementChange = val => {
    let updatedLocation;
    if (val) {
      updatedLocation = val.value;
    } else {
      updatedLocation = null;
    }
    this.setState({
      selectedSupplementIndex: updatedLocation
    });
  };

  renderSubmitSupplementForm() {
    if (!this.state.supplements) {
      return <div />;
    }

    const supplementsKeys = Object.keys(this.state.supplements);
    // React-Select needs it in this value: label format
    const supplementDetails = supplementsKeys.map(e => {
      return {
        value: e,
        label: this.state.supplements[e].name
      };
    });

    return (
      <div className="card-block card-block-no-padding-bottom">
        <form onSubmit={e => this.submitSupplementEvent(e)}>
          <div className="row">
            <div className="col-sm-12">
              <div className="form-group">
                <label className="add-event-label">Supplement</label>
                <Select
                  name="form-field-name"
                  value={this.state.selectedSupplementIndex}
                  options={supplementDetails}
                  onChange={this.handleSupplementChange}
                />
              </div>
            </div>
          </div>
          <div className="row">
            <div className="form-group col-sm-4">
              <label className="add-event-label">
                Quantity (Serving Size)
              </label>
              <input
                type="number"
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
                  type="number"
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
              <i className="fa fa-dot-circle-o" /> Create Supplement Stack
            </button>
          </div>
        </form>
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        <CreateSupplementsStackButton />
        {this.renderSubmitSupplementForm()}
      </div>
    );
  }
}
