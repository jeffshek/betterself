import React, { Component } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";

const CreateSupplementsStackButton = () => {
  return (
    <div className="card-header">
      <strong id="add-supplement-entry-text">Create Supplement Stack</strong>
    </div>
  );
};

export class AddSupplementsStack extends Component {
  constructor(props) {
    super(props);
  }

  submitSupplementsStackEvent = e => {
    e.preventDefault();

    // api parameters used to send
    const stackName = this.stackName.value;
    const postParams = {
      name: stackName
    };

    fetch("/api/v1/supplements_stacks/", {
      method: "POST",
      headers: JSON_POST_AUTHORIZATION_HEADERS,
      body: JSON.stringify(postParams)
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {});
  };

  renderSubmitSupplementForm() {
    return (
      <div className="card-block card-block-no-padding-bottom">
        <form onSubmit={e => this.submitSupplementsStackEvent(e)}>
          <div className="row">
            <div className="col-sm-12">
              <div className="form-group">
                <label className="add-event-label">Stack Name</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Black Tea"
                  ref={input => this.stackName = input}
                />
              </div>
            </div>
          </div>
          <div className="float-right">
            <button
              type="submit"
              id="event-dashboard-submit"
              className="btn btn-sm btn-success"
              onClick={e => this.submitSupplementsStackEvent(e)}
            >
              <i className="fa fa-dot-circle-o" /> Create Supplement Stack
            </button>
          </div>
        </form>
      </div>
    );
  }

  render() {
    return (
      <div className="card">
        <CreateSupplementsStackButton />
        {this.renderSubmitSupplementForm()}
      </div>
    );
  }
}
