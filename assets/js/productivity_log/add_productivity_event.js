import Datetime from "react-datetime";
import React, { Component } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";
import moment from "moment";
import { Link } from "react-router-dom";
import {
  DATE_REQUEST_FORMAT,
  YEAR_MONTH_DAY_FORMAT
} from "../constants/dates_and_times";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";

export class AddProductivityEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modal: false,
      inputDateTime: moment(),
      veryProductiveMinutes: 0,
      productiveMinutes: 0,
      neutralMinutes: 0,
      distractingMinutes: 0,
      veryDistractingMinutes: 0,
      // Picking a week ago just since that seems like a reasonable default
      apiStartDate: moment().subtract(7, "days"),
      apiEndDate: moment(),
      apiRescueTimeKey: "RESCUETIME_API_KEY_SAMPLE-A32jWZ-219ZE-135ZFF"
    };
    this.addInputRow = this.addInputRow.bind(this);

    this.submitProductivityEvent = this.submitProductivityEvent.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleInputDatetimeChange = this.handleInputDatetimeChange.bind(this);

    // Used for the API Modals
    this.toggle = this.toggle.bind(this);
    this.handleAPIStartTimeChange = this.handleAPIStartTimeChange.bind(this);
    this.handleAPIEndTimeChange = this.handleAPIEndTimeChange.bind(this);
    this.submitUpdateRescueTimeAPIRequest = this.submitUpdateRescueTimeAPIRequest.bind(
      this
    );
  }

  toggle() {
    this.setState({
      modal: !this.state.modal
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

  handleAPIStartTimeChange(moment) {
    this.setState({ apiStartDate: moment });
  }

  handleAPIEndTimeChange(moment) {
    this.setState({ apiEndDate: moment });
  }

  handleInputDatetimeChange(moment) {
    this.setState({ inputDateTime: moment });
  }

  addInputRow(label, inputName) {
    return (
      <div className="col-sm-4">
        <div className="form-group row">
          <label className="col-md-3 form-control-label label-no-bottom-padding">
            {label}{" "}
          </label>
          <div className="col-sm-9">
            <input
              type="number"
              id="number-input"
              name={inputName}
              className="form-control"
              placeholder={0}
              onChange={this.handleInputChange}
            />
          </div>
        </div>
      </div>
    );
  }

  submitUpdateRescueTimeAPIRequest(e) {
    e.preventDefault();

    const postParams = {
      start_date: this.state.apiStartDate.format(DATE_REQUEST_FORMAT),
      end_date: this.state.apiEndDate.format(DATE_REQUEST_FORMAT),
      rescuetime_api_key: this.state.apiRescueTimeKey
    };

    fetch("/api/v1/rescuetime/update-productivity-history", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(postParams)
    })
      .then(response => {
        // Turn off the modal after the request has been sent.
        {
          this.toggle();
        }
        return response;
      })
      .then(responseData => {
        alert(
          "User's RescueTime history will update in the next thirty minutes."
        );
        return responseData;
      })
      .catch(error => {
        alert("Invalid Error Occurred When Submitting Data " + error);
      });
  }

  submitProductivityEvent(e) {
    e.preventDefault();

    const postParams = {
      very_productive_time_minutes: this.state.veryProductiveMinutes,
      productive_time_minutes: this.state.productiveMinutes,
      neutral_time_minutes: this.state.neutralMinutes,
      distracting_time_minutes: this.state.distractingMinutes,
      very_distracting_time_minutes: this.state.veryDistractingMinutes,
      date: this.state.inputDateTime.format(DATE_REQUEST_FORMAT)
    };

    fetch("api/v1/productivity_log/", {
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
        alert("Invalid Error Occurred When Submitting Data " + error);
      });
  }

  renderImportModal() {
    return (
      <Modal isOpen={this.state.modal} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>
          Import Historically from RescueTime
        </ModalHeader>
        <ModalBody>
          <label className="form-control-label add-event-label">
            RescueTime API Key
          </label>
          <input
            name="apiRescueTimeKey"
            type="text"
            className="form-control"
            defaultValue={this.state.apiRescueTimeKey}
            onChange={this.handleInputChange}
          />
          <br />
          <label className="form-control-label add-event-label">
            Start Date
          </label>
          <Datetime
            onChange={this.handleAPIStartTimeChange}
            value={this.state.apiStartDate.format(YEAR_MONTH_DAY_FORMAT)}
          />
          <br />
          <label className="form-control-label add-event-label">
            End Date
          </label>
          <Datetime
            onChange={this.handleAPIEndTimeChange}
            value={this.state.apiEndDate.format(YEAR_MONTH_DAY_FORMAT)}
          />
          <br />
          This will OVERWRITE any days already stored from RescueTime. Data may take up to THIRTY minutes to be reflected.
        </ModalBody>
        <ModalFooter>
          <Button
            color="primary"
            onClick={this.submitUpdateRescueTimeAPIRequest}
          >
            Update
          </Button>
          <Button color="decline-modal" onClick={this.toggle}>Cancel</Button>
        </ModalFooter>
      </Modal>
    );
  }

  renderAddProductivityTimeManually() {
    return (
      <div className="card">
        <div className="card-header">
          <strong id="add-supplement-entry-text">
            Add RescueTime Productivity
          </strong>
          <div className="float-right">
            <button
              type="submit"
              id="add-new-object-button"
              className="btn btn-sm btn-success"
              onClick={this.toggle}
            >
              <div id="white-text">
                <i className="fa fa-dot-circle-o" /> Import from RescueTime
              </div>
            </button>
          </div>
        </div>

        <div className="card-block card-block-no-padding-bottom">
          <form onSubmit={e => this.submitProductivityEvent(e)}>
            <label className="add-event-label">
              Productivity Date
            </label>
            <div className="form-group col-sm-4">
              {/*Use the current datetime as a default */}
              <Datetime
                onChange={this.handleInputDatetimeChange}
                value={this.state.inputDateTime.format(YEAR_MONTH_DAY_FORMAT)}
              />
            </div>
            <label className="add-event-label">
              Productivity Time (In Minutes)
            </label>
            {this.addInputRow("Very Productive", "veryProductiveMinutes")}
            {this.addInputRow("Productive", "productiveMinutes")}
            {this.addInputRow("Neutral", "neutralMinutes")}
            {this.addInputRow("Distracting", "distractingMinutes")}
            {this.addInputRow("Very Distracting", "veryDistractingMinutes")}

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

  render() {
    return (
      <div>
        {this.renderAddProductivityTimeManually()}
        {this.state.modal ? <div>{this.renderImportModal()}</div> : <div />}
      </div>
    );
  }
}
