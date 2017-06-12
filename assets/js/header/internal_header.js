import React, { Component } from "react";
import { Dropdown, DropdownMenu, DropdownItem } from "reactstrap";
import { Link, Redirect } from "react-router-dom";
import { LOGOUT_URL } from "../urls/constants";
import {
  JSON_HEADERS,
  JSON_POST_AUTHORIZATION_HEADERS
} from "../constants/util_constants";

const AVATAR_IMG = require("../../img/icons/small_brain.svg");

class LoggedInHeader extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      dropdownOpen: false
    };
    if (localStorage.userName) {
      this.state.userName = localStorage.userName;
    }
  }

  toggle(e) {
    this.setState({
      dropdownOpen: !this.state.dropdownOpen
    });
  }

  updateUserName() {
    fetch("/api/v1/user-info/", {
      method: "GET",
      headers: JSON_POST_AUTHORIZATION_HEADERS
    })
      .then(response => {
        return response.json();
      })
      .then(responseData => {
        // If valid response, get the store the username
        localStorage.userName = responseData.username;
        this.setState({
          userName: responseData.username
        });
      });
  }

  componentDidMount() {
    if (window.location.href.includes("signup")) {
      document.body.classList.toggle("sidebar-hidden");
    }
    if (!localStorage.userName) {
      this.updateUserName();
    }
  }

  sidebarToggle(e) {
    e.preventDefault();
    document.body.classList.toggle("sidebar-hidden");
  }

  mobileSidebarToggle(e) {
    e.preventDefault();
    document.body.classList.toggle("sidebar-mobile-show");
  }

  render() {
    return (
      <header className="app-header navbar">
        <button
          className="navbar-toggler mobile-sidebar-toggler hidden-lg-up"
          onClick={this.mobileSidebarToggle}
          type="button"
        >
          ☰
        </button>
        <a className="navbar-brand" href="/" />
        <ul className="nav navbar-nav hidden-md-down">

          {/*Toggles the sidebar*/}
          <li className="nav-item">
            <a
              className="nav-link navbar-toggler sidebar-toggler"
              onClick={this.sidebarToggle}
              href="#"
            >
              ☰
            </a>
          </li>

        </ul>
        <ul className="nav navbar-nav ml-auto">
          <li className="nav-item">
            <Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggle}>
              <a
                onClick={this.toggle}
                className="nav-link dropdown-toggle nav-link"
                data-toggle="dropdown"
                role="button"
                aria-haspopup="true"
                aria-expanded={this.state.dropdownOpen}
              >
                <img
                  src={AVATAR_IMG}
                  className="img-avatar"
                  width="50px"
                  height="50px"
                />
                <span className="hidden-md-down username-text">
                  {this.state.userName} &nbsp;
                </span>
              </a>

              <DropdownMenu className="dropdown-menu-right">

                <DropdownItem>
                  <i className="fa fa-lock" />
                  <Link to={LOGOUT_URL}>Logout</Link>
                </DropdownItem>

              </DropdownMenu>
            </Dropdown>
          </li>
          {/*Use some minor spacing for to username logo too close, fix when CSS is improved*/}
          <div>&nbsp;&nbsp;</div>
        </ul>
      </header>
    );
  }
}

export default LoggedInHeader;
