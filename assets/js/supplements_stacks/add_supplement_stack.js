import React, { Component } from "react";
import { postFetchJSONAPI } from "../utils/fetch_utils";
import { SUPPLEMENT_STACKS_RESOURCE_URL } from "../constants/urls";

const CreateSupplementStackButton = () => {
  return (
    <div className="card-header">
      <strong id="add-supplement-entry-text">Create Supplement Stack</strong>
    </div>
  );
};

export class AddSupplementStack extends Component {
  submitSupplementStackEvent = e => {
    e.preventDefault();

    // api parameters used to send
    const stackName = this.stackName.value;
    const postParams = {
      name: stackName
    };

    postFetchJSONAPI(
      SUPPLEMENT_STACKS_RESOURCE_URL,
      postParams
    ).then(responseData => {
      window.location.reload();
      return responseData;
    });
  };

  renderAddSupplementStackForm() {
    return (
      <div className="card-block card-block-no-padding-bottom">
        <form onSubmit={e => this.submitSupplementStackEvent(e)}>
          <div className="row">
            <div className="col-sm-12">
              <div className="form-group">
                <label className="add-event-label">Stack Name</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Morning Stack"
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
              onClick={e => this.submitSupplementStackEvent(e)}
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
        <CreateSupplementStackButton />
        {this.renderAddSupplementStackForm()}
      </div>
    );
  }
}
