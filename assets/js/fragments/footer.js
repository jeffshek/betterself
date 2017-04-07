import React, { PropTypes, Component } from 'react'
import { logo_background } from './image_paths'

const BetterSelfAddress = () => <p className="address small">BetterHealth, Inc.<br />99 St Marks, 3D<br />New York, NY, 10009</p>

export default class Footer extends Component {
  render() {
    return (
      <section className="content-block-nopad bg-deepocean footer-wrap-1-3">
        <div className="container footer-1-3">
          <div className="col-md-4 pull-left">
            <img src={logo_background} className="brand-img img-responsive" />
          </div>
          <div className="col-md-3 pull-right">
            <p className="address-bold-line">We <i className="fa fa-heart pomegranate" />&nbsp;analytics</p>
            <BetterSelfAddress/>
          </div>
          <div className="col-xs-12 footer-text">
            <p>Please take a few minutes to read our <a href="#">Terms &amp; Conditions</a> and <a href="#">Privacy Policy</a></p>
          </div>
        </div>
      </section>
    );
  }
}
