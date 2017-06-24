import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import { DASHBOARD_INDEX_URL } from "../constants/urls";

export class CreateDemoUserView extends Component {
  constructor() {
    super();
    this.handleSubmit = this.handleSubmit.bind(this);
    this.state = {
      onClickDisabled: false,
      createDemoUserText: "Create Demo User",
      createDemoUserState: "CREATE DEMO USER"
    };
  }

  handleSubmit(event) {
    event.preventDefault();
    this.setState({
      onClickDisabled: true,
      createDemoUserState: "CREATING DEMO USER ... PLEASE WAIT"
    });

    return fetch("/api/v1/user-signup-demo/", {
      method: "GET"
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        if ("token" in responseData) {
          // If the token is in the response, set localStorage correctly
          // and then redirect to the dashboard
          localStorage.token = responseData["token"];
          localStorage.userName = responseData["username"];
          localStorage.timezone = responseData["timezone"];

          window.location.assign(DASHBOARD_INDEX_URL);
        }
        return responseData;
      });
  }

  render() {
    return (
      <div>
        <div className="row approve-modal">
          <br /><br /><br />
          <div className="col-md-6 offset-sm-3">
            <br /><br /><br />
            <div className="card">
              <div className="card-header">
                <br />
                <h3><strong>&nbsp;{this.state.createDemoUserText}</strong></h3>
              </div>
              <div className="card-block">
                <form method="post" className="form-horizontal ">
                  <div className="col-md-11 form-group row">
                    <label className="form-control-label">
                      Hitting CREATE generates a demo user with randomly generated data to illustrate analytics.
                      {" "}
                      <br />
                      {" "}
                      <p>
                        {" "}
                        Demo users are temporary and will be deleted by the end of day.
                        {" "}
                      </p>
                    </label>
                  </div>
                </form>
              </div>
              <div className="card-footer">
                <button
                  type="submit"
                  className="btn btn-sm btn-success float-right"
                  id="create-username"
                  onClick={this.handleSubmit}
                  disabled={this.state.onClickDisabled}
                >
                  <i className="fa fa-dot-circle-o" />
                  {" "}
                  {this.state.createDemoUserState}
                </button>&nbsp;
              </div>
            </div>
          </div>
        </div>
        <div id="special-signup-footer" />
      </div>
    );
  }
}
