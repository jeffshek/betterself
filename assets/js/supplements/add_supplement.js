import { Link } from "react-router-dom";
import React, { Component } from "react";
import {
  JSON_AUTHORIZATION_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/requests";

export class AddSupplementView extends Component {
  constructor() {
    super();
    this.state = { ready: false };
  }

  componentDidMount() {
    this.getPossibleSupplements();
  }

  createSupplement = supplementName => {
    let params = {
      name: supplementName
    };

    return fetch("/api/v1/supplements/", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(params)
    })
      .then(response => {
        return response.json();
      })
      .then(function(responseData) {
        window.location.reload();
      });
  };

  addSupplementFormData = e => {
    e.preventDefault();
    this.createSupplement(this.supplementName.value);
  };

  getPossibleSupplements() {
    fetch("/api/v1/measurements/", {
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
