import React from "react"
let auth = require('./auth')

export default React.createClass({
  contextTypes: {
    router: React.PropTypes.object.isRequired
  },

  handleSubmit: function(e) {
    e.preventDefault()

    let username = this.refs.username.value
    let pass = this.refs.pass.value

    auth.login(username, pass, (loggedIn) => {
      if (loggedIn) {
        this.context.router.replace('/app/')
      }
    })
  },

  render: function() {
    return (
      <form onSubmit={this.handleSubmit}>
        <input type="text" placeholder="username" ref="username" />
        <input type="password" placeholder="password" ref="pass" />
        <input type="submit" />
      </form>
    )
  }
})
