import React, { Component } from "react";
import { getFetchJSONAPI, postFetchJSONAPI } from "../utils/fetch_utils";
import { CubeLoadingStyle } from "../constants/loading_styles";
import moment from "moment";
import Datetime from "react-datetime";
import { TEXT_TIME_FORMAT } from "../constants/dates_and_times";
import { CreateSupplement } from "../supplements/constants";

export class AddSupplementReminderView extends Component {
  constructor(props) {
    super();

    this.state = {
      supplements: null,
      inputDateTime: moment(),
      phoneNumber: "",
      supplementQuantity: 1
    };

    const { reminders } = props;
    if (reminders.length > 0) {
      // because you can add a reminder without a phoneNumber
      if (reminders[0].phone_number_details) {
        this.state["phoneNumber"] =
          reminders[0].phone_number_details.phone_number;
      }
    }
  }

  handleInputChange = event => {
    const target = event.target;
    const name = target.name;
    const value = target.value;

    this.setState({
      [name]: value
    });
  };

  submitEventDetails(e) {
    e.preventDefault();

    const indexSelected = this.state.supplementIndexSelected.value;
    const supplementUUIDSelected = this.state.supplements[indexSelected].uuid;

    const utcTime = this.state.inputDateTime.utc();
    const utcTimeString = utcTime.format("HH:mm");

    const phoneParams = {
      phone_number: this.state.phoneNumber
    };
    const phoneUrl = "api/v1/user/phone_number/";
    postFetchJSONAPI(phoneUrl, phoneParams).then(responseData => {
      return responseData;
    });

    const postParams = {
      supplement_uuid: supplementUUIDSelected,
      quantity: this.state.supplementQuantity,
      reminder_time: utcTimeString,
      source: "web"
    };

    const reminderUrl = "api/v1/supplement_reminders/";
    postFetchJSONAPI(reminderUrl, postParams).then(responseData => {
      window.location.reload();
      return responseData;
    });
  }

  renderSupplementsSelect() {
    const supplementsKeys = Object.keys(this.state.supplements);

    return (
      <div className="col-sm-4">
        <div className="form-group">
          <label className="add-event-label">
            Supplement Name
          </label>
          <select
            className="form-control"
            ref={input => this.state.supplementIndexSelected = input}
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
    );
  }

  renderInputRow(label, inputName, defaultValue = 1) {
    return (
      <div className="col-sm-6">
        <div className="form-group">
          <label className="add-event-label">
            {label}
          </label>
          <input
            name={inputName}
            type="text"
            className="form-control"
            defaultValue={defaultValue}
            onChange={this.handleInputChange}
          />
        </div>
      </div>
    );
  }

  handleDatetimeChange = moment => {
    this.setState({ inputDateTime: moment });
  };

  renderSubmitEventForm() {
    return (
      <div className="card">
        <div className="card-block card-block-no-padding-bottom">
          <form onSubmit={e => this.submitEventDetails(e)}>
            <div className="form-group col-sm-4">
              <label className="add-event-label">
                Daily Text Time
              </label>
              <Datetime
                dateFormat={false}
                onChange={this.handleDatetimeChange}
                defaultValue={this.state.inputDateTime.format(TEXT_TIME_FORMAT)}
              />
            </div>
            {this.renderSupplementsSelect()}
            {this.renderInputRow("Quantity", "supplementQuantity")}
            {this.renderInputRow(
              "Phone Number To Text +countryPhoneNumber aka +16171234567",
              "phoneNumber",
              this.state.phoneNumber
            )}
            <div className="float-right">
              <button
                type="submit"
                id="event-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.submitEventDetails(e)}
              >
                <i className="fa fa-dot-circle-o" /> Log Text Reminder
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  componentDidMount() {
    this.getPossibleSupplements();
  }

  getPossibleSupplements() {
    const url = "/api/v1/supplements";
    getFetchJSONAPI(url).then(responseData => {
      this.setState({ supplements: responseData });
    });
  }

  render() {
    if (!this.state.supplements) {
      return <CubeLoadingStyle />;
    }

    return (
      <div className="card">
        {this.renderSubmitEventForm()}
      </div>
    );
  }
}
