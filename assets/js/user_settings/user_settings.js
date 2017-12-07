import React, { Component } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";
import { Authenticator } from "../authentication/auth";
import { USER_INFO_URL } from "../constants/urls";

export class UserSettingsView extends Component {
  constructor() {
    super();
  }

  confirmDelete = () => {
    const userConfirmedDelete = confirm(
      "Are you sure you want to delete? This user's info will be permanently deleted!"
    );
    if (userConfirmedDelete) {
      this.deleteUser();
    }
  };

  deleteUser = cb => {
    fetch(USER_INFO_URL, {
      method: "DELETE",
      headers: JSON_POST_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        Authenticator.logout(cb);
      });
  };

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
                  <a href="/users/~update/">
                    <button
                      type="button"
                      className="btn btn-outline btn-lg active"
                    >
                      Change Time Zone
                    </button>
                  </a>
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
