import React, { Component } from "react";
import { getFetchJSONAPI } from "../utils/fetch_utils";
import { MEASUREMENTS_RESOURCE_URL } from "../constants/api_urls";
import { CreateSupplement } from "./constants";

export class AddSupplementView extends Component {
  constructor() {
    super();
    this.state = { ready: false };
  }

  componentDidMount() {
    this.getPossibleMeasurements();
  }

  addSupplementFormData = e => {
    e.preventDefault();
    CreateSupplement(this.supplementName.value);
  };

  getPossibleMeasurements() {
    getFetchJSONAPI(MEASUREMENTS_RESOURCE_URL).then(responseData => {
      this.setState({ measurements: responseData });
      this.setState({ ready: true });
    });
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <strong>Create Supplement</strong> (Per Serving)
        </div>
        <div className="card-block">
          <form onSubmit={e => this.addSupplementFormData(e)}>
            <div className="row">
              <div className="form-group col-sm-4">
                <label><strong>Supplement Name</strong></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Black Tea"
                  ref={input => this.supplementName = input}
                />
              </div>
            </div>
            <span className="float-right">
              <button
                type="submit"
                id="add-new-object-button"
                className="btn btn-sm btn-success"
                onClick={e => this.addSupplementFormData(e)}
              >
                <i className="fa fa-dot-circle-o" /> Add Supplement
              </button>
            </span>
          </form>
        </div>
      </div>
    );
  }
}
