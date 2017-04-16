import React, { PropTypes, Component } from 'react'
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from 'react-router-dom'

import { DASHBOARD_OVERVIEW_URL, DASHBOARD_INDEX_URL, LOGIN_URL, HOME_URL, SETTINGS_URL } from './urls/constants'
import { Authenticator } from './authentication/auth'
import LoggedOutView from './authentication/login'
import Header from './fragments/header'
import Footer from './fragments/footer'
import { HomePage } from './home/home'

const Protected = () => <h3>Protected</h3>

const BetterSelfRouter = () => (
  <Router>
    <div>
      <Header />

      {/*Public Routes*/}
      <Route exact path={HOME_URL} component={HomePage}/>
      <Route path={DASHBOARD_OVERVIEW_URL} component={LoggedOutView}/>
      <Route path={LOGIN_URL} component={LoggedOutView}/>
      <Route path={SETTINGS_URL} component={LoggedOutView}/>
      {/*Private Routes*/}
      <PrivateRoute path={DASHBOARD_INDEX_URL} component={Protected}/>

      <Footer />
    </div>
  </Router>
)

const PrivateRoute = ({ component, ...rest }) => (
  <Route {...rest} render={props => (
    Authenticator.isAuthenticated ? (
      React.createElement(component, props)
    ) : (
      <Redirect to={{
        pathname: LOGIN_URL,
        state: { from: props.location }
      }}/>
    )
  )}/>
)

ReactDOM.render(
  <BetterSelfRouter />, document.getElementById('root')
)
