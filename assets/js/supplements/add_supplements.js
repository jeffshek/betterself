import React, { PropTypes, Component } from "react";
import { JSON_AUTHORIZATION_HEADERS } from "../constants/util_constants";

export class AddSupplementView extends Component {
  constructor() {
    super();
    this.state = { ready: false };
    this.submitSupplementEvent = this.submitSupplementEvent.bind(this);
  }

  componentDidMount() {
    this.getPossibleSupplements();
  }

  submitSupplementEvent(e) {
    e.preventDefault();
    console.log(this.supplementName.value);
    console.log(this.vendorName.value);
  }

  getPossibleSupplements() {
    fetch("/api/v1/measurements", {
      method: "GET",
      headers: JSON_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        this.setState({ measurements: responseData });
        this.setState({ ready: true });
      });
  }

  renderMeasurements() {
    const measurementKeys = Object.keys(this.state.measurements);

    return (
      <div className="form-group col-sm-4">
        <label><strong>Measurement</strong></label>
        <select
          className="form-control"
          ref={input => this.supplementNameKey = input}
        >
          {measurementKeys.map(key => (
            <option value={key} key={key}>
              {this.state.measurements[key].name}
            </option>
          ))}
        </select>

        <select
          className="form-control"
          ref={input => this.supplementNameKey = input}
        >
          {measurementKeys.map(key => (
            <option value={key} key={key}>
              {this.state.measurements[key].name}
            </option>
          ))}
        </select>
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        <div className="card-header">
          <strong>Create Supplement</strong> (Per Serving)
        </div>
        <div className="card-block">
          <form onSubmit={e => this.submitSupplementEvent(e)}>
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

            <div className="row">
              <div className="form-group col-sm-4">
                <label><strong>Vendor</strong></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Lipton"
                  ref={input => this.vendorName = input}
                />
              </div>
            </div>

            <div className="row">
              <div className="form-group col-sm-4">
                <label><strong>Ingredients</strong><sup>1</sup></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Caffeine"
                  ref={input => this.vendorName = input}
                />
                <input
                  type="text"
                  className="form-control"
                  placeholder="Theanine"
                  ref={input => this.vendorName = input}
                />
              </div>
              <div className="form-group col-sm-4">
                <label><strong>Quantity</strong><sup>2</sup></label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="50"
                  ref={input => this.vendorName = input}
                />

                <input
                  type="text"
                  className="form-control"
                  placeholder="75"
                  ref={input => this.vendorName = input}
                />
              </div>

              {this.state.ready ? this.renderMeasurements() : ""}

            </div>
            <div className="float-right">
              <button
                type="submit"
                id="supplement-dashboard-submit"
                className="btn btn-sm btn-success"
                onClick={e => this.submitSupplementEvent(e)}
              >
                <i className="fa fa-dot-circle-o" /> Add Supplement
              </button>
            </div>
          </form>
          <div>
            <sup>1) Ingredients are optional inputs. </sup>
            <sup>2) Per unit of measurement.</sup>
          </div>
        </div>
      </div>
    );
  }
}
