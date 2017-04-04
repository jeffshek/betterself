import React from 'react';
import { withRouter } from 'react-router-dom';

import { JSON_HEADERS } from '../constants'

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
      .then((responseData) =>
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
    <p>You are not logged in.</p>
  )
))
