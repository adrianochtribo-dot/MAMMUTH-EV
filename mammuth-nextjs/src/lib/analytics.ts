import { v4 as uuidv4 } from 'uuid';
import type { AnalyticsPayload, AnalyticsContext, EventType, AnalyticsProperties } from '@/types/analytics';

const SESSION_KEY = 'mme_anon_id';

function getAnonymousId(): string {
  if (typeof sessionStorage === 'undefined') return 'ssr';
  let id = sessionStorage.getItem(SESSION_KEY);
  if (!id) { id = uuidv4(); sessionStorage.setItem(SESSION_KEY, id); }
  return id;
}

function buildContext(): AnalyticsContext {
  return {
    anonymousId: getAnonymousId(),
    url:      typeof window !== 'undefined' ? window.location.href : '',
    referrer: typeof document !== 'undefined' ? document.referrer : '',
    viewport: {
      width:  typeof window !== 'undefined' ? window.innerWidth  : 0,
      height: typeof window !== 'undefined' ? window.innerHeight : 0,
    },
    clientTs: new Date().toISOString(),
  };
}

export async function fireEvent(
  eventType:  EventType,
  eventName:  string,
  properties: AnalyticsProperties = {},
): Promise<void> {
  const payload: AnalyticsPayload = {
    eventType, eventName, properties, context: buildContext(),
  };
  const endpoint = '/api/analytics';
  const body     = JSON.stringify(payload);
  try {
    await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
      keepalive: true,
    });
  } catch {
    if (typeof navigator !== 'undefined' && navigator.sendBeacon) {
      navigator.sendBeacon(endpoint, new Blob([body], { type: 'application/json' }));
    }
  }
}

const seenSections = new Set<string>();

export function initSectionTracking(): () => void {
  if (typeof IntersectionObserver === 'undefined') return () => {};
  const entryTimes = new Map<string, number>();
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      const sectionId = (entry.target as HTMLElement).dataset.trackSection;
      if (!sectionId) return;
      if (entry.isIntersecting && !seenSections.has(sectionId)) {
        entryTimes.set(sectionId, Date.now());
        seenSections.add(sectionId);
        fireEvent('section_view', sectionId, { visibilityRatio: Math.round(entry.intersectionRatio * 100) });
      } else if (!entry.isIntersecting && entryTimes.has(sectionId)) {
        const dwell = Date.now() - (entryTimes.get(sectionId) ?? 0);
        entryTimes.delete(sectionId);
        fireEvent('section_view', `${sectionId}:dwell`, { dwellMs: dwell });
      }
    });
  }, { threshold: [0, 0.2, 1] });
  document.querySelectorAll<HTMLElement>('[data-track-section]').forEach((el) => observer.observe(el));
  return () => observer.disconnect();
}

export function trackPlanSelect(planName: string): void {
  fireEvent('pricing_select', `Piano: ${planName}`, { planName });
}
