import React, { PropTypes, Component } from "react";
import { logo_background } from "./image_paths";
import { HOME_URL } from "../urls/constants";
import { Link } from "react-router-dom";

const MenuItem = props => (
  <li className="nav-item" key={props.key}>
    <Link to={HOME_URL}>{props.name}</Link>
  </li>
);

export default class Header extends Component {
  menuItems = [
    { name: "Home", key: "Home" },
    { name: "Dashboard", key: "Dashboard" },
    { name: "Features", key: "Features" },
    { name: "About", key: "About" },
    { name: "Contact", key: "Contact" },
    { name: "Settings", key: "Settings" }
  ];

  render() {
    return (
      <header id="header-1" className="soft-scroll header-1">
        <nav className="main-nav navbar-fixed-top headroom headroom--pinned">
          <div className="container">
            <div className="navbar-header">
              {/* TODO - Figure out how to use Routers to return href*/}
              <Link to={HOME_URL}>
                <img
                  src={logo_background}
                  className="brand-img img-responsive"
                />
              </Link>
            </div>
            <div className="collapse navbar-collapse">
              <ul className="nav navbar-nav navbar-right">
                {this.menuItems.map(MenuItem)}
              </ul>
            </div>
          </div>
        </nav>
      </header>
    );
  }
}
