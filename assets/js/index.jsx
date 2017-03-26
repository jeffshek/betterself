var React = require('react')
var ReactDOM = require('react-dom')
var Dashboard = require('./dashboard')
var Login = require('./auth/login')
var auth = require('./auth/auth')
var Router = require('react-router-dom').HashRouter
var Route = require('react-router-dom').Route
var browserHistory = require('react-router-dom').browserHistory

function requireAuth(nextState, replace) {
    if (!auth.loggedIn()) {
        replace({
            pathname:'/dashboard/login/',
            state: {nextPathname: '/dashboard/'}
        })
    }
}

ReactDOM.render(
    <Router history={browserHistory}>
        <div>
          <Route exact path="/" component={Login} />
          <Route path='/dashboard/login' component={Login} />
          <Route path='/dashboard/' component={Dashboard} onEnter={requireAuth} />
        </div>
    </Router>,
    document.getElementById('dashboard')
)
