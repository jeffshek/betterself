import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import { DASHBOARD_INDEX_URL } from "../constants/urls";
import LaddaButton, { EXPAND_LEFT } from "react-ladda";

const ShowLoading = () => {
  return (
    <LaddaButton
      className="btn btn-sm btn-success btn-ladda float-right"
      loading={true}
      data-color="green"
      data-style={EXPAND_LEFT}
    >
      Creating Demo User History
    </LaddaButton>
  );
};

export class CreateDemoUserView extends Component {
  constructor() {
    super();
    this.state = {
      onClickDisabled: false,
      demoToken: null,
      demoUserName: null
    };
  }

  componentDidMount() {
    // Upon getting to this page, create a demo user in the background, so it doesn't take forever to load
    this.createDemoUser();
  }

  createDemoUser() {
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
          this.setState({
            demoToken: responseData["token"],
            demoUserName: responseData["username"]
          });
        }
        return responseData;
      });
  }

  handleSubmit = event => {
    event.preventDefault();
    this.setState({
      onClickDisabled: true
    });

    localStorage.token = this.state.demoToken;
    localStorage.userName = this.state.demoUserName;
    window.location.assign(DASHBOARD_INDEX_URL);
  };

  renderSubmitButton() {
    if (this.state.onClickDisabled) {
      return <ShowLoading />;
    } else
      return (
        <button
          type="submit"
          className="btn btn-sm btn-success float-right"
          id="create-username"
          onClick={this.handleSubmit}
          disabled={this.state.onClickDisabled}
        >
          <i className="fa fa-dot-circle-o" />
          {" "}Create Demo User
        </button>
      );
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
                <h3><strong>&nbsp;Create Demo User</strong></h3>
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
                {this.renderSubmitButton()}
              </div>
            </div>
          </div>
        </div>
        <div id="special-signup-footer" />
      </div>
    );
  }
}
