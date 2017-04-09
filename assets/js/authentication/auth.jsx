import React from 'react';
import { withRouter } from 'react-router-dom';

import { JSON_HEADERS } from '../constants'
import {login_ledge_photo} from '../fragments/image_paths'

export const Authenticator = {
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
    let credentials = {
      username : username,
      password : pass
    }

    fetch('/api-token-auth/', {
      method: 'POST',
      headers: JSON_HEADERS,
      body: JSON.stringify(credentials)
    })
      .then((response) =>
      {
        return response.json()
      })
      .then((responseData) => // Because these are promises second then means data has arrived
      {
        if ('token' in responseData){
          cb({
            authenticated: true,
            token: responseData.token
          })
        }
        else {
          alert("Invalid Login Error")
          cb({
            authenticated: false
          })
        }
      })
      .catch((error) => {
        alert("Network Issue Encountered")
        cb({
          authenticated: false
        })
      })
  },
}

const LoggedOutView = () => {
  return (
    <section id="promo-1" className="content-block promo-2 min-height-600px bg-black">
      {/*<section id="promo-1" className="content-block promo-1 min-height-600px bg-offwhite">*/}
      <div className="container">
        <div className="row">
          <div className="col-md-5">
            <h2>Login, please!</h2>
            <p><br /></p>
            <form>
              <div className="row">
                <div className="col-md-6">
                  <div className="form-group">
                    <input type="text" placeholder="Username" className="form-control" />
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="form-group">
                    <input type="password" placeholder="Password" className="form-control" />
                  </div>
                </div>
              </div>
              <a className="btn btn-primary btn-block">Login</a>
            </form>
          </div>
          <div className="col-md-6 col-md-offset-1">
            <img src={login_ledge_photo} width="100%"/>
          </div>
        </div>
      </div>
    </section>
  );
}

export const AuthButton = withRouter(({ history }) => (
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
    <LoggedOutView />
  )
))
