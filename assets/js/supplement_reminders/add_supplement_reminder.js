import React, { Component } from "react";
import { getFetchJSONAPI } from "../utils/fetch_utils";
import { CubeLoadingStyle } from "../constants/loading_styles";
import moment from "moment";
import Datetime from "react-datetime";
import { TEXT_TIME_FORMAT } from "../constants/dates_and_times";

export class AddSupplementReminderView extends Component {
  constructor() {
    super();
    this.state = {
      supplements: null,
      inputDateTime: moment(),
      phoneNumber: "+16171234567",
      supplementQuantity: 1
    };
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

    const postParams = {
      supplement_uuid: supplementUUIDSelected,
      quantity: this.state.supplementQuantity,
      remind_time: utcTimeString,
      source: "web",
      phoneNumber: this.state.phoneNumber
    };

    console.log(postParams);

    // fetch("api/v1/user_activity_events/", {
    //   method: "POST",
    //   headers: JSON_POST_AUTHORIZATION_HEADERS,
    //   body: JSON.stringify(postParams)
    // })
    //   .then(response => {
    //     return response.json();
    //   })
    //   .then(responseData => {
    //     this.props.addEventEntry(responseData);
    //     return responseData;
    //   })
    //   .catch(error => {
    //     alert("Invalid Error Occurred When Submitting Data " + error);
    //   });
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
              "Phone Number To Text +countryCodePhoneNumber aka +16171234567",
              "phoneNumber",
              "+16171234567"
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
