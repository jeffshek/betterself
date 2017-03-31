import React, { PropTypes } from 'react'
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from 'react-router-dom'

////////////////////////////////////////////////////////////
// 1. Click the public page
// 2. Click the protected page
// 3. Log in
// 4. Click the back button, note the URL each time

const DASHBOARD_OVERVIEW = '/dashboard/overview/'
const DASHBOARD_INDEX = '/dashboard/index'
const LOGIN_PATH = '/dashboard/login'

const AuthExample = () => (
  <Router>
    <div>
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

const Authenticator = {
  isAuthenticated: false,
  login(username, password, cb) {
    console.log(username, password, cb)
    if (localStorage.token) {
      if (cb) cb(true)
      return
    }

    this.isAuthenticated = true
    setTimeout(cb, 100) // fake async
  },
  logout(cb) {
    this.isAuthenticated = false
    setTimeout(cb, 100)
  }
}

const AuthButton = withRouter(({ history }) => (
  Authenticator.isAuthenticated ? (
    <p>
      Welcome!
      <button onClick={() => {
        Authenticator.logout(() => history.push('/'))}
      }>
        Sign out
      </button>
    </p>
  ) : (
    <p>You are not logged in.</p>
  )
))

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

const Public = () => <h3>Public</h3>
const Protected = () => <h3>Protected</h3>

class Login extends React.Component {
  state = {
    redirectToReferrer: false
  }

  login = () => {
    Authenticator.login(1, 2, () => {
      this.setState({ redirectToReferrer: true })
    })
  }

  render() {
    const { from } = this.props.location.state || { from: { pathname: '/' } }
    const { redirectToReferrer } = this.state

    if (redirectToReferrer) {
      return (
        <Redirect to={from}/>
      )
    }

    return (
      <div>
        <p>You must log in to view the page at {from.pathname}</p>
        <input type="text" placeholder="username" ref="username" />
        <input type="password" placeholder="password" ref="pass" />
        <button onClick={this.login}>Log in</button>
      </div>
    )
  }
}

ReactDOM.render(
  <AuthExample />, document.getElementById('dashboard')
)
