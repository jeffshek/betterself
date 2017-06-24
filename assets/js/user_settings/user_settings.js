import React, { PropTypes, Component } from "react";

export class UserSettingsView extends Component {
  super() {
    this();
    this.confirmDelete = this.confirmDelete.bind(this);
  }

  confirmDelete() {
    const userConfirmedDelete = confirm(
      "Are you sure you want to delete? This user's info will be permanently deleted!"
    );
    if (userConfirmedDelete) {
      console.log("Deleting!");
    }
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
