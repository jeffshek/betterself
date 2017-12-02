import React, { Component } from "react";
import { JSON_HEADERS } from "../constants/requests";
import { DASHBOARD_DAILY_OVERVIEW_ANALYTICS_URL } from "../constants/urls";
import moment from "moment-timezone";
import { USER_SIGNUP_URL } from "../constants/api_urls";

export class SignupView extends Component {
  constructor() {
    super();

    this.state = {
      username: "",
      password: "",
      email: ""
    };

    // Instead of using router props (which is the right way), this is a quick
    // and dirty way of picking out a way to create custom supplements for users
    const current_url = window.location.href;
    if (current_url.includes("create_supplements=")) {
      // get all the text after the phrase create_supplements
      this.state.supplements = current_url.split("create_supplements=")[1];
    }
  }

  handleSubmit = event => {
    event.preventDefault();

    let postParams = {
      username: this.state.username,
      password: this.state.password,
      timezone: moment.tz.guess(),
      supplements: this.state.supplements
    };

    if (this.state.email) {
      postParams["email"] = this.state.email;
    }

    fetch(USER_SIGNUP_URL, {
      method: "POST",
      headers: JSON_HEADERS,
      body: JSON.stringify(postParams)
    })
      .then(response => {
        // 400 responses
        if (response.status === 400) {
          response.json().then(responseData => {
            if ("username" in responseData) {
              alert("Username : " + responseData["username"]);
            } else if ("password" in responseData) {
              alert("Password : " + responseData["password"]);
            } else if ("email" in responseData) {
              alert("Email : " + responseData["email"]);
            }
          });
          // Don't return anything if its not working
          return {};
        }

        if (response.status === 429) {
          alert(
            "Too many users have been created from this IP in the last 24 hours."
          );
          // Don't return anything if its not working
          return {};
        }

        return response.json();
      })
      .then(responseData => {
        if ("token" in responseData) {
          // If the token is in the response, set the storage
          // and then redirect to the dashboard
          localStorage.token = responseData["token"];
          localStorage.userName = responseData["username"];
          window.location.assign(DASHBOARD_DAILY_OVERVIEW_ANALYTICS_URL);
        }
      });
  };

  handleChange = event => {
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  };

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
                        placeholder="Create Username (Think of something AWESOME) ..."
                      />
                      <span className="help-block">
                        {" "}
                        Between 4-32 Characters. You can make it whatever you want. Just not "JustinBieber". That's taken.
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
                        placeholder="Enter Password (Something SECURE and not 12345678) ..."
                      />
                      <span className="help-block">
                        {" "}
                        Minimum of eight characters. Think of it as protection from noisy neighbors. If you have more than eight noisy neighbors, you should probably move.
                      </span>
                    </div>
                  </div>
                  <div className="form-group row">
                    <label className="col-md-3 form-control-label">
                      Email (Optional)
                    </label>
                    <div className="col-md-9">
                      <input
                        name="email"
                        type="email"
                        className="form-control"
                        value={this.state.email}
                        onChange={this.handleChange}
                        placeholder="Enter Email (Optional) ..."
                      />
                      <span className="help-block">
                        {" "}
                        Used for password resets. It's oddly our most requested feature. Says a lot about self-improvement.
                      </span>
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
                </button>
                &nbsp;
              </div>
            </div>
          </div>
        </div>
        <div id="special-signup-footer" />
      </div>
    );
  }
}
