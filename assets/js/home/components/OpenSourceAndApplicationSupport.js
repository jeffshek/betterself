import React, { PropTypes, Component } from "react";
import CSSModules from 'react-css-modules';

import styles from '../css/OpenSourceAndApplicationSupport.css'

class OpenSourceAndApplicationSupport extends React.Component {
  render () {
    return (
      <section styleName="content-deep-ocean">
        <div className="container text-center">
          <a
            href="https://github.com/jeffshek/betterself"
            className="btn btn-outline btn-outline-xl outline-light"
          >
            Made with <span className="fa fa-heart pomegranate" /> on GitHUb
          </a>
          <h2>
            Track your progress on <b>iOS</b> or <b>Android</b>&nbsp;devices.
          </h2>
        </div>
      </section>
    );
  }
}

export default CSSModules(OpenSourceAndApplicationSupport, styles)
