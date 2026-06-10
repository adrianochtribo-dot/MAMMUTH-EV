export type EventType =
  | 'cta_click'
  | 'section_view'
  | 'pricing_select'
  | 'nav_click'
  | 'feature_hover';

export interface AnalyticsContext {
  anonymousId: string;
  url: string;
  referrer: string;
  userAgent?: string;
  viewport: { width: number; height: number };
  clientTs: string;
}

export interface AnalyticsProperties {
  label?: string;
  elementId?: string;
  planName?: string;
  visibilityRatio?: number;
  dwellMs?: number;
  [key: string]: unknown;
}

export interface AnalyticsPayload {
  eventType: EventType;
  eventName: string;
  properties: AnalyticsProperties;
  context: AnalyticsContext;
}

export interface AnalyticsResponse {
  ok:       boolean;
  eventId:  string;
  received: string;
  message:  string;
}
