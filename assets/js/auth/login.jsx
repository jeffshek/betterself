// var React = require('react')
// var auth = require('./auth')
// var browserHistory = require('react-router-dom').browserHistory
//
// module.exports = React.createClass({
//     contextTypes: {
//         router: React.PropTypes.object.isRequired
//     },
//
//     handleSubmit: function(e) {
//         e.preventDefault()
//
//         var username = this.refs.username.value
//         var pass = this.refs.pass.value
//
//         auth.login(username, pass, (loggedIn) => {
//             // console.log(browserHistory);
//             this.context.router.transitionTo('/dashboard/')
//             // browserHistory.push('/dashboard/')
//         })
//     },
//
//     render: function() {
//         return (
//             <form onSubmit={this.handleSubmit}>
//                 <input type="text" placeholder="username" ref="username"/>
//                 <input type="password" placeholder="password" ref="pass"/>
//                 <input type="submit"/>
//             </form>
//         )
//     }
// })

import { Component, PropTypes } from 'react';

class Login extends Component {
    handleSubmit(e) {
        e.preventDefault()

        var username = this.refs.username.value
        var pass = this.refs.pass.value

        auth.login(username, pass, (loggedIn) => {
            // console.log(browserHistory);
            this.context.router.transitionTo('/dashboard/')
            // browserHistory.push('/dashboard/')
        })
    };

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <input type="text" placeholder="username" ref="username"/>
                <input type="password" placeholder="password" ref="pass"/>
                <input type="submit"/>
            </form>
        )
    }
}

Login.contextTypes = {
    router: PropTypes.object.isRequired
};

export default Login;
