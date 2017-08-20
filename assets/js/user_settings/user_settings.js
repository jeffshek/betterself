import React, { Component, PropTypes } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";
import { Authenticator } from "../authentication/auth";

export class UserSettingsView extends Component {
  constructor() {
    super();
    this.deleteUser = this.deleteUser.bind(this);
    this.confirmDelete = this.confirmDelete.bind(this);
  }

  confirmDelete() {
    const userConfirmedDelete = confirm(
      "Are you sure you want to delete? This user's info will be permanently deleted!"
    );
    if (userConfirmedDelete) {
      this.deleteUser();
    }
  }

  deleteUser(cb) {
    fetch("/api/v1/user-info/", {
      method: "DELETE",
      headers: JSON_POST_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        Authenticator.logout(cb);
      });
  }

  render() {
    return (
      <div>
        <div className="row approve-modal">
          <br />
          <div className="col-md-6 offset-sm-0">
            <br /><br /><br />
            <div className="card">
              <div className="card-header">
                <br />
                <h3><strong>&nbsp;User Settings</strong></h3>
              </div>
              <div className="animated fadeIn">
                <div className="card-block">
                  <button
                    type="button"
                    className="btn btn-outline btn-lg active"
                    onClick={this.confirmDelete}
                  >
                    Change Time Zone
                  </button>
                  &nbsp;&nbsp;
                  <button
                    type="button"
                    className="btn btn-outline-danger btn-lg active"
                    onClick={this.confirmDelete}
                  >
                    Delete My Account
                  </button>&nbsp;
                </div>
              </div>
            </div>
          </div>
        </div>
        <div id="special-signup-footer" />
      </div>
    );
  }
}
