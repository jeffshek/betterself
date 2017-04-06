import React, { PropTypes, Component } from 'react'

const header_logo_background = require('../../../betterself/static/images/logos/logojoy/png/white_logo_transparent_background.png')


const MenuItem = (props) => (
  <li className="nav-item">
    <a href="#">{props.name}</a>
  </li>
)

export default class Header extends Component {
  menuItems = [
    {name:"Home", key:"Home"},
    {name:"Dashboard", key:"Dashboard"},
    {name:"Features", key:"Features"},
    {name:"About", key:"About"},
    {name:"Contact", key:"Contact"}
  ]

  render() {
    return (
      <header id="header-1" className="soft-scroll header-1">
        <nav className="main-nav navbar-fixed-top headroom headroom--pinned">
          <div className="container">
            <div className="navbar-header">
              <button type="button" className="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span className="sr-only">Toggle navigation</span>
              </button>
              <a href="#">
                <img src={header_logo_background} className="brand-img img-responsive" />
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
