import React from "react"
import { render } from "react-dom"


class Example extends React.Component {
  render() {
    return (
      <h1>
          Hello React
      </h1>
    )
  }
}

render(<Example />, document.getElementById('container'))