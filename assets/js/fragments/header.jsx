import React, { PropTypes, Component } from 'react'
import { logo_background } from './image_paths'


const MenuItem = (props) => (
  <li className="nav-item" key={props.key}>
    <a href="#">{props.name}</a>
  </li>
)

export default class Header extends Component {
  menuItems = [
    {name:"Home", key:"Home"},
    {name:"Dashboard", key:"Dashboard"},
    {name:"Features", key:"Features"},
    {name:"About", key:"About"},
    {name:"Contact", key:"Contact"},
    // Figure out how to use for login and logout
    // or make another Component for just user settings
    {name:"Settings", key:"Settings"}
  ]

  render() {
    return (
      <header id="header-1" className="soft-scroll header-1">
        <nav className="main-nav navbar-fixed-top headroom headroom--pinned">
          <div className="container">
            <div className="navbar-header">
              {/* TODO - Figure out how to use Routers to return href*/}
              <a href="#">
                <img src={logo_background} className="brand-img img-responsive" />
              </a>
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
