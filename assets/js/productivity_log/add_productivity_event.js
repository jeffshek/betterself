import Datetime from "react-datetime";
import React, { Component, PropTypes } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/util_constants";
import moment from "moment";
import { Link } from "react-router-dom";
import { YEAR_MONTH_DAY_FORMAT } from "../constants/dates";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";

export class AddProductivityEvent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      inputDateTime: moment(),
      veryProductiveMinutes: 0,
      productiveMinutes: 0,
      neutralMinutes: 0,
      distractingMinutes: 0,
      veryDistractingMinutes: 0
    };

    this.submitProductivityEvent = this.submitProductivityEvent.bind(this);
    this.handleDatetimeChange = this.handleDatetimeChange.bind(this);
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
        <div className="form-group row">
          <label className="col-md-3 form-control-label">{label} </label>
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

  submitProductivityEvent(e) {
    e.preventDefault();

    const postParams = {
      very_productive_time_minutes: this.state.veryProductiveMinutes,
      productive_time_minutes: this.state.productiveMinutes,
      neutral_time_minutes: this.state.neutralMinutes,
      distracting_time_minutes: this.state.distractingMinutes,
      very_distracting_time_minutes: this.state.veryDistractingMinutes,
      date: this.state.inputDateTime.format("YYYY-MM-D")
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
        alert("Invalid Error Occurred When Submitting Data");
      });
  }

  handleDatetimeChange(moment) {
    this.setState({ inputDateTime: moment });
  }

  renderImportModal() {
    const supplementKeys = Object.keys(this.props.supplements);
    const supplementNames = supplementKeys.map(
      key => this.props.supplements[key].name
    );
    const indexOfSupplementSelected = supplementNames.indexOf(
      this.state.editObject["supplement_name"]
    );

    return (
      <Modal isOpen={this.state.modal} toggle={this.toggle}>
        <ModalHeader toggle={this.toggle}>Edit Supplement</ModalHeader>
        <ModalBody>
          <label className="form-control-label add-event-label">
            Supplement
          </label>
          <select
            className="form-control"
            name="activityTypeIndexSelected"
            onChange={this.handleSupplementChangeOnEditObject}
            value={indexOfSupplementSelected}
          >
            {supplementKeys.map(key => (
              <option value={key} key={key}>
                {this.props.supplements[key].name}
              </option>
            ))}
          </select>
          <br />
          <label className="form-control-label add-event-label">
            Serving Size
          </label>
          <input
            name="servingSizeUpdate"
            type="text"
            className="form-control"
            defaultValue={this.state.editObject["quantity"]}
            onChange={this.handleInputChange}
          />
          <br />
          <label className="form-control-label add-event-label">
            Time
          </label>
          <Datetime
            onChange={this.handleDatetimeChangeOnEditObject}
            value={this.state.editObject.time}
          />
        </ModalBody>
        <ModalFooter>
          <Button color="primary" onClick={this.submitEdit}>Update</Button>
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
            >
              <div id="white-text">
                <i className="fa fa-dot-circle-o" /> Import from RescueTime
              </div>
            </button>
          </div>
        </div>

        <div className="card-block">
          <form onSubmit={e => this.submitProductivityEvent(e)}>
            <label className="add-event-label">
              Productivity Date
            </label>
            <div className="form-group col-sm-4">
              {/*Use the current datetime as a default */}
              <Datetime
                onChange={this.handleDatetimeChange}
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
      </div>
    );
  }
}
