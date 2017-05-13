import React, { PropTypes, Component } from "react";
import { LOGO_BACKGROUND_PATH } from "../fragments/image_paths";
import { HOME_URL } from "../urls/constants";
import { Link } from "react-router-dom";
import CSSModules from 'react-css-modules';
import styles from './css/external_header.css'

const MenuItem = props => (
  <li className="nav-item" key={props.key}>
    <Link to={HOME_URL}>{props.name}</Link>
  </li>
);

class LoggedOutHeader extends Component {
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
      <header id="header-1" styleName="the-header" className="soft-scroll">
        <nav className="main-nav navbar-fixed-top headroom headroom--pinned">
          <div className="container">
            <div className="navbar-header">
              <a href={HOME_URL}>
              <img
                src={LOGO_BACKGROUND_PATH}
                className="brand-img img-responsive"
              />
              </a>
            </div>
            {/*Menu Dropdown Items*/}
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

export default CSSModules(LoggedOutHeader, styles)
