import React, { Component } from 'react';
import { Link } from "react-router-dom"

class Sidebar extends Component {

  handleClick(e) {
    e.preventDefault();
    e.target.parentElement.classList.toggle('open');
  }

  render() {
    return (
      <div className="sidebar">
        <nav className="sidebar-nav">
          <ul className="nav">
            <li className="nav-item">
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

            <li className="nav-item nav-dropdown">
               <a className="nav-link nav-dropdown-toggle" href="#" onClick={this.handleClick.bind(this)}><i className="icon-energy"></i> Plugins</a>
               <ul className="nav-dropdown-items">
                 <li className="nav-item">
                   <Link to={'/plugins/loading-buttons'} className="nav-link"><i className="icon-cursor"></i> Loading Buttons</Link>
                 </li>
                 <li className="nav-item">
                   <Link to={'/plugins/spinners'} className="nav-link"><i className="fa fa-spinner"></i> Spinners</Link>
                 </li>
               </ul>
             </li>
             <li className="nav-item">
               <Link to={'/widgets'} className="nav-link"><i className="icon-calculator"></i> Widgets <span className="badge badge-info">NEW</span></Link>
             </li>
             <li className="nav-item">
               <Link to={'/charts'} className="nav-link"><i className="icon-pie-chart"></i> Charts</Link>
             </li>
             <li className="divider"></li>
             <li className="nav-title">
               Extras
             </li>
             <li className="nav-item nav-dropdown">
               <a className="nav-link nav-dropdown-toggle" href="#" onClick={this.handleClick.bind(this)}><i className="icon-star"></i> Pages</a>
               <ul className="nav-dropdown-items">
                 <li className="nav-item">
                   <Link to={'/pages/login'} className="nav-link"><i className="icon-star"></i> Login</Link>
                 </li>
                 <li className="nav-item">
                   <Link to={'/pages/register'} className="nav-link"><i className="icon-star"></i> Register</Link>
                 </li>
                <li className="nav-item">
                  <Link to={'/pages/404'} className="nav-link"><i className="icon-star"></i> Error 404</Link>
                </li>
                <li className="nav-item">
                  <Link to={'/pages/500'} className="nav-link"><i className="icon-star"></i> Error 500</Link>
                </li>
              </ul>
             </li>
          </ul>
        </nav>
      </div>
    )
  }
}

export default Sidebar;
