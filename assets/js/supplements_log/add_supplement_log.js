import Datetime from "react-datetime";
import React, { Component } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";
import moment from "moment";
import { DASHBOARD_SUPPLEMENTS_URL } from "../constants/urls";
import { Link } from "react-router-dom";
import Select from "react-select";
import { postFetchJSONAPI } from "../utils/fetch_utils";

const CreateSupplementButton = () => {
  {
    return (
      <div className="card-header">
        <strong id="add-supplement-entry-text">Log Supplement Entry</strong>
        <Link to={DASHBOARD_SUPPLEMENTS_URL}>
          <div className="float-right">
            <button
              type="submit"
              id="add-new-object-button"
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
};

export class AddSupplementLog extends Component {
  constructor() {
    super();

    this.state = {
      formSupplementDateTime: moment()
    };
  }

  componentWillReceiveProps(props) {
    const { supplements } = props;
    this.setState({ supplements: supplements });
  }

  submitIndividualSupplement = supplement => {
    // api parameters used to send
    const supplementUUID = supplement.uuid;
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

    const url = "/api/v1/supplement_events/";
    postFetchJSONAPI(url, postParams).then(responseData => {
      this.props.addEventEntry(responseData);
    });
  };

  submitSupplementEvent = e => {
    e.preventDefault();

    const supplement = this.state.supplements[
      this.state.selectedSupplementIndex
    ];

    this.submitIndividualSupplement(supplement);
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
              <i className="fa fa-dot-circle-o" /> Log Supplement Entry
            </button>
          </div>
        </form>
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        <CreateSupplementButton />
        {this.renderSubmitSupplementForm()}
      </div>
    );
  }
}
