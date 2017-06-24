import React, { Component } from "react";
import { Dropdown, DropdownItem, DropdownMenu } from "reactstrap";
import { Link, Redirect } from "react-router-dom";
import { LOGOUT_URL, SETTINGS_URL } from "../constants/urls";

const AVATAR_IMG = require("../../img/icons/small_brain.svg");

class LoggedInHeader extends Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      dropdownOpen: false,
      userName: localStorage.userName
    };

    // If the data wasn't available, do this so there isn't an ugly undefined in the top right
    if (
      localStorage.userName === "undefined" ||
      typeof localStorage.userName === "undefined"
    ) {
      this.state.userName = "";
    }
  }

  toggle(e) {
    this.setState({
      dropdownOpen: !this.state.dropdownOpen
    });
  }

  componentDidMount() {
    if (window.location.href.includes("signup")) {
      document.body.classList.toggle("sidebar-hidden");
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
                  <Link to={SETTINGS_URL}>Settings</Link>
                </DropdownItem>

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
