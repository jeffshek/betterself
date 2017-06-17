import React, { Component, PropTypes } from "react";
import { LOGO_BACKGROUND_PATH } from "../constants/image_paths";
import { DASHBOARD_INDEX_URL, HOME_URL } from "../constants/urls";
import { Link } from "react-router-dom";
import CSSModules from "react-css-modules";
import styles from "./css/external_header.css";

class LoggedOutHeader extends Component {
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
            <div className="collapse navbar-collapse">
              <ul className="nav navbar-nav navbar-right">
                <li className="nav-item">
                  {/*Have to do this because of conflicting CSS*/}
                  <a href={DASHBOARD_INDEX_URL}>Dashboard</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </header>
    );
  }
}

export default CSSModules(LoggedOutHeader, styles);
