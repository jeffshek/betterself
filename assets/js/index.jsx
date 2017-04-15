import React, { PropTypes, Component } from 'react'

import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from 'react-router-dom'

import { DASHBOARD_OVERVIEW_URL, DASHBOARD_INDEX_URL, LOGIN_URL } from './urls/constants'
import { Authenticator } from './authentication/auth'

import LoggedOutView, { IsLoggedInWelcomeText } from './authentication/login'
import Header from './fragments/header'
import Footer from './fragments/footer'

const Public = () => <h3>Public</h3>
const Protected = () => <h3>Protected</h3>

import { HomePage } from './home/home'

const BetterSelfRouter = () => (
  <Router>
    <div>
      <Header />
      <HomePage />
      {/*<IsLoggedInWelcomeText/>*/}
      <Route path={DASHBOARD_OVERVIEW_URL} component={Public}/>
      <Route path={LOGIN_URL} component={LoggedOutView}/>
      {/*Goal is to eventually wrap all Routes that should be protected under a component*/}
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
