"""Globe-Visualizer (frontend + backend merged) - globe payload for Monad activity.
Backend: build points/arcs. Frontend: the exact JSON payload + a minimal render snippet it consumes.
"""
import hashlib, json
def point_for(key, weight=1.0):
    h=int(hashlib.sha256(key.encode()).hexdigest(), 16)
    lat=((h>>8)%1700)/10-85; lng=((h>>24)%3500)/10-175
    return {"key": key, "lat": round(lat,2), "lng": round(lng,2), "weight": weight}
def backend_payload(protocols, tx_keys=()):
    return {"points": [point_for(p, 2.0) for p in protocols] + [point_for(t) for t in tx_keys],
            "arcs": [{"from": point_for(protocols[i]), "to": point_for(protocols[i+1])} for i in range(len(protocols)-1)] if len(protocols)>1 else [],
            "meta": {"source": "Mon-Ultra-Matrix globe backend", "renderer": "globe-visualizer-frontend"}}
def frontend_snippet(payload):
    return "<script>window.GLOBE_DATA = "+json.dumps(payload)+"; // globe-visualizer-frontend renders window.GLOBE_DATA</script>"
