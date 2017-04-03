import React from 'react';
import { withRouter } from 'react-router-dom';

const JSON_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }

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
    console.log("wtf 8")
    fetch('/api-token-auth/', {
      method: 'POST',
      headers: JSON_HEADERS,
      body: JSON.stringify(credentials)
    }).then(function(res){
        let json_result = res.json()

        cb({
          authenticated: true,
          token: json_result.token
        })

        console.log(json_result.token)

    }).catch(function(err){
      console.log("no work")
      console.log(err)
    });
    // $.ajax({
    //   type: 'POST',
    //   url: '/api-token-auth/',
    //   data: {
    //     username: username,
    //     password: pass
    //   },
    //   success: function(res){
    //     cb({
    //       authenticated: true,
    //       token: res.token
    //     })
    //   }
    // })
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
