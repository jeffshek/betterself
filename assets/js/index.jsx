var React = require('react')
var ReactDOM = require('react-dom')
var Router = require('react-router')
var App = require('./app')
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
        <Router.Route path='/login/' component={Login} />
        <Router.Route path='/react/' component={App} onEnter={requireAuth} />
    </Router.Router>,
    document.getElementById('app')
)
