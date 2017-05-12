import React, { PropTypes, Component } from "react";

import { Link } from "react-router-dom";
import LoggedOutHeader from "../header/external_header";

import Footer from "../fragments/footer";
import FontAwesomeIconBox from "./components/FontAwesomeIconBox"
import HomePageDescriptionSection from "./components/HomePageDescription"
import HomePageAnalyticsDescriptionSection from './components/HomePageAnalyticsDescriptionSection'
import HomePageFeaturesShortDescriptionSection from './components/HomePageFeaturesShortDescriptionSection'
import CSSModules from 'react-css-modules';

import styles from '../../../betterself/static/css/pinegrow/legacy.css'


{/*const HomePageFeaturesShortDescriptionSection = () => {*/}
  {/*return (*/}
    {/*<section id="content-3-5" className="content-block content-3-5">*/}
      {/*<div className="container">*/}
        {/*<div className="row">*/}
          {/*<FontAwesomeIconBox*/}
            {/*icon="fa fa-pencil"*/}
            {/*header="Simple"*/}
//             description="Integrates with all major fitness trackers. Automatically gets data to give the most accurate snapshot of &nbsp;you."
//           />
//           <FontAwesomeIconBox
//             icon="fa fa-code"
//             header="Privacy"
//             description="We respect privacy. Your data is confidential and we don't store names or emails. Comes with a purge data option. &nbsp;"
//           />
//           <FontAwesomeIconBox
//             icon="fa fa-search"
//             header="Analytics"
//             description="How many hours of sleep do you really need? Does fish oil actually help? We help you eliminate truth from placebo."
//           />
//           <FontAwesomeIconBox
//             icon="fa fa-mobile"
//             header="Integrations"
//             description="Track supplement or medication usage in seven seconds or less. Available on iOS and Android."
//           />
//         </div>
//       </div>
//     </section>
//   );
// };

const OpenSourceAndApplicationSupport = () => {
  return (
    <section
      id="content-2-1"
      className="content-block content-2-1 bg-deepocean"
    >
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
};

export const HomePage = () => {
  return (
    <div>
      <LoggedOutHeader />
      <HomePageDescriptionSection />
      <HomePageAnalyticsDescriptionSection />
      <HomePageFeaturesShortDescriptionSection />
      <OpenSourceAndApplicationSupport />
      <Footer />
    </div>
  );
};
