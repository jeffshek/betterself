import React from "react"
import { render } from "react-dom"


class Dashboard extends React.Component {
  render() {
    return (
      <h1>
        Insert Dashboard Things.
      </h1>
    )
  }
}

render(<Dashboard />, document.getElementById('container'))
