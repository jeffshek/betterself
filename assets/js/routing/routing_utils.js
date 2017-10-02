import React from "react";
import { DATE_REQUEST_FORMAT } from "../constants/dates_and_times";
import {
  DASHBOARD_DAILY_OVERVIEW_ANALYTICS_URL,
  DASHBOARD_SUPPLEMENT_OVERVIEW_ANALYTICS_URL
} from "../constants/urls";

export const getDailyOverViewURLFromDate = date => {
  const dateString = date.format(DATE_REQUEST_FORMAT);
  return `${DASHBOARD_DAILY_OVERVIEW_ANALYTICS_URL}${dateString}`;
};

export const getSupplementOverviewURLFromUUID = uuid => {
  return `${DASHBOARD_SUPPLEMENT_OVERVIEW_ANALYTICS_URL}${uuid}`;
};

export const getSupplementAnalyticsSummaryURL = supplement => {
  return `/api/v1/supplements/${supplement.uuid}/analytics/summary/`;
};

export const getSupplementSleepAnalyticsURL = supplement => {
  return `/api/v1/supplements/${supplement.uuid}/analytics/sleep/`;
};

export const getSupplementProductivityAnalyticsURL = supplement => {
  return `/api/v1/supplements/${supplement.uuid}/analytics/productivity/`;
};

export const getSupplementDosagesAnalyticsURL = supplement => {
  return `/api/v1/supplements/${supplement.uuid}/analytics/dosages/`;
};

export const getSupplementAggregatesAnalyticsURL = supplement => {
  return `/api/v1/supplements/${supplement.uuid}/log/aggregate/`;
};
