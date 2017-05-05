import React, { PropTypes, Component } from "react";
import CSSModules from 'react-css-modules';
import styles from './css/sidebar.css'


class Sidebar extends Component {
  render() {
    return (
      <div styleName="sidebar-background">
        <div id="sidebar-menu" className="main_menu_side hidden-print main_menu">
          <div className="menu_section">
            <h3>General</h3>
            <ul className="nav side-menu">
              <li>
                <a>
                  <i className="fa fa-home" />
                  {" "}
                  Home
                  {" "}
                  <span className="fa fa-chevron-down" />
                </a>
                <ul className="nav child_menu">
                  <li><a href="index.html">Dashboard</a></li>
                  <li><a href="index2.html">Dashboard2</a></li>
                  <li><a href="index3.html">Dashboard3</a></li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </div>
    );
  }
}
export default CSSModules(Sidebar, styles);
