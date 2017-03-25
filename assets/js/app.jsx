var React = require('react')
var auth = require('./auth/auth')

module.exports = React.createClass({
    getInitialState: function() {
        return {'user':[]}
    },

    componentDidMount: function() {
        this.loadUserData()
    },

    contextTypes: {
        router: React.PropTypes.object.isRequired
    },

    logoutHandler: function() {
        auth.logout()
        this.context.router.replace('/login/')
    },

    loadUserData: function() {
        $.ajax({
            method: 'GET',
            // change this so this actually works
            url: '/api/users/i/',
            datatype: 'json',
            headers: {
                'Authorization': 'Token ' + localStorage.token
            },
            success: function(res) {
                this.setState({user: res})
            }.bind(this)
        })
    },

    render: function() {
        return (
            <div>
            <h1>You are now logged in, {this.state.user.username}</h1>
            <button onClick={this.logoutHandler}>Log out</button>
            </div>
        )
    }
})
