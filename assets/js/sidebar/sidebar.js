import React, { Component } from 'react';
import { Link } from "react-router-dom"

const AVATAR_IMG_8 = require('../../img/avatars/8.jpg')

class Sidebar extends Component {

  handleClick(e) {
    e.preventDefault();
    e.target.parentElement.classList.toggle('open');
  }

  // activeRoute(routeName) {
  //   return this.props.location.pathname.indexOf(routeName) > -1 ? 'nav-item nav-dropdown open' : 'nav-item nav-dropdown';
  // }

  // secondLevelActive(routeName) {
  //   return this.props.location.pathname.indexOf(routeName) > -1 ? "nav nav-second-level collapse in" : "nav nav-second-level collapse";
  // }

  render() {
    return (
      <div className="sidebar">
        <div className="sidebar-header">
          <img src={AVATAR_IMG_8} className="img-avatar" alt="Avatar"/>
          <div><strong>JOHN DOE</strong></div>
          <div className="text-muted"><small>Founder &amp; CEO</small></div>

          <div className="btn-group" role="group" aria-label="Button group with nested dropdown">
            <button type="button" className="btn btn-link">
              <i className="icon-settings"></i>
            </button>
            <button type="button" className="btn btn-link">
              <i className="icon-speech"></i>
            </button>
            <button type="button" className="btn btn-link" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <i className="icon-user"></i>
            </button>
          </div>
        </div>
        <nav className="sidebar-nav">
          <ul className="nav">
            <li className="nav-item">
              {/*<Link to={'/dashboard'} className="nav-link" activeClassName="active">*/}
              <Link to={'/dashboard'} className="nav-link">
                <i className="icon-speedometer" />
                  Dashboard
                <span className="badge badge-info">
                  NEW
                </span>
              </Link>
            </li>
            <li className="nav-title">
              UI Elements
            </li>
            <li className="nav-item nav-dropdown">
               <a className="nav-link nav-dropdown-toggle" href="#" onClick={this.handleClick.bind(this)}><i className="icon-puzzle"></i> Components</a>
               <ul className="nav-dropdown-items">
                 <li className="nav-item">
                   <Link to={'/components/buttons'} className="nav-link"><i className="icon-puzzle"></i> Buttons</Link>
                 </li>
                 <li className="nav-item">
                   <Link to={'/components/social-buttons'} className="nav-link"><i className="icon-puzzle"></i> Social Buttons</Link>
                 </li>
                 <li className="nav-item">
                   <Link to={'/components/cards'} className="nav-link"><i className="icon-puzzle"></i> Cards</Link>
                 </li>
                 <li className="nav-item">
                   <Link to={'/components/modals'} className="nav-link"><i className="icon-puzzle"></i> Modals</Link>
                 </li>
                 <li className="nav-item">
                   <Link to={'/components/switches'} className="nav-link"><i className="icon-puzzle"></i> Switches</Link>
                 </li>
                 <li className="nav-item">
                   <Link to={'/components/tables'} className="nav-link"><i className="icon-puzzle"></i> Tables</Link>
                 </li>
                 <li className="nav-item">
                   <Link to={'/components/tabs'} className="nav-link"><i className="icon-puzzle"></i> Tabs</Link>
                 </li>
               </ul>
             </li>
             <li className="nav-item nav-dropdown">
               <a className="nav-link nav-dropdown-toggle" href="#" onClick={this.handleClick.bind(this)}><i className="icon-note"></i> Forms</a>
               <ul className="nav-dropdown-items">
                 <li className="nav-item">
                   <Link to={'/forms/basic-forms'} className="nav-link"><i className="icon-note"></i> Basic Forms</Link>
                 </li>
                 <li className="nav-item">
                   <Link to={'/forms/advanced-forms'} className="nav-link"><i className="icon-note"></i> Advanced Forms</Link>
                 </li>
               </ul>
             </li>

            {/*<li className="nav-item nav-dropdown">*/}
            {/*   <a className="nav-link nav-dropdown-toggle" href="#" onClick={this.handleClick.bind(this)}><i className="icon-star"></i> Icons</a>*/}
            {/*   <ul className="nav-dropdown-items">*/}
            {/*     <li className="nav-item">*/}
            {/*       <Link to={'/icons/font-awesome'} className="nav-link"><i className="icon-star"></i> Font Awesome</Link>*/}
            {/*     </li>*/}
            {/*     <li className="nav-item">*/}
            {/*       <Link to={'/icons/glyphicons'} className="nav-link"><i className="icon-star"></i> Glyphicons</Link>*/}
            {/*     </li>*/}
            {/*     <li className="nav-item">*/}
            {/*       <Link to={'/icons/glyphicons-filetypes'} className="nav-link"><i className="icon-star"></i> Glyphicons Filetypes</Link>*/}
            {/*     </li>*/}
            {/*     <li className="nav-item">*/}
            {/*       <Link to={'/icons/glyphicons-social'} className="nav-link"><i className="icon-star"></i> Glyphicons Social</Link>*/}
            {/*     </li>*/}
            {/*     <li className="nav-item">*/}
            {/*       <Link to={'/icons/simple-line-icons'} className="nav-link"><i className="icon-star"></i> Simple Line Icons</Link>*/}
            {/*     </li>*/}
            {/*   </ul>*/}
            {/* </li>*/}
            {/*<li className="nav-item nav-dropdown">*/}
            {/*   <a className="nav-link nav-dropdown-toggle" href="#" onClick={this.handleClick.bind(this)}><i className="icon-energy"></i> Plugins</a>*/}
            {/*   <ul className="nav-dropdown-items">*/}
            {/*     <li className="nav-item">*/}
            {/*       <Link to={'/plugins/loading-buttons'} className="nav-link"><i className="icon-cursor"></i> Loading Buttons</Link>*/}
            {/*     </li>*/}
            {/*     <li className="nav-item">*/}
            {/*       <Link to={'/plugins/spinners'} className="nav-link"><i className="fa fa-spinner"></i> Spinners</Link>*/}
            {/*     </li>*/}
            {/*   </ul>*/}
            {/* </li>*/}
            {/* <li className="nav-item">*/}
            {/*   <Link to={'/widgets'} className="nav-link"><i className="icon-calculator"></i> Widgets <span className="badge badge-info">NEW</span></Link>*/}
            {/* </li>*/}
            {/* <li className="nav-item">*/}
            {/*   <Link to={'/charts'} className="nav-link"><i className="icon-pie-chart"></i> Charts</Link>*/}
            {/* </li>*/}
            {/* <li className="divider"></li>*/}
            {/* <li className="nav-title">*/}
            {/*   Extras*/}
            {/* </li>*/}
            {/* <li className="nav-item nav-dropdown">*/}
            {/*   <a className="nav-link nav-dropdown-toggle" href="#" onClick={this.handleClick.bind(this)}><i className="icon-star"></i> Pages</a>*/}
            {/*   <ul className="nav-dropdown-items">*/}
            {/*     <li className="nav-item">*/}
            {/*       <Link to={'/pages/login'} className="nav-link"><i className="icon-star"></i> Login</Link>*/}
            {/*     </li>*/}
            {/*     <li className="nav-item">*/}
            {/*       <Link to={'/pages/register'} className="nav-link"><i className="icon-star"></i> Register</Link>*/}
            {/*     </li>*/}
                {/*<li className="nav-item">*/}
                  {/*<Link to={'/pages/404'} className="nav-link"><i className="icon-star"></i> Error 404</Link>*/}
                {/*</li>*/}
                {/*<li className="nav-item">*/}
                  {/*<Link to={'/pages/500'} className="nav-link"><i className="icon-star"></i> Error 500</Link>*/}
                {/*</li>*/}
              {/*</ul>*/}
          </ul>
        </nav>
      </div>
    )
  }
}

// class Sidebar extends Component {
//   render() {
//     return (
//       <div>Hello</div>
//     )
//   }
//
// }

export default Sidebar;
