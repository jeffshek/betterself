import React, { Component } from "react";
import { JSON_HEADERS } from "../constants/requests";
import { DASHBOARD_INDEX_URL } from "../constants/urls";
import { Redirect } from "react-router-dom";
import moment from "moment";

export class SignupView extends Component {
  constructor() {
    super();

    this.state = {
      username: "",
      password: "",
      password_confirm: ""
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    if (this.state.password !== this.state.password_confirm) {
      alert("Passwords does not match confirm password. Please try again.");
    } else {
      const postParams = {
        username: this.state.username,
        password: this.state.password,
        timezone: moment.tz.guess()
      };

      fetch("api/v1/user-signup/", {
        method: "POST",
        headers: JSON_HEADERS,
        body: JSON.stringify(postParams)
      })
        .then(response => {
          if (response.status === 400) {
            response.json().then(responseData => {
              if ("username" in responseData) {
                alert("Username : " + responseData["username"]);
              } else if ("password" in responseData) {
                alert("Password : " + responseData["password"]);
              }
            });
            // Don't return anything if its not working
            return;
          }
          return response.json();
        })
        .then(responseData => {
          if ("token" in responseData) {
            // If the token is in the response, set the storage
            // and then redirect to the dashboard
            localStorage.token = responseData["token"];
            localStorage.userName = responseData["username"];
            window.location.assign(DASHBOARD_INDEX_URL);
          }
        });
    }
  }

  handleChange(event) {
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  render() {
    return (
      <div>
        <div className="row approve-modal">
          <br />
          <div className="col-md-6 offset-sm-1">
            <br /><br /><br />
            <div className="card">
              <div className="card-header">
                <h3><strong>Sign Up</strong></h3>
              </div>
              <div className="card-block">
                <form method="post" className="form-horizontal ">
                  <div className="form-group row">
                    <label className="col-md-3 form-control-label">
                      Username
                    </label>
                    <div className="col-md-9">
                      <input
                        name="username"
                        className="form-control"
                        value={this.state.username}
                        onChange={this.handleChange}
                        placeholder="Create Username ..."
                      />
                      <span className="help-block">
                        {" "}Between 4-32 Characters
                      </span>
                    </div>
                  </div>
                  <div className="form-group row">
                    <label className="col-md-3 form-control-label">
                      Password
                    </label>
                    <div className="col-md-9">
                      <input
                        name="password"
                        type="password"
                        className="form-control"
                        value={this.state.password}
                        onChange={this.handleChange}
                        placeholder="Enter Password ..."
                      />
                      <span className="help-block">
                        {" "}Minimum of 8 Characters
                      </span>
                    </div>
                  </div>
                  <div className="form-group row">
                    <label className="col-md-3 form-control-label" />
                    <div className="col-md-9">
                      <input
                        name="password_confirm"
                        type="password"
                        className="form-control"
                        value={this.state.password_confirm}
                        onChange={this.handleChange}
                        placeholder="Confirm Password.."
                      />
                    </div>
                  </div>
                </form>
              </div>
              <div className="card-footer">
                <button
                  type="submit"
                  className="btn btn-sm btn-success float-right"
                  id="create-username"
                  onClick={this.handleSubmit}
                >
                  <i className="fa fa-dot-circle-o" /> Submit
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
