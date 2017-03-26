var React = require('react')
var ReactDOM = require('react-dom')
var Router = require('react-router')
var Dashboard = require('./dashboard')
var Login = require('./auth/login')
var auth = require('./auth/auth')

function requireAuth(nextState, replace) {
    if (!auth.loggedIn()) {
        replace({
            pathname:'/dashboard/login/',
            state: {nextPathname: '/dashboard/'}
        })
    }
}

ReactDOM.render(
    <Router.Router history={Router.browserHistory}>
        <Router.Route path='/dashboard/login' component={Login} />
        <Router.Route path='/dashboard/' component={Dashboard} onEnter={requireAuth} />
    </Router.Router>,
    document.getElementById('dashboard')
)
