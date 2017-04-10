import React, { Component } from 'react'
import { Authenticator } from './auth'
import { DASHBOARD_OVERVIEW } from '../urls/constants'
import { Redirect, withRouter } from 'react-router-dom'
import { login_ledge_photo } from '../fragments/image_paths'

export default class Login extends Component {
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
      // This might be dumb, considering taking this out
      return (
        <Redirect to={DASHBOARD_OVERVIEW}/>
      )
    }

    return <div></div>

  }
}

// Auth Commented Out Code - Refactor Into Original
//   <div>
//     <p>You must log in to view the page at {from.pathname}</p>
//     <input type="text" placeholder="username" ref="username" />
//     <input type="password" placeholder="password" ref="password" />
//     <button onClick={this.handleSubmit}>Log In</button>
//   </div>
// )


class LoggedOutView extends Component {
  state = {
    redirectToReferrer: false
  }

  handleSubmit(event) {
    event.preventDefault()

    username = this.username.value
    password = this.password.value

    Authenticator.login(username, password, (loggedIn) => {
      if (loggedIn) {
        this.setState({ redirectToReferrer: true })
      }
    })

  }

  render() {
    return (
      <section id="promo-1" className="content-block promo-2 min-height-600px bg-black">
        <div className="container">
          <div className="row">
            <div className="col-md-5">
              <h2>Please Enter User Login</h2>
              <p><br /></p>
              <form onSubmit={(e) => this.handleSubmit(e)}>
                <div className="row">
                  <div className="col-md-6">
                    <div className="form-group">
                      <input type="text" placeholder="Username" className="form-control" ref={(input) => {this.username = input}} />
                    </div>
                  </div>
                  <div className="col-md-6">
                    <div className="form-group">
                      <input type="password" placeholder="Password" className="form-control" ref={(input) => {this.password = input}} />
                    </div>
                  </div>
                </div>
                <button className="btn btn-primary btn-block" type="submit">Login</button>
              </form>
            </div>
            <div className="col-md-6 col-md-offset-1">
              <img src={login_ledge_photo} width="100%"/>
            </div>
          </div>
        </div>
      </section>
    )
  }

}


export const IsLoggedInWelcomeText = withRouter(({ history }) => (
    // If a user isAuthenticated, show the correct view, otherwise give LoginPage
    Authenticator.isAuthenticated
      ? (
      <p>
        Welcome User!
        <button onClick={() => {Authenticator.logout(() => history.push('/'))}}>
          Log out
        </button>
      </p>
    ) : (
      <LoggedOutView />
    )
  )
)

