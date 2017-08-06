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
import {
  RESCUETIME_EXAMPLE,
  RESCUETIME_EXAMPLE_BREAKDOWN,
  RESCUETIME_LOGO
} from "../constants/image_paths";

export class AddProductivityEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modal: false,
      rescueTimeModal: false,
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
  }

  toggle = () => {
    this.setState({
      modal: !this.state.modal
    });
  };

  toggleRescueTimeHelper = () => {
    this.setState({
      rescueTimeModal: !this.state.rescueTimeModal
    });
  };

  handleInputChange = event => {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  };

  handleAPIStartTimeChange = moment => {
    this.setState({ apiStartDate: moment });
  };

  handleAPIEndTimeChange = moment => {
    this.setState({ apiEndDate: moment });
  };

  handleInputDatetimeChange = moment => {
    this.setState({ inputDateTime: moment });
  };

  addInputRow = (label, inputName) => {
    return (
      <div className="col-sm-8">
        <div className="form-group row">
          <label className="col-sm-7 form-control-label label-no-bottom-padding">
            {label}
          </label>
          <div className="col-sm-5">
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
  };

  submitUpdateRescueTimeAPIRequest = e => {
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
  };

  submitProductivityEvent = e => {
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
  };

  renderRescueTimeExplainModal() {
    return (
      <Modal
        isOpen={this.state.rescueTimeModal}
        toggle={this.toggleRescueTimeHelper}
      >
        <ModalHeader toggle={this.toggleRescueTimeHelper}>
          What is RescueTime?
        </ModalHeader>
        <ModalBody>
          <a href="https://www.rescuetime.com/rp/betterhealth" target="_blank">
            <img src={RESCUETIME_LOGO} width="100%" />
          </a>
          <br />
          <br />
          <div>
            RescueTime is an application that runs securely and privately in the background tracking time spent on applications and websites, giving an accurate picture of the day. RescueTime helps you understand your daily habits so you can focus and be more productive.
            <b>
              Click
              <a
                href="https://www.rescuetime.com/rp/betterhealth"
                target="_blank"
              >
                here
              </a>
              or the image below for a referral link.
            </b>
          </div>

          <br />
          <div>
            <a
              href="https://www.rescuetime.com/rp/betterhealth"
              target="_blank"
            >
              <img src={RESCUETIME_EXAMPLE} width="100%" />
              <br />
              <img src={RESCUETIME_EXAMPLE_BREAKDOWN} width="100%" />
            </a>
          </div>

        </ModalBody>
      </Modal>
    );
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
          <div className="float-left">
            <button
              type="submit"
              id="explain-rescuetime"
              className="btn btn-sm btn-success"
              onClick={this.toggleRescueTimeHelper}
            >
              <div id="white-text">
                <i className="fa fa-dot-circle-o" /> What is RescueTime?
              </div>
            </button>
          </div>
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
            <div className="row">
              <div className="cols-2 col-sm-5">
                <label className="add-event-label">
                  Productivity Date
                </label>
                <div className="form-group col-sm-8">
                  <Datetime
                    onChange={this.handleInputDatetimeChange}
                    value={this.state.inputDateTime.format(
                      YEAR_MONTH_DAY_FORMAT
                    )}
                  />
                </div>
                <label className="add-event-label">
                  Log Productivity Time (In Minutes)
                </label>
                {this.addInputRow("Very Productive", "veryProductiveMinutes")}
                {this.addInputRow("Productive", "productiveMinutes")}
                {this.addInputRow("Neutral", "neutralMinutes")}
                {this.addInputRow("Distracting", "distractingMinutes")}
                {this.addInputRow("Very Distracting", "veryDistractingMinutes")}
              </div>

            </div>
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
        {this.state.rescueTimeModal
          ? <div>{this.renderRescueTimeExplainModal()}</div>
          : <div />}
      </div>
    );
  }
}
