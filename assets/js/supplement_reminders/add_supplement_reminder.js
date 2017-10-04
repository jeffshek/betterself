import React, { Component } from "react";
import { getFetchJSONAPI } from "../utils/fetch_utils";
import { CubeLoadingStyle } from "../constants/loading_styles";
import moment from "moment";
import Datetime from "react-datetime";
import { TEXT_TIME_FORMAT } from "../constants/dates_and_times";

export class AddSupplementReminderView extends Component {
  constructor() {
    super();
    // this.state.supplements = false;
    this.state = {
      supplements: null,
      inputDateTime: moment()
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
    // const indexSelected = this.activityTypeIndexSelected.value;
    // const userActivityUUIDSelected = this.props.userActivityTypes[indexSelected]
    //   .uuid;
    //
    // const postParams = {
    //   user_activity_uuid: userActivityUUIDSelected,
    //   duration_minutes: this.state.durationMinutes,
    //   time: this.state.inputDateTime.toISOString(),
    //   source: "web"
    // };
    //
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

  renderInputRow(label, inputName) {
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
            defaultValue={0}
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
                Text Time
              </label>
              <Datetime
                dateFormat={false}
                onChange={this.handleDatetimeChange}
                // value={this.state.inputDateTime}
                defaultValue={this.state.inputDateTime.format(TEXT_TIME_FORMAT)}
              />
            </div>
            {this.renderSupplementsSelect()}
            {this.renderInputRow("Quantity", "supplementQuantity")}
            {this.renderInputRow(
              "Phone Number To Text +countryCodePhoneNumber aka +16173334444",
              "phoneNumber"
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
      // this.setState({ loadedSupplements: true });
    });
  }

  render() {
    if (!this.state.supplements) {
      return <CubeLoadingStyle />;
    }

    const supplementsKeys = Object.keys(this.state.supplements);

    return (
      <div className="card">
        {this.renderSubmitEventForm()}
      </div>
    );
  }
}
