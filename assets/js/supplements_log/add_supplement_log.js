import Datetime from "react-datetime";
import React, { Component } from "react";
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
    const { supplements, supplementStacks } = props;
    this.setState({ supplements: supplements });
    this.setState({ supplementStacks: supplementStacks });
  }

  submitIndividualSupplement = indexLocation => {
    const supplement = this.state.supplements[indexLocation];

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

  submitSupplementStack = indexLocation => {
    const supplementStack = this.state.supplementStack[indexLocation];

    const time = this.state.formSupplementDateTime.toISOString();

    const postParams = {
      supplement_uuid: supplementStack.uuid,
      time: time,
      source: "web"
    };
  };

  submitSupplementEvent = e => {
    e.preventDefault();

    const supplementStackLength = this.state.supplementStacks.length;

    let supplementStackSelected;
    // For the underlying array, what is true point that was selected?
    let selectionIndex = this.state.selectedSupplementIndex;
    if (this.state.selectedSupplementIndex < supplementStackLength) {
      supplementStackSelected = true;
    } else {
      supplementStackSelected = false;
      // If a stack wasn't selected, but the stack is a length of 4
      // we want to subtract 4 from it
      selectionIndex = selectionIndex - supplementStackLength;
    }

    if (supplementStackSelected) {
      this.submitSupplementStack(selectionIndex);
    } else {
      this.submitIndividualSupplement(selectionIndex);
    }
  };

  handleDateInputChange = moment => {
    this.setState({ formSupplementDateTime: moment });
  };

  handleSupplementSelectionChange = val => {
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

    // Combine both to allow a user to select a stack or an individual supplement
    const supplementsAndStacks = this.state.supplementStacks.concat(
      this.state.supplements
    );

    const supplementStackKeys = Object.keys(supplementsAndStacks);
    const supplementStackDetails = supplementStackKeys.map(e => {
      return {
        value: e,
        label: supplementsAndStacks[e].name
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
                  options={supplementStackDetails}
                  onChange={this.handleSupplementSelectionChange}
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
