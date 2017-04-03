import React, { PropTypes } from 'react'
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from 'react-router-dom'

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
  isAuthenticated: !!localStorage.token,

  login(username, password, cb) {
    if (localStorage.token) {
      this.isAuthenticated = true
      return
    }

    this.getToken(username, password, (res) => {
      if (res.authenticated) {
        this.isAuthenticated = true

        localStorage.token = res.token
        if (cb) cb(true)
      } else {
        if (cb) cb(false)
      }
    })
  },

  logout(cb) {
    delete localStorage.token
    this.isAuthenticated = false
    setTimeout(cb, 100)
  },

  getToken(username, pass, cb) {
    $.ajax({
      type: 'POST',
      url: '/api-token-auth/',
      data: {
        username: username,
        password: pass
      },
      success: function(res){
        cb({
          authenticated: true,
          token: res.token
        })
      }
    })
  },

}

const AuthButton = withRouter(({ history }) => (
  Authenticator.isAuthenticated
    ? (
      <p>
        Welcome User!
        <button onClick={() => {
          Authenticator.logout(() => history.push('/'))}
        }>
          Log out
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

  handleSubmit = (e) => {
    e.preventDefault()

    let username = this.refs.username.value
    let password = this.refs.password.value

    Authenticator.login(username, password, (loggedIn) => {
      if (loggedIn) {
        this.setState({ redirectToReferrer: true })
      }
    })
  }

  render() {
    const { from } = this.props.location.state || { from: { pathname: '/' } }
    const { redirectToReferrer } = this.state

    if (Authenticator.isAuthenticated) {
      return (
        <Redirect to={DASHBOARD_OVERVIEW}/>
      )
    }

    if (redirectToReferrer) {
      return (
        <Redirect to={DASHBOARD_OVERVIEW}/>
      )
    }

    return (
      <div>
        <p>You must log in to view the page at {from.pathname}</p>
        <input type="text" placeholder="username" ref="username" />
        <input type="password" placeholder="password" ref="password" />
        <button onClick={this.handleSubmit}>Log In</button>
      </div>
    )
  }
}

ReactDOM.render(
  <AuthExample />, document.getElementById('dashboard')
)
