import React, {PropTypes, Component} from "react";
import {Link} from "react-router-dom";
import LoggedOutHeader from "../header/external_header";
import Footer from "../fragments/footer";
import HomePageDescriptionSection from "./components/HomePageDescription";
import HomePageAnalyticsDescriptionSection from "./components/HomePageAnalyticsDescriptionSection";
import HomePageFeaturesShortDescriptionSection from "./components/HomePageFeaturesShortDescriptionSection";
import OpenSourceAndApplicationSupport from "./components/OpenSourceAndApplicationSupport";


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
