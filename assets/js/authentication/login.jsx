import React from 'react'
import { Authenticator } from './auth'
import { DASHBOARD_OVERVIEW } from '../urls/constants'
import { Redirect } from 'react-router-dom'

export default class Login extends React.Component {
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
