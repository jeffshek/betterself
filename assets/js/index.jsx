import React, { PropTypes } from 'react'
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from 'react-router-dom'

import { DASHBOARD_OVERVIEW, DASHBOARD_INDEX, LOGIN_PATH } from './urls/constants'
import { Authenticator, AuthButton } from './auth/auth'
import Login from './auth/login'

const Public = () => <h3>Public</h3>
const Protected = () => <h3>Protected</h3>

// http://stackoverflow.com/questions/38510111/react-js-do-common-header
//
// import Header from './header.jsx';
//
// class App extends Component {
//   render() {
//     return (
//       <div>
//         <Header />
//         {this.props.children}
//       </div>
//     );
//   }
// }

const DashboardRouter = () => (
  <Router>
    <div>
      <AuthButton/>
      <ul>
        <li><Link to={DASHBOARD_OVERVIEW}>Overview Page</Link></li>
        <li><Link to={DASHBOARD_INDEX}>Dashboard Index</Link></li>
      </ul>
      <Route path={DASHBOARD_OVERVIEW} component={Public}/>
      <Route path={LOGIN_PATH} component={Login}/>
      {/*Goal is to eventually wrap all Routes that should be protected under a component*/}
      <PrivateRoute path={DASHBOARD_INDEX} component={Protected}/>
    </div>
  </Router>
)

const PrivateRoute = ({ component, ...rest }) => (
  <Route {...rest} render={props => (
    Authenticator.isAuthenticated ? (
      React.createElement(component, props)
    ) : (
      <Redirect to={{
        pathname: LOGIN_PATH,
        state: { from: props.location }
      }}/>
    )
  )}/>
)

ReactDOM.render(
  <DashboardRouter />, document.getElementById('dashboard')
)
