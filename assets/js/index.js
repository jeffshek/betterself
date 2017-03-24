import React from "react"
import { render } from "react-dom"


class Dashboard extends React.Component {

  fetchUserData () {
    return 'Fetching User Data';
  }

  render() {
    return (
      <h1>
        { this.fetchUserData() }
      </h1>
    )
  }
}

render(<Dashboard />, document.getElementById('container'))
