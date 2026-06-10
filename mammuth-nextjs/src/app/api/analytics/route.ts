import { NextRequest, NextResponse } from 'next/server';
import { v4 as uuidv4 } from 'uuid';
import type { AnalyticsPayload, AnalyticsResponse } from '@/types/analytics';

const VALID_EVENT_TYPES = new Set([
  'cta_click','section_view','pricing_select','nav_click','feature_hover',
]);

function validatePayload(data: unknown): data is AnalyticsPayload {
  if (!data || typeof data !== 'object') return false;
  const p = data as Record<string, unknown>;
  if (typeof p.eventType !== 'string')        return false;
  if (!VALID_EVENT_TYPES.has(p.eventType))    return false;
  if (typeof p.eventName !== 'string')        return false;
  if (p.eventName.length === 0)               return false;
  if (p.eventName.length > 200)              return false;
  if (typeof p.properties !== 'object')      return false;
  if (typeof p.context !== 'object')         return false;
  const ctx = p.context as Record<string, unknown>;
  if (typeof ctx.anonymousId !== 'string')   return false;
  if (typeof ctx.clientTs !== 'string')      return false;
  const parsed = Date.parse(ctx.clientTs as string);
  if (isNaN(parsed))                         return false;
  if ((Date.now() - parsed) / 1000 > 300)   return false;
  return true;
}

export async function POST(req: NextRequest): Promise<NextResponse<AnalyticsResponse | { error: string }>> {
  const contentType = req.headers.get('content-type') ?? '';
  if (!contentType.includes('application/json')) {
    return NextResponse.json({ error: 'Content-Type must be application/json' }, { status: 415 });
  }
  let body: unknown;
  try { body = await req.json(); }
  catch { return NextResponse.json({ error: 'Malformed JSON body' }, { status: 400 }); }
  if (!validatePayload(body)) {
    return NextResponse.json({ error: 'Invalid payload' }, { status: 422 });
  }
  const eventId    = uuidv4();
  const receivedAt = new Date().toISOString();
  const enriched: AnalyticsPayload = {
    ...body,
    context: { ...body.context, userAgent: req.headers.get('user-agent') ?? 'unknown' },
  };
  console.log(JSON.stringify({
    level: 'info', source: 'analytics',
    eventId, eventType: enriched.eventType, eventName: enriched.eventName,
    anonymousId: enriched.context.anonymousId, url: enriched.context.url,
    receivedAt, properties: enriched.properties,
  }));
  return NextResponse.json({ ok: true, eventId, received: receivedAt, message: 'Event recorded' }, {
    status: 200,
    headers: { 'Cache-Control': 'no-store' },
  });
}

export function OPTIONS(): NextResponse {
  return new NextResponse(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}
