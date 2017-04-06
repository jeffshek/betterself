import React, { PropTypes, Component } from 'react'
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from 'react-router-dom'

import { DASHBOARD_OVERVIEW, DASHBOARD_INDEX, LOGIN_PATH } from './urls/constants'
import { Authenticator, AuthButton } from './auth/auth'
import Login from './auth/login'

const Public = () => <h3>Public</h3>
const Protected = () => <h3>Protected</h3>

const logo_background = require('../../betterself/static/images/logos/logojoy/png/white_logo_transparent_background.png')

const Header = React.createClass({
  render: function() {
    return (
      <header id="header-1" className="soft-scroll header-1">
        <nav className="main-nav navbar-fixed-top headroom headroom--pinned">
          <div className="container">
            <div className="navbar-header">
              <button type="button" className="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span className="sr-only">Toggle navigation</span>
              </button>
              <a href="#">
                <img src={logo_background} className="brand-img img-responsive" />
              </a>
            </div>
            <div className="collapse navbar-collapse">
              <ul className="nav navbar-nav navbar-right">
                <li className="active nav-item">
                  <a href="#">Home</a>
                </li>
                <li className="nav-item">
                  <a href="#">Features</a>
                </li>
                <li className="nav-item">
                </li>
                <li className="nav-item dropdown">
                  <a className="dropdown-toggle" data-toggle="dropdown" data-hover="dropdown" data-delay={0} data-close-others="false" href="#">Pages <i className="fa fa-angle-down" /></a>
                  <ul className="dropdown-menu">
                    <li>
                      <a href="#">Dropdown 1</a>
                    </li>
                    <li>
                      <a href="#">Dropdown 2</a>
                    </li>
                    <li>
                      <a href="#">Dropdown 3</a>
                    </li>
                    <li>
                      <a href="#">Dropdown 4</a>
                    </li>
                  </ul>
                </li>
                <li className="nav-item">
                  <a href="#">Contact</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
      </header>
    );
  }
});

const DashboardRouter = () => (
  <Router>
    <div>
      <Header />
      <AuthButton/>
      <ul>
        <li><Link to={DASHBOARD_OVERVIEW}>Overview Page</Link></li>
        <li><Link to={DASHBOARD_INDEX}>Dashboard Index</Link></li>
      </ul>
      <Route path={DASHBOARD_OVERVIEW} component={Public}/>
      <Route path={LOGIN_PATH} component={Login}/>
      {/*Goal is to eventually wrap all Routes that should be protected under a component*/}
      <PrivateRoute path={DASHBOARD_INDEX} component={Protected}/>
    </div>
  </Router>
)

const PrivateRoute = ({ component, ...rest }) => (
  <Route {...rest} render={props => (
    Authenticator.isAuthenticated ? (
      React.createElement(component, props)
    ) : (
      <Redirect to={{
        pathname: LOGIN_PATH,
        state: { from: props.location }
      }}/>
    )
  )}/>
)

ReactDOM.render(
  <DashboardRouter />, document.getElementById('dashboard')
)
