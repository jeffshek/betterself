// import React from "react"
// import { render } from "react-dom"
// import { BrowserRouter as Router } from 'react-router-dom'
//
// var auth = require('./auth/auth')
// var Login = require('./auth/login')


// class Dashboard extends React.Component {
//
//   fetchUserData () {
//     return 'Fetching User Data';
//   }
//
//   render() {
//     return (
//       <h1>
//         { this.fetchUserData() }
//       </h1>
//     )
//   }
// }
//
// render(<Dashboard />, document.getElementById('container'))

var React = require('react')
var ReactDOM = require('react-dom')
var Router = require('react-router')
var App = require('./app')
var Login = require('./auth/login')
var auth = require('./auth/auth')

function requireAuth(nextState, replace) {
  if (!auth.loggedIn()) {
    replace({
      pathname:'/app/login/',
      state: {nextPathname: '/app/'}
    })
  }
}

ReactDOM.render(
  <Router.Router history={Router.browserHistory}>
    <Router.Route path='/app/login/' component={Login} />
    <Router.Route path='/app/' component={App} onEnter={requireAuth} />
  </Router.Router>,
  document.getElementById('app')
)
