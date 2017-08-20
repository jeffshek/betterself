import React, { Component } from "react";
import { JSON_POST_AUTHORIZATION_HEADERS } from "../constants/requests";
import { Authenticator } from "../authentication/auth";
import { Nav, NavItem, NavLink } from "reactstrap";
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from "reactstrap";

export class UserSettingsView extends Component {
  constructor() {
    super();

    this.state = {
      userTimeZoneModal: false
    };
  }

  toggle = () => {
    this.setState({
      userTimeZoneModal: !this.state.userTimeZoneModal
    });
  };

  confirmDelete = () => {
    const userConfirmedDelete = confirm(
      "Are you sure you want to delete? This user's info will be permanently deleted!"
    );
    if (userConfirmedDelete) {
      this.deleteUser();
    }
  };

  deleteUser = cb => {
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
  };

  renderTimeZoneSelectionModal() {
    if (this.state.userTimeZoneModal) {
      return (
        <Modal isOpen={this.state.userTimeZoneModal} toggle={this.toggle}>
          <ModalHeader toggle={this.toggle}>
            Change Timezone Preference
          </ModalHeader>
          <ModalFooter>
            <Button color="primary" onClick={this.submitUpdate}>
              Save
            </Button>
            <Button color="decline-modal" onClick={this.toggle}>Cancel</Button>
          </ModalFooter>
        </Modal>
      );
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
                    className="btn btn-outline btn-lg active"
                    onClick={this.toggle}
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
        {this.renderTimeZoneSelectionModal()}
      </div>
    );
  }
}
